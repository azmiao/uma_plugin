import asyncio
import base64
import json
import os

from yuiChyan.resources import base_res_path
from yuiChyan.service import Service
from .plugin_utils.base_util import get_img_cq, get_interval
from .plugin_utils.plugin_update import init_plugin, plugin_update_auto
from .uma_comic.update_init import update as comic_update, auto_update as comic_auto
from .uma_compatibility.update_init import update as com_update, auto_update as com_auto
from .uma_face.update_init import update as face_update, auto_update as face_auto
from .uma_gacha_v2.update_init import update as gacha_update, auto_update as gacha_auto
from .uma_info.update_init import update as info_update, update_info_auto as info_auto
from .uma_skills.update_init import update as skills_update, auto_update as skills_auto
from .uma_support_chart.update_init import update as sup_update
from .uma_tasks.update_init import update as tasks_update, auto_update as tasks_auto

sv = Service('uma_help')
with open(os.path.join(os.path.dirname(__file__), f'{sv.name}.png'), 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
sv.help = f'![](data:image/jpeg;base64,{s})'


@sv.on_match('马娘帮助')
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)


@sv.on_match(('马娘插件-v', '马娘插件-version'))
async def get_plugin_version(bot, ev):
    version_path = os.path.join(os.path.dirname(__file__), 'version.json')
    with open(version_path, 'r', encoding="UTF-8") as file:
        version_data = json.load(file)
    version = version_data['version']
    commit_time = version_data['commit_time']
    msg = f'【马娘插件】\n基础版本：{version}\n更新时间：{commit_time}'
    await bot.send(ev, msg)


# 马娘速查，一些支援卡对比的子网站就不列举了，去百科里找就行了
@sv.on_match('马娘速查')
async def uma_query(bot, ev):
    query_path = os.path.join(os.path.dirname(__file__), 'query_data.json')
    with open(query_path, 'r', encoding='UTF-8') as file:
        query_data = json.load(file)
    msg = '◎赛马娘常用网站◎'
    for title in list(query_data.keys()):
        msg += '\n' + title + '：' + query_data[title]
    await bot.send(ev, msg)


# 资源文件夹
res_path = os.path.join(base_res_path, 'umamusume')
if not os.path.exists(res_path):
    os.mkdir(res_path)


# v1.8将首次启动事件合并到一块，防止首次启动时过多线程同时工作导致触发反爬虫
async def update():
    sv.logger.info('【马娘插件】启动时检查更新...')
    try:
        await init_plugin(False)
    except:
        sv.logger.error('马娘插件版本获取失败，插件部分功能已停止启动！请检查是否能访问Github，如不能请设置代理或者关闭插件自动更新功能，重启生效')
    await asyncio.sleep(0.1)
    flag = await info_update()
    if not flag:
        sv.logger.error('马娘基础数据库更新失败，后续部分更新操作已停止，请重新启动Bot更新')
    await asyncio.sleep(0.1)
    await comic_update()
    await asyncio.sleep(0.1)
    await com_update()
    await asyncio.sleep(0.1)
    await face_update()
    await asyncio.sleep(0.1)
    await skills_update()
    await asyncio.sleep(0.1)
    await tasks_update()
    await asyncio.sleep(0.1)
    await sup_update()
    await asyncio.sleep(0.1)
    await gacha_update()
    sv.logger.info('【马娘插件】更新检查完成...')


loop = asyncio.get_event_loop()
loop.run_until_complete(update())


# 部分统一自动更新时间点
@sv.scheduled_job(day=f'1/{get_interval()}', hour='2', minute='30')
async def auto_update():
    await plugin_update_auto()
    await asyncio.sleep(0.1)
    _ = await info_auto()
    await asyncio.sleep(0.1)
    await comic_auto()
    await asyncio.sleep(0.1)
    await com_auto()
    await asyncio.sleep(0.1)
    await face_auto()
    await asyncio.sleep(0.1)
    await gacha_auto()


# 其他每小时自动对比是否有更新
@sv.scheduled_job(hour='0-23', minute='00')
async def auto_update_per():
    await skills_auto()
    await asyncio.sleep(0.1)
    await tasks_auto()
