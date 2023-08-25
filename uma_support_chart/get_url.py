import httpx
import re
import os
from PIL import Image
from bs4 import BeautifulSoup
import json

from hoshino import R, logger
from ..plugin_utils.base_util import get_img_cq

# 获取各个节奏榜的链接
async def get_title_url(sup_type):
    url_header = 'https://wiki.biligame.com/umamusume/'
    url_region = 'https://wiki.biligame.com/umamusume/支援卡节奏榜合集'
    res = httpx.get(url_region, timeout=10)
    soup = BeautifulSoup(res.text, 'lxml')
    title = soup.find('a', {"title": re.compile(fr"^((?!SR).)*{sup_type}卡节奏榜\S+$")}).text
    return url_header + title

# 生成字典
async def generate_url(sup_type):
    # 获取配置
    current_dir = os.path.join(os.path.dirname(__file__), 'sup_config.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        img_dict = json.load(f)
    img_path = os.path.join(R.img('umamusume').path, 'uma_support_chart/')
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    # 获取存储的链接
    chart_url = await get_title_url(sup_type)
    if not img_dict.get(sup_type, None):
        logger.info(f'配置文件内未找到{sup_type}卡节奏榜相关配置，现已成功创建')
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
    ver_old = 0
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
        # 获取新图片
        img_dict = await get_image(img_dict, sup_type, chart_url, ver_body)
        # 如果img_data是空就说明虽然版本更新，但一图流未更新，恢复旧版本号
        if not img_dict[sup_type]['img_data']:
            img_dict[sup_type]['version'] = ver_old
    return img_dict, is_update

# 获取详细图片数据
async def get_image(img_dict, sup_type, chart_url, ver_body):
    # 真实的页面
    res = httpx.get(chart_url, timeout=10)
    soup = BeautifulSoup(res.text, 'lxml')
    # name_pattern = re.compile(f'{sup_type}[0-9]\.[0-9][0-9]\.[0-9]\.[0-9]\.png')
    name_pattern = re.compile(f'(巅峰杯)?{sup_type}[0-9]\.[0-9][0-9]\.[0-9]榜\.png')
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
    img_path = os.path.join(R.img('umamusume').path, 'uma_support_chart/')
    current_dir = os.path.join(img_path, file_name)
    response = httpx.get(url, timeout=10)
    with open(current_dir, 'wb') as f:
        f.write(response.read())
    # 压缩图片
    im = Image.open(current_dir)
    x, y = im.size
    k = 900 / x
    out = im.resize((int(x*k), int(y*k)))
    out.save(current_dir, quality=80)
    logger.info(f'最新版节奏榜图片：{file_name}下载成功')

# 删除旧版图片
async def del_img(sup_type):
    img_path = os.path.join(R.img('umamusume').path, 'uma_support_chart/')
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
        current_dir = os.path.join(os.path.join(R.img('umamusume').path, 'uma_support_chart/'), f'{img_name}')
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

# 删除错误的信息配置
async def del_err_info(sup_type):
    current_dir = os.path.join(os.path.dirname(__file__), 'sup_config.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        img_dict = json.load(f)
    img_dict.pop(sup_type)
    with open(current_dir, 'w', encoding='UTF-8') as f:
        json.dump(img_dict, f, indent=4, ensure_ascii=False)

# 返回消息
async def generate_img(sup_type):
    try:
        img_dict, is_update = await generate_url(sup_type)
    except httpx.ConnectTimeout:
        return '请求超时，请重试'
    end_path = os.path.join(R.img('umamusume').path, 'uma_support_chart/end_img/')
    if not os.path.exists(end_path):
        os.mkdir(end_path)
    end_img_path = os.path.join(end_path, f'end_{sup_type}.png')
    # 没有更新时，直接发送本地图片
    if not is_update:
        logger.info(f'{sup_type}卡节奏榜没有更新，将发送本地图片文件')
        # 图片丢失就再合成一下，正常情况不会运行到这
        if not os.path.exists(end_img_path):
            logger.info(f'本地{sup_type}卡节奏榜图片文件丢失，正在重新合成')
            try:
                end_img = await fix_img(img_dict, sup_type)
            # 如果配置里有信息，但实际没有图片
            except UnboundLocalError as e:
                await del_err_info(sup_type)
                msg_ = f'遇到特殊问题{e}，因此已清除缓存信息，请尝试重新使用命令“{sup_type}卡节奏榜”'
                logger.info(msg_)
                return msg_
            end_img.save(end_img_path, 'PNG')
        msg = await get_img_cq(end_img_path)
        return msg
    # 检测到更新，但是图片还没上传
    if not img_dict[sup_type]['img_data']:
        logger.info(f'{sup_type}卡节奏榜有更新，但未获取到图片，将发送旧版图片')
        msg = await get_img_cq(end_img_path)
        return msg
    # 有更新就先合成完整图片
    end_img = await fix_img(img_dict, sup_type)
    end_img.save(end_img_path, 'PNG')
    msg = await get_img_cq(end_img_path)
    return msg