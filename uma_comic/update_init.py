import os
import json

from hoshino import logger
from .comic import update_info, get_img_url, create_config, download_img


# 首次启动函数
async def update():
    current_dir = os.path.join(os.path.dirname(__file__), f'comic_config.json')
    if not os.path.exists(current_dir):
        logger.info('====未检测到马娘漫画信息，正在开始更新====')
        await update_info()
        logger.info('====马娘漫画信息更新完成====')


# 自动对比是否有更新，有更新就更新，没有就跳过
async def auto_update():
    img_dict = await get_img_url()
    current_dir = os.path.join(os.path.dirname(__file__), f'comic_config.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        img_data = json.load(f)
    if len(list(img_dict.keys())) > len(list(img_data.keys())):
        logger.info('马娘漫画检测到更新，正在开始更新')
        for comic_id in list(img_dict.keys()):
            # 只更新没有下载的漫画
            if comic_id not in list(img_data.keys()):
                await download_img(comic_id, img_dict[comic_id]['url'])
        await create_config(img_dict)
    else:
        logger.info('马娘漫画已是最新')
