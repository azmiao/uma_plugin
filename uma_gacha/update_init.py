import os
import json
import re
import datetime

from .config import check_config
from .pretty_handle import update_pretty_info, reload_pretty_pool
from .async_update_game_info import async_update_game
from .util import _check_dir

import hoshino
from hoshino import R, logger

# 首次启动函数
async def update():
    DRAW_PATH = os.path.join(R.img('umamusume').path, 'uma_gacha/')
    if not os.path.exists(DRAW_PATH):
        os.mkdir(f'{DRAW_PATH}')
        os.mkdir(f'{DRAW_PATH}/draw_card')
        os.mkdir(f'{DRAW_PATH}/draw_card/pretty')
        os.mkdir(f'{DRAW_PATH}/draw_card_up')
    check_config()
    logger.info('====正在检测马娘抽卡信息====')
    await async_update_game()
    _check_dir()
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'char_atlas.txt')):
        logger.info('马娘卡池信息不存在，正在重新生成...')
        try:
            await update_pretty_info()
            logger.info('马娘卡池信息更新完成')
        except Exception as e:
            logger.info(f'马娘卡池信息失败：{e}')
    logger.info('====马娘抽卡信息更新完成====')

# 自动检测是否有更新，若有则自动更新赛马娘up卡池
async def auto_update():
    logger.info('开始检测马娘卡池是否有更新')
    draw_path = os.path.join(R.img('umamusume').path, 'uma_gacha/')
    with open(f'{draw_path}/draw_card_up/pretty_up_char.json', encoding='UTF-8') as f:
        data = json.load(f)
    up_time = str(data['char']['time'])
    end_time = re.search(r'- (\d{1,2})月(\d{1,2})日', up_time)
    now_time = datetime.datetime.now()
    startTime = datetime.datetime(int(now_time.year), int(end_time.group(1)), int(end_time.group(2))+1, 2, 30, 0)
    if now_time < startTime:
        logger.info(f'未检测到更新！当前池子结束时间：{str(now_time.year)}年{str(end_time.group(1))}月{str(end_time.group(2))}日 11:00')
        return
    bot = hoshino.get_bot()
    superid = hoshino.config.SUPERUSERS[0]
    logger.info('检测到更新！正在更新赛马娘信息和up卡池')
    try:
        await update_pretty_info()
        _ = await reload_pretty_pool()
    except Exception as e:
        logger.info(f'自动更新赛马娘信息和up卡池失败，{e}')
        msg = f'自动更新赛马娘信息和up卡池失败，{e}'
        msg = msg + '\n可能是公告界面布局变动导致，请先使用命令“更新马娘信息”手动更新查看报错日志然后反馈，或等待插件更新，一般来说插件更新的还是蛮勤快的'
        await bot.send_private_msg(user_id=superid, message=msg)
        return
    logger.info('自动更新赛马娘信息和up卡池成功')
    msg = '自动更新赛马娘信息和up卡池成功'
    await bot.send_private_msg(user_id=superid, message=msg)