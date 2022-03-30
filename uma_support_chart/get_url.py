import httpx
import re
import os
from PIL import Image
from bs4 import BeautifulSoup
import json
import asyncio
from hoshino import R, logger

# 获取真实的url链接
async def get_true_url(old_url):
    await asyncio.sleep(0.5)
    res = httpx.get(old_url, timeout=10)
    soup = BeautifulSoup(res.text, 'lxml')
    redirect = soup.find('div', {"class": "redirectMsg"})
    if redirect:
        # 下一级url的标题
        title = redirect.find('ul').find('li').find('a').text
        # 拼接出新的url链接
        next_url = 'https://wiki.biligame.com/umamusume/' + str(title)
        true_url = await get_true_url(next_url)
    # 不点击重定向了就对获取本链接重定向的链接
    else:
        title= re.findall('<title>(.+)</title>', res.text)[0]
        title = title.replace(' - 赛马娘WIKI_BWIKI_哔哩哔哩', '')
        true_url = 'https://wiki.biligame.com/umamusume/' + str(title)
    return true_url

# 生成字典
async def generate_url(sup_type):
    # 获取配置
    current_dir = os.path.join(os.path.dirname(__file__), 'sup_config.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        img_dict = json.load(f)
    # 获取存储的链接
    if img_dict.get(sup_type, None):
        old_url = img_dict[sup_type]['chart_url']
        chart_url = await get_true_url(old_url)
        if old_url != chart_url:
            img_dict[sup_type]['chart_url'] = chart_url
    # 不存在就通过 旧链接 获取 新链接
    else:
        logger.info(f'配置文件内未找到{sup_type}卡节奏榜相关配置，现已成功创建')
        if sup_type == '速':
            old_url = 'https://wiki.biligame.com/umamusume/SSR速卡节奏榜（Ver.1.15.2）已更新成田路'
        elif sup_type == '耐':
            old_url = 'https://wiki.biligame.com/umamusume/SSR耐卡节奏榜（Ver.1.16.0）已更新目白光明'
        elif sup_type == '力':
            old_url = 'https://wiki.biligame.com/umamusume/SSR力卡节奏榜（Ver.1.13.2）已更新爱丽数码'
        elif sup_type == '根':
            old_url = 'https://wiki.biligame.com/umamusume/SSR根卡节奏榜（Ver.1.15.2）已更新SR织姬'
        elif sup_type == '智':
            old_url = 'https://wiki.biligame.com/umamusume/SSR智卡节奏榜（Ver.1.15.2）已更新周年光钻'
        elif sup_type == '友人':
            old_url = 'https://wiki.biligame.com/umamusume/友人卡节奏榜（Ver.1.16.6）至天狼星小队'
        chart_url = await get_true_url(old_url)
        img_dict[sup_type] = {}
        img_dict[sup_type]['chart_url'] = chart_url
    img_dict, is_update = await get_img(img_dict, sup_type, chart_url)
    # 写入新的信息
    with open(current_dir, 'w', encoding='UTF-8') as f:
        json.dump(img_dict, f, indent=4, ensure_ascii=False)
    return img_dict, is_update

# 获取图像
async def get_img(img_dict, sup_type, chart_url):
    # 获取最新版本号
    ver_tmp = re.search(r'(Ver\.)([0-9]*)\.([0-9]*)\.([0-9]*)', chart_url)
    # 精确版本
    ver = ver_tmp.group(2) + '.' + ver_tmp.group(3) + '.' + ver_tmp.group(4)
    # 大版本
    ver_body = ver_tmp.group(2) + '.' + ver_tmp.group(3)
    # 比较版本号
    ver_int = int(ver.replace('.', ''))
    ver_old_int = 0
    if img_dict[sup_type].get('version', None):
        ver_old = img_dict[sup_type]['version']
        ver_old_int = int(ver_old.replace('.', ''))
    # 如果获取到的版本大于当前版本，就说明表格更新了
    is_update = False
    if ver_int > ver_old_int:
        logger.info(f'{sup_type}卡节奏榜有更新，正在替换旧版文件')
        is_update = True
        ver_now = ver 
        img_dict[sup_type]['version'] = ver_now
        img_dict[sup_type]['img_data'] = {}
        # 删除旧版图片
        await del_img(sup_type)
        img_dict = await get_image(img_dict, sup_type, chart_url, ver_body,)
    return img_dict, is_update

# 获取详细图片数据
async def get_image(img_dict, sup_type, chart_url, ver_body):
    # 真实的页面
    res = httpx.get(chart_url, timeout=10)
    soup = BeautifulSoup(res.text, 'lxml')
    name_pattern = re.compile(f'{sup_type}{ver_body}\.\d\.\d[\.\(\d\)]?\.png')
    img_soup_list = soup.find_all('img', {"decoding": "async"})
    for img_soup in img_soup_list:
        file_name = re.match(name_pattern, img_soup.get('alt'))
        if file_name:
            file_name = file_name.group(0)
            img_dict[sup_type]['img_data'][file_name] = img_soup.get('src')
            await download_img(file_name, img_soup.get('src'))
    return img_dict

# 下载图片
async def download_img(file_name, url):
    img_path = R.img('uma_support_chart').path
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    current_dir = os.path.join(img_path, file_name)
    response = httpx.get(url, timeout=10)
    with open(current_dir, 'wb') as f:
        f.write(response.read())
    logger.info(f'最新版节奏榜图片：{file_name}下载成功')

# 删除旧版图片
async def del_img(sup_type):
    img_path = R.img('uma_support_chart').path
    img_pattern = re.compile(f'{sup_type}\S+\.png')
    for file in os.listdir(img_path):
        file_name = re.match(img_pattern, file)
        if file_name:
            file_name = file_name.group(0)
            current_dir = os.path.join(img_path, file_name)
            os.remove(current_dir)
            logger.info(f'旧版{sup_type}卡节奏榜图片{file_name}删除成功')

# 合成图片
async def fix_img(img_dict, sup_type):
    data_dict = {}
    for img_name in list(img_dict[sup_type]['img_data'].keys()):
        current_dir = os.path.join(R.img('uma_support_chart').path, f'{img_name}')
        img = Image.open(current_dir)
        data_dict[img_name] = {}
        data_dict[img_name]['width'] = img.width
        data_dict[img_name]['height'] = img.height
        data_dict[img_name]['img'] = img
    all_height = 0
    for img_name in list(img_dict[sup_type]['img_data'].keys()):
        all_height += data_dict[img_name]['height']
        all_width = data_dict[img_name]['width']
    end_img = Image.new('RGB', (all_width, all_height))
    all_height = 0
    for img_name in list(img_dict[sup_type]['img_data'].keys()):
        img_tmp = data_dict[img_name]['img']
        end_img.paste(img_tmp, (0, all_height))
        all_height += data_dict[img_name]['height']
    logger.info(f'{sup_type}卡节奏榜图片合成成功，即将准备发送')
    return end_img

# 返回消息
async def generate_img(sup_type):
    try:
        img_dict, is_update = await generate_url(sup_type)
    except httpx.ConnectTimeout:
        return '请求超时，请重试'
    img_path = R.img('uma_support_chart').path
    end_path = os.path.join(img_path, 'end_img/')
    if not os.path.exists(end_path):
        os.mkdir(end_path)
    end_img_path = os.path.join(end_path, f'end_{sup_type}.png')
    # 没有更新时，直接发送本地图片
    if not is_update:
        logger.info(f'{sup_type}卡节奏榜没有更新，将发送本地图片文件')
        # 图片丢失就再合成一下
        if not os.path.exists(end_img_path):
            logger.info(f'本地{sup_type}卡节奏榜图片文件丢失，正在重新合成')
            end_img = await fix_img(img_dict, sup_type)
            end_img.save(end_img_path, 'PNG')
        msg = f'[CQ:image,file=file:///{os.path.abspath(end_img_path)}]'
        return msg
    # 有更新就先合成完整图片
    end_img = await fix_img(img_dict, sup_type)
    end_img.save(end_img_path, 'PNG')
    msg = f'[CQ:image,file=file:///{os.path.abspath(end_img_path)}]'
    return msg