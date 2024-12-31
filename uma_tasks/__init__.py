import json
import os

from yuiChyan import LakePermissionException
from yuiChyan.permission import check_permission, SUPERUSER
from yuiChyan.service import Service
from .generate import get_title, get_task_info
from .update_tasks import del_img, update_info, del_img
from ..plugin_utils.base_util import get_img_cq

current_dir = os.path.join(os.path.dirname(__file__), f'tasks_config.json')

sv = Service('uma_tasks')


@sv.on_match('马娘限时任务帮助')
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)


@sv.on_rex(r'^限时任务(\S{1,3})$')
async def check_meanings(bot, ev):
    task_id = ev['match'].group(1)
    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    if task_id == '列表':
        task_list = []
        for task_id_tmp in list(f_data['tasks'].keys()):
            title = f_data['tasks'][task_id_tmp]['title']
            task_list.append(title)
        msg = await get_title(f_data)
        await bot.send(ev, msg)
        return
    try:
        task_id = int(task_id)
    except:
        return
    number = int(f_data['number'])
    if task_id not in range(1, number + 1):
        await bot.send(ev, f'未找到此编号的限时任务：{task_id}\n目前支持 1-{number}')
        return
    msg = await get_task_info(str(task_id), f_data)
    await bot.send(ev, msg)


# 手动更新本地数据
@sv.on_match('手动更新限时任务')
async def force_update(bot, ev):
    if not check_permission(ev,  SUPERUSER):
        raise LakePermissionException(ev, None, SUPERUSER)
    try:
        await update_info()
        await del_img()
        await bot.send(ev, '限时任务信息刷新完成')
    except Exception as e:
        await bot.send(ev, f'限时任务信息刷新失败：{e}')
