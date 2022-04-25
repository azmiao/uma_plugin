import os
import json

from hoshino import Service, priv, R
from .update_tasks import del_img, update_info, del_img
from .generate import get_title, get_task_info

current_dir = os.path.join(os.path.dirname(__file__), f'tasks_config.json')

sv_help = '''=====功能=====
[限时任务列表] 查看所有的限定任务标题对应编号

[限时任务x] x为列表中的编号，查看限时任务的内容

[手动更新限时任务] 强制刷新列表，限维护组
'''.strip()

sv = Service('uma_tasks')

@sv.on_fullmatch('马娘限时任务帮助')
async def get_help(bot, ev):
    await bot.send(ev, sv_help)

@sv.on_rex(r'^限时任务(\S{1,3})$')
async def check_meanings(bot, ev):
    task_id = ev['match'].group(1)
    with open(current_dir, 'r', encoding='UTF-8') as f:
        f_data = json.load(f)
    if task_id == '列表':
        task_list = []
        for task_id_tmp in list(f_data['tasks'].keys()):
            title = f_data['tasks'][task_id_tmp]['title']
            task_list.append(title)
        msg = await get_title(f_data)
        await bot.finish(ev, msg)
    try:
        task_id = int(task_id)
    except:
        return
    number = int(f_data['number'])
    if task_id not in range(1, number+1):
        await bot.finish(ev, f'未找到此编号的限时任务：{task_id}\n目前支持 1-{number}')
    msg = await get_task_info(str(task_id), f_data)
    await bot.send(ev, msg)

# 手动更新本地数据
@sv.on_fullmatch('手动更新限时任务')
async def force_update(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.send(ev, msg)
        return
    try:
        await update_info()
        await del_img(R.img('umamusume').path)
        await bot.send(ev, '限时任务信息刷新完成')
    except Exception as e:
        await bot.send(ev, f'限时任务信息刷新失败：{e}')