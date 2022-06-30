import os
import json

from hoshino import logger

current_dir = os.path.join(os.path.dirname(__file__), 'sup_config.json')
current_dir_tw = os.path.join(os.path.dirname(__file__), 'sup_config_tw.json')
async def update():
    if not os.path.exists(current_dir):
        img_dict = {}
        with open(current_dir, 'w', encoding='UTF-8') as f:
            json.dump(img_dict, f, indent=4, ensure_ascii=False)
        logger.info(f'====节奏榜配置文件不存在，现已成功创建====')
    if not os.path.exists(current_dir_tw):
        img_dict = {}
        with open(current_dir_tw, 'w', encoding='UTF-8') as f:
            json.dump(img_dict, f, indent=4, ensure_ascii=False)
        logger.info(f'====台服节奏榜配置文件不存在，现已成功创建====')