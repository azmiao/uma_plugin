import json
import os
import random

import httpx
from bs4 import BeautifulSoup

from yuiChyan import logger, base_res_path
from ..plugin_utils.base_util import get_img_cq
from ..uma_info.info_utils import *


async def update_info():
    img_dict = await get_img_dict()
    for img_id in list(img_dict.keys()):
        await download_img(img_id, img_dict[img_id]['url'])
    await create_config(img_dict)


# 获取表情包的url字典
async def get_img_dict():
    url = 'https://wiki.biligame.com/umamusume/表情包'
    res = httpx.get(url, timeout=15)
    soup = BeautifulSoup(res.text, 'lxml')
    img_dict = {}
    all_gallery = soup.find('ul', {"class": "gallery mw-gallery-traditional"}).find_all('img')
    for gallery in all_gallery:
        img_id = gallery.get('alt').replace('.png', '')
        img_dict[img_id] = {}
        img_dict[img_id]['url'] = gallery.get('src')
    return img_dict


# 创建json配置文件
async def create_config(img_dict):
    current_dir_tmp = os.path.join(os.path.dirname(__file__), f'face_info.json')
    with open(current_dir_tmp, 'r', encoding='UTF-8') as f:
        mean_data = json.load(f)
    for img_id in list(img_dict.keys()):
        if img_id in list(mean_data.keys()):
            img_dict[img_id]['en_name'] = mean_data[img_id]['en_name']
            img_dict[img_id]['meanings'] = mean_data[img_id]['meanings']
        else:
            img_dict[img_id]['en_name'] = ''
            img_dict[img_id]['meanings'] = ''
    current_dir = os.path.join(os.path.dirname(__file__), f'img_config.json')
    with open(current_dir, 'w', encoding='UTF-8') as af:
        # noinspection PyTypeChecker
        json.dump(img_dict, af, indent=4, ensure_ascii=False)


# 下载图片
async def download_img(face_id, url):
    res_path = os.path.join(base_res_path, 'umamusume')
    img_path = os.path.join(res_path, 'uma_face')
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    current_dir = os.path.join(img_path, f'{face_id}.png')
    if not os.path.exists(current_dir):
        response = httpx.get(url, timeout=10)
        with open(current_dir, 'wb') as f:
            f.write(response.read())
        logger.info(f'未检测到马娘表情包 {face_id}.png ，现已下载成功')
    else:
        logger.info(f'检测到马娘表情包 {face_id}.png 已存在，将不会重新下载')


async def get_uma_id(name_tmp):
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info')
    current_dir = os.path.join(config_dir, 'config_v2.json')
    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    rep_dir = os.path.join(config_dir, 'replace_dict.json')
    with open(rep_dir, 'r', encoding='UTF-8') as file:
        replace_data = json.load(file)

    uma = await query_uma_by_name(name_tmp, f_data, replace_data)
    return uma.id if uma else None


# 按马娘名字的表情包
async def get_face_uma(uma_name_tmp):
    uma_id = await get_uma_id(uma_name_tmp)
    if not uma_id:
        return ''
    res_path = os.path.join(base_res_path, 'umamusume')
    path = os.path.join(res_path, 'uma_face')
    current_dir = os.path.join(os.path.dirname(__file__), f'img_config.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        img_data = json.load(f)
    for face_id in list(img_data.keys()):
        if img_data[face_id]['en_name'] == uma_id:
            img_path = os.path.join(path, f'{face_id}.png')
            # 当文件丢失就重新下载
            if not os.path.exists(img_path):
                url = img_data[face_id]['url']
                await download_img(face_id, url)
            face_id = str(int(face_id) - 100000)
            img = await get_img_cq(img_path)
            msg = f'> Face Id: {face_id}{img}'
            return msg
    return ''


# 按编号的表情包
async def get_face_id(face_id):
    res_path = os.path.join(base_res_path, 'umamusume')
    path = os.path.join(res_path, 'uma_face')
    img_path = os.path.join(path, f'{face_id}.png')
    if not os.path.exists(img_path):
        length = len(os.listdir(path))
        return f'此编号的表情包不存在哦，目前有的编号范围为 1 到 {length}'
    msg = await get_img_cq(img_path)
    return msg


# 随机表情包
async def get_face_random():
    res_path = os.path.join(base_res_path, 'umamusume')
    path = os.path.join(res_path, 'uma_face')
    if not os.listdir(path):
        return 'res/img/uma_face/下没有表情包文件呢，请联系维护组检查'
    file_name = random.choice(os.listdir(path))
    img_path = os.path.join(path, file_name)
    face_id = file_name.replace('.png', '')
    face_id = str(int(face_id) - 100000)
    img = await get_img_cq(img_path)
    return f'> Face Id: {face_id}{img}'


# 按编号查含义
async def get_mean_id(face_id):
    current_dir = os.path.join(os.path.dirname(__file__), f'img_config.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        img_data = json.load(f)
    if face_id not in list(img_data.keys()):
        length = len(list(img_data.keys()))
        return f'此编号的表情包不存在哦，目前有的编号范围为 1 到 {length}'
    meanings = img_data[face_id]['meanings']
    face_id = str(int(face_id) - 100000)
    msg = f'> Face Id: {face_id} 表情包的含义是：\n{meanings}'
    return msg


# 按马娘名字查含义
async def get_mean_uma(uma_name_tmp):
    uma_id = await get_uma_id(uma_name_tmp)
    if not uma_id:
        return ''
    current_dir = os.path.join(os.path.dirname(__file__), f'img_config.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        img_data = json.load(f)
    for face_id in list(img_data.keys()):
        en_name = img_data[face_id]['en_name']
        if en_name == uma_id:
            meanings = img_data[face_id]['meanings']
            face_id = str(int(face_id) - 100000)
            msg = f'> Face Id: {face_id} 表情包的含义是：\n{meanings}'
            return msg
    return ''
