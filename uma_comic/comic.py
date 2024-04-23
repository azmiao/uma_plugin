import json
import os
import random
import re

import hoshino
import httpx
from bs4 import BeautifulSoup
from hoshino import R

from ..plugin_utils.base_util import get_img_cq
from ..uma_info.info_utils import *


async def update_info():
    img_dict = await get_img_url()
    for img_id in list(img_dict.keys()):
        await download_img(img_id, img_dict[img_id]['url'])
    await create_config(img_dict)


# 获取漫画的url字典
async def get_img_url():
    url = 'https://wiki.biligame.com/umamusume/1格漫画'
    res = httpx.get(url, timeout=15)
    soup = BeautifulSoup(res.text, 'lxml')
    img_dict = {}
    all_gallery = soup.find('ul', {"class": "gallery mw-gallery-slideshow"}).find_all('img')
    img_id = 1
    for gallery in all_gallery:
        img_name = gallery.get('alt').replace('.jpg', '').replace('.png', '').replace('一格', '')
        img_id = str(img_id)
        img_dict[img_id] = {}
        img_dict[img_id]['url'] = await adjust_url(gallery.get('src'))
        en_name = await get_en_name(img_name)
        img_dict[img_id]['en_name'] = en_name
        img_id = int(img_id)
        img_id += 1
    return img_dict


# 调整url
async def adjust_url(url):
    url_pattern = re.compile(r'https://patchwiki\.biligame\.com/images/umamusume\S+?(/\S+?\.(jpg|png))')
    url_g = re.match(url_pattern, url)
    url = url_g.group(0).replace('/thumb', '')
    return url


# 创建json配置文件
async def create_config(img_dict):
    current_dir = os.path.join(os.path.dirname(__file__), f'comic_config.json')
    with open(current_dir, 'w', encoding='UTF-8') as af:
        json.dump(img_dict, af, indent=4, ensure_ascii=False)


# 下载图片
async def download_img(comic_id, url):
    img_path = os.path.join(R.img('umamusume').path, 'uma_comic')
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    current_dir = os.path.join(img_path, f'uma_comic_{comic_id}.jpg')
    if not os.path.exists(current_dir):
        response = httpx.get(url, timeout=10)
        with open(current_dir, 'wb') as f:
            f.write(response.read())
        hoshino.logger.info(f'未检测到马娘漫画 uma_comic_{comic_id}.jpg ，现已下载成功')
    else:
        hoshino.logger.info(f'检测到马娘漫画 uma_comic_{comic_id}.jpg 已存在，将不会重新下载')


# 获取英文名
async def get_en_name(name_tmp):
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info')
    current_dir = os.path.join(config_dir, 'config_v2.json')
    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    rep_dir = os.path.join(config_dir, 'replace_dict.json')
    with open(rep_dir, 'r', encoding='UTF-8') as file:
        replace_data = json.load(file)

    uma = await query_uma_by_name(name_tmp, f_data, replace_data)
    return uma.en


# 按马娘名字的漫画
async def get_comic_uma(uma_name_tmp):
    uma_name = await get_en_name(uma_name_tmp)
    if not uma_name:
        return ''
    path = os.path.join(R.img('umamusume').path, 'uma_comic')
    current_dir = os.path.join(os.path.dirname(__file__), f'comic_config.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        img_data = json.load(f)
    for comic_id in list(img_data.keys()):
        if img_data[comic_id]['en_name'] == uma_name:
            img_path = os.path.join(path, f'uma_comic_{comic_id}.jpg')
            # 当文件丢失就重新下载
            if not os.path.exists(img_path):
                url = img_data[comic_id]['url']
                await download_img(comic_id, url)
            img = await get_img_cq(img_path)
            msg = f'id: {comic_id}{img}'
            return msg
    return ''


# 按编号的漫画
async def get_comic_id(comic_id):
    path = os.path.join(R.img('umamusume').path, 'uma_comic')
    img_path = os.path.join(path, f'uma_comic_{comic_id}.jpg')
    if not os.path.exists(img_path):
        length = len(os.listdir(path))
        return f'此编号的漫画不存在哦，目前有的编号范围为 1 到 {length}'
    msg = await get_img_cq(img_path)
    return msg


# 随机漫画
async def get_comic_random():
    path = os.path.join(R.img('umamusume').path, 'uma_comic')
    if not os.listdir(path):
        return 'res/img/uma_comic/下没有漫画文件呢，请联系维护组检查'
    file_name = random.choice(os.listdir(path))
    img_path = os.path.join(path, file_name)
    comic_id = file_name.replace('.jpg', '').replace('uma_comic_', '')
    img = await get_img_cq(img_path)
    return f'id: {comic_id}{img}'
