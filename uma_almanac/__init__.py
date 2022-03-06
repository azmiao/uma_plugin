from hoshino import Service
import shutil
import os
from .get_all_info import *

sv = Service('uma_almanac', bundle='马娘黄历')

@sv.on_fullmatch('马娘签到')
async def get_calendar(bot, ev):
    user_id = ev.user_id
    group_id = ev.group_id
    is_get = judge(group_id, user_id)
    if is_get:
        msg = '你今天已经签到过啦！'
    else:
        msg = get_msg(group_id, user_id)
    await bot.send(ev, msg)

@sv.scheduled_job('cron', hour='0', minute='00')
async def clean_dir():
    current_dir = os.path.join(os.path.dirname(__file__), f'data')
    if os.path.exists(current_dir):
        shutil.rmtree(current_dir)  #删除目录，包括目录下的所有文件
        os.mkdir(current_dir)
    else:
        os.mkdir(current_dir)