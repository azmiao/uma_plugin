import os
import json

from hoshino import logger, R
from .update_skills import update_info, judge_update, del_img

# 启动时自动更新至最新版马娘技能信息
current_dir = os.path.join(os.path.dirname(__file__), f'skills_config.json')
async def update():
    if not os.path.exists(current_dir):
        logger.info('====未检测到马娘技能信息文件，正在开始创建文件和更新信息====')
        img_path = os.path.join(R.img('umamusume').path, f'uma_skills/')
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        init_data = {}
        with open(current_dir, 'w', encoding='UTF-8') as f:
            json.dump(init_data, f, indent=4, ensure_ascii=False)
        try:
            await update_info()
            logger.info('====马娘技能信息更新完成====')
        except Exception as e:
            logger.info(f'====马娘技能信息更新失败：{e}====')

# 自动更新
async def auto_update():
    flag = await judge_update()
    if not flag:
        logger.info('马娘技能没有更新')
        return
    logger.info('马娘技能检测到更新，正在开始更新')
    try:
        await update_info()
        await del_img(R.img('umamusume').path)
        logger.info('马娘技能信息刷新完成')
    except Exception as e:
        logger.error(f'马娘技能信息刷新失败：{e}')