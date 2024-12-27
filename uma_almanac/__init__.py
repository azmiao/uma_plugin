import os
import shutil

from yuiChyan.service import Service
from .get_all_info import judge, get_msg, get_almanac_info

sv = Service('uma_almanac')


@sv.on_match('马娘签到')
async def get_calendar(bot, ev):
    user_id = ev.user_id
    group_id = ev.group_id
    is_get = await judge(group_id, user_id)
    if is_get:
        msg = await get_almanac_info(group_id, user_id)
    else:
        msg = await get_msg(group_id, user_id)
    await bot.send(ev, msg)


# 独立于主服务的自动任务
@sv.scheduled_job(hour='0', minute='00')
async def clean_dir():
    current_dir = os.path.join(os.path.dirname(__file__), f'data')
    if os.path.exists(current_dir):
        shutil.rmtree(current_dir)
        os.mkdir(current_dir)
    else:
        os.mkdir(current_dir)
