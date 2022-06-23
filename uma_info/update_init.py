from ast import Return
import os
import json
import shutil

from .spider import uma_update
from hoshino import logger, R

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
            # 更新失败就回退
            os.remove(current_dir)
            download_path = os.path.join(R.img('umamusume').path, f'base_data/')
            if os.path.exists(download_path):
                shutil.rmtree(download_path)
            logger.error(f'====马娘数据库更新失败：{e}。已回退====')
            return False
    return True

# 自动更新
async def update_info_auto():
    try:
        await uma_update(current_dir)
        logger.info('马娘数据更新完成')
    except Exception as e:
        logger.error(f'马娘数据更新失败{e}')