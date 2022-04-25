import os
import json

from hoshino import logger, R
from .update_tasks import del_img, update_info, judge_update, del_img

# 启动时自动更新至最新版限时任务信息
current_dir = os.path.join(os.path.dirname(__file__), f'tasks_config.json')
async def update():
    if not os.path.exists(current_dir):
        logger.info('====未检测到马娘限时任务信息文件，正在开始创建文件和更新信息====')
        init_data = {}
        with open(current_dir, 'w', encoding='UTF-8') as f:
            json.dump(init_data, f, indent=4, ensure_ascii=False)
        try:
            await update_info()
            logger.info('====限时任务信息更新完成====')
        except Exception as e:
            logger.info(f'====限时任务信息更新失败：{e}====')

async def auto_update():
    flag = await judge_update()
    if not flag:
        logger.info('马娘限时任务没有更新')
        return
    logger.info('马娘限时任务检测到更新，正在开始更新')
    try:
        await update_info()
        await del_img(R.img('umamusume').path)
        logger.info('限时任务信息刷新完成')
    except Exception as e:
        logger.error(f'限时任务信息刷新失败：{e}')