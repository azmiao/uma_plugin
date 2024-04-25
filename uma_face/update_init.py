import json
import os

from hoshino import logger

from .face import update_info, get_img_dict


# 首次启动函数
async def update():
    current_dir = os.path.join(os.path.dirname(__file__), f'img_config.json')
    if not os.path.exists(current_dir):
        logger.info('====未检测到马娘表情包信息，正在开始更新====')
        await update_info()
        logger.info('====马娘表情包信息更新完成====')


# 自动对比是否有更新，有更新就更新，没有就跳过，但目前不能自动匹配这张表情包是哪个角色
async def auto_update():
    img_dict = await get_img_dict()
    current_dir = os.path.join(os.path.dirname(__file__), f'img_config.json')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        img_data = json.load(f)
    if len(list(img_dict.keys())) > len(list(img_data.keys())):
        logger.info('马娘表情包检测到更新，正在开始更新')
        await update_info()
    else:
        logger.info('马娘表情包已是最新')
