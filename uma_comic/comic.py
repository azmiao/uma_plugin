import random
import re

import httpx
from bs4 import BeautifulSoup

from yuiChyan import base_res_path
from ..plugin_utils.base_util import get_img_cq
from ..uma_info.info_utils import *


async def update_info():
    img_dict = await get_img_dict()
    for image in img_dict:
        await download_img(image.get('comic_id'), image.get('url'))
    await create_config(img_dict)


# 获取漫画的url字典
async def get_img_dict():
    url = 'https://wiki.biligame.com/umamusume/1格漫画'
    res = httpx.get(url, timeout=15)
    soup = BeautifulSoup(res.text, 'lxml')
    img_list = []
    all_gallery = soup.find('ul', {"class": "gallery mw-gallery-slideshow"}).find_all('img')
    comic_id = 1
    for gallery in all_gallery:
        img_name_raw = gallery.get('alt').replace('.jpg', '').replace('.png', '').replace('一格', '')
        match = re.match(r'^(\S+?)(\d*)$', img_name_raw)
        img_name = match.group(1)

        uma_id = await get_uma_id(img_name)
        if not uma_id:
            continue

        img_list.append({
            'comic_id': comic_id,
            'url': await adjust_url(gallery.get('src')),
            'uma_id': uma_id
        })

        comic_id += 1
    return img_list


# 调整url
async def adjust_url(url):
    url_pattern = re.compile(r'https://patchwiki\.biligame\.com/images/umamusume\S+?(/\S+?\.(jpg|png))')
    url_g = re.match(url_pattern, url)
    url = url_g.group(0).replace('/thumb', '')
    return url


# 创建json配置文件
async def create_config(img_dict):
    current_dir = os.path.join(os.path.dirname(__file__), f'comic_config_v2.json')
    with open(current_dir, 'w', encoding='UTF-8') as af:
        # noinspection PyTypeChecker
        json.dump(img_dict, af, indent=4, ensure_ascii=False)


# 下载图片
async def download_img(comic_id, url):
    res_path = os.path.join(base_res_path, 'umamusume')
    img_path = os.path.join(res_path, 'uma_comic')
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    current_dir = os.path.join(img_path, f'uma_comic_{comic_id}.jpg')
    if os.path.exists(current_dir):
        logger.info(f'检测到马娘漫画 uma_comic_{comic_id}.jpg 已存在，将不会重新下载')
    else:
        response = httpx.get(url, timeout=10)
        with open(current_dir, 'wb') as f:
            f.write(response.read())
        logger.info(f'未检测到马娘漫画 uma_comic_{comic_id}.jpg ，现已下载成功')



# 按马娘名字的漫画
async def get_comic_uma(uma_name_tmp):
    uma_id = await get_uma_id(uma_name_tmp)
    if not uma_id:
        return ''
    res_path = os.path.join(base_res_path, 'umamusume')
    path = os.path.join(res_path, 'uma_comic')
    current_dir = os.path.join(os.path.dirname(__file__), f'comic_config_v2.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        img_data = json.load(f)
    msg_list = []
    for comic in img_data:
        if comic.get('uma_id') == uma_id:
            comic_id = comic.get('comic_id')
            img_path = os.path.join(path, f'uma_comic_{comic_id}.jpg')
            # 当文件丢失就重新下载
            if not os.path.exists(img_path):
                await download_img(comic_id, comic.get('url'))
            img = await get_img_cq(img_path)
            msg = f'> Comic Id: {comic_id}{img}'
            msg_list.append(msg)
    return '\n'.join(msg_list) if msg_list else None


# 按编号的漫画
async def get_comic_id(comic_id):
    res_path = os.path.join(base_res_path, 'umamusume')
    path = os.path.join(res_path, 'uma_comic')
    img_path = os.path.join(path, f'uma_comic_{comic_id}.jpg')
    if not os.path.exists(img_path):
        return f'此编号的漫画不存在哦'
    msg = await get_img_cq(img_path)
    return msg


# 随机漫画
async def get_comic_random():
    res_path = os.path.join(base_res_path, 'umamusume')
    path = os.path.join(res_path, 'uma_comic')
    if not os.listdir(path):
        return 'res/img/uma_comic/下没有漫画文件呢，请联系维护组检查'
    file_name = random.choice(os.listdir(path))
    img_path = os.path.join(path, file_name)
    comic_id = file_name.replace('.jpg', '').replace('uma_comic_', '')
    img = await get_img_cq(img_path)
    return f'id: {comic_id}{img}'
