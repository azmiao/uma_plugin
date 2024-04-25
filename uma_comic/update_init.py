import json
import os

from hoshino import logger

from .comic import update_info, get_img_dict
from ..plugin_utils.base_util import delete_file


# 首次启动函数
async def update():
    old_file = os.path.join(os.path.dirname(__file__), f'comic_config.json')
    current_dir = os.path.join(os.path.dirname(__file__), f'comic_config_v2.json')
    if os.path.exists(old_file):
        await delete_file(old_file)
    if not os.path.exists(current_dir):
        logger.info('====未检测到马娘漫画信息，正在开始更新====')
        await update_info()
        logger.info('====马娘漫画信息更新完成====')


# 自动对比是否有更新，有更新就更新，没有就跳过
async def auto_update():
    img_dict = await get_img_dict()
    current_dir = os.path.join(os.path.dirname(__file__), f'comic_config_v2.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        img_data = json.load(f)
    if len(img_dict) > len(img_data):
        logger.info('马娘漫画检测到更新，正在开始更新')
        await update_info()
    else:
        logger.info('马娘漫画已是最新')
