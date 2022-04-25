import os
import json

from .spider import uma_update
from hoshino import logger

# 启动时自动更新至最新版马娘技能信息
current_dir = os.path.join(os.path.dirname(__file__), 'config.json')
async def update():
    if not os.path.exists(current_dir):
        logger.info('====未检测到马娘数据库文件，正在开始创建文件和更新信息====')
        init_data = {}
        with open(current_dir, 'w', encoding='UTF-8') as f:
            json.dump(init_data, f, indent=4, ensure_ascii=False)
        try:
            await uma_update(current_dir)
            logger.info('====马娘数据库更新完成====')
        except Exception as e:
            logger.info(f'====马娘数据库更新失败：{e}====')

# 自动更新
async def update_info_auto():
    try:
        await uma_update(current_dir)
        logger.info('马娘数据更新完成')
    except Exception as e:
        logger.info(f'马娘数据更新失败{e}')