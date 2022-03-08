import httpx
import re
import os
from PIL import Image
from bs4 import BeautifulSoup
from hoshino import R

async def generate_url(sup_type):
    # 先保留rank吧，防止跟以前的根卡界面一样
    rank = 'SSR'
    # 试了下，发现bwiki是可以自动跳转的，所以可以这样写，还减少了反爬虫的概率
    # 等啥时候不能自动跳转了再说吧
    if sup_type == '速卡':
        chart_url = 'https://wiki.biligame.com/umamusume/SSR速卡节奏榜（Ver.1.15.2）已更新成田路'
    elif sup_type == '耐卡':
        chart_url = 'https://wiki.biligame.com/umamusume/SSR耐卡节奏榜（Ver.1.16.0）已更新目白光明'
    elif sup_type == '力卡':
        chart_url = 'https://wiki.biligame.com/umamusume/SSR力卡节奏榜（Ver.1.13.2）已更新爱丽数码'
    elif sup_type == '根卡':
        chart_url = 'https://wiki.biligame.com/umamusume/SSR根卡节奏榜（Ver.1.15.2）已更新SR织姬'
    elif sup_type == '智卡':
        chart_url = 'https://wiki.biligame.com/umamusume/SSR智卡节奏榜（Ver.1.15.2）已更新周年光钻'
    img_dict = await get_img(rank, sup_type, chart_url)
    return img_dict

async def get_img(rank, sup_type, chart_url):
    res = httpx.get(chart_url, timeout=10)
    soup = BeautifulSoup(res.text, 'lxml')
    pattern = re.compile(f'{rank}{sup_type}节奏榜\S+')
    # 这里获取URL的真实名称
    true_id = soup.find(text=pattern)
    ver = re.search(r'(Ver\.)([0-9]*\.[0-9]*\.[0-9]*)', str(true_id))
    ver = ver.group(2)
    sup_type_tmp = sup_type.replace('卡', '')
    img_dict = {}
    for i in range(3):
        file_name = f'{sup_type_tmp}{ver}.{str(i)}.png'
        res_tmp = httpx.get(f'https://wiki.biligame.com/umamusume/文件:{file_name}', timeout=10)
        soup_tmp = BeautifulSoup(res_tmp.text, 'lxml')
        img_url_tmp = soup_tmp.find(title=file_name)
        if img_url_tmp:
            img_url = img_url_tmp.get('href')
            img_dict[file_name] = img_url
    return img_dict

async def download_img(url, current_dir):
    img_path = R.img('uma_support_chart').path
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    response = httpx.get(url, timeout=10)
    with open(current_dir, 'wb') as f:
        f.write(response.read())

async def generate_img(sup_type):
    img_dict = await generate_url(sup_type)
    data_dict = {}
    # 如果最新的网页已更新，但大佬的图片未上传（一般不会遇到这样的问题）
    if not img_dict:
        # 就生成旧版节奏榜
        file_list = await generate_old_img(sup_type)
        if not file_list:
            return False, False
        for img_name in file_list:
            current_dir = os.path.join(R.img('uma_support_chart').path, f'{img_name}')
            img = Image.open(current_dir)
            data_dict[img_name] = {}
            data_dict[img_name]['width'] = img.width
            data_dict[img_name]['height'] = img.height
            data_dict[img_name]['img'] = img
        all_height = 0
        for img_name in list(data_dict.keys()):
            all_height += data_dict[img_name]['height']
            all_width = data_dict[img_name]['width']
        end_img = Image.new('RGB', (all_width, all_height))
        return end_img, 'old'
    for img_name in list(img_dict.keys()):
        current_dir = os.path.join(R.img('uma_support_chart').path, f'{img_name}')
        await download_img(img_dict[img_name], current_dir)
        img = Image.open(current_dir)
        data_dict[img_name] = {}
        data_dict[img_name]['width'] = img.width
        data_dict[img_name]['height'] = img.height
        data_dict[img_name]['img'] = img
    all_height = 0
    for img_name in list(data_dict.keys()):
        all_height += data_dict[img_name]['height']
        all_width = data_dict[img_name]['width']
    end_img = Image.new('RGB', (all_width, all_height))
    all_height = 0
    for img_name in list(data_dict.keys()):
        img_tmp = data_dict[img_name]['img']
        end_img.paste(img_tmp, (0, all_height))
        all_height += data_dict[img_name]['height']
    return end_img, 'new'

async def generate_old_img(sup_type):
    sup_type = sup_type.replace('卡', '')
    file_name_pattern = re.compile(f'力\S+\.png')
    path = R.img('uma_support_chart').path
    file_list = []
    if os.path.isdir(path) and os.listdir(path):
        for file in os.listdir(path):
            if re.match(file_name_pattern, file):
                file_list.append(str(file))
    return file_list