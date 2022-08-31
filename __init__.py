import os
import shutil
import asyncio
import json

from hoshino import Service, R, logger
from .plugin_utils.base_util import get_img_cq, get_interval
from .plugin_utils.plugin_update import init_plugin, plugin_update_auto

from .uma_comic.update_init import update as comic_update, auto_update as comic_auto
from .uma_compatibility.update_init import update as com_update, auto_update as com_auto
from .uma_face.update_init import update as face_update, auto_update as face_auto
from .uma_info.update_init import update as info_update, update_info_auto as info_auto
from .uma_skills.update_init import update as skills_update, auto_update as skills_auto
from .uma_tasks.update_init import update as tasks_update, auto_update as tasks_auto
from .uma_gacha_v2.update_init import update as gacha_update, auto_update as gacha_auto
from .uma_support_chart.update_init import update as sup_update

sv = Service('uma_help', help_='![](https://img.gejiba.com/images/1d987330ad0a9e041321cdf433e5c7c4.png)')

@sv.on_fullmatch('马娘帮助')
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)

@sv.on_fullmatch(('马娘插件-v', '马娘插件-version'))
async def get_plugin_version(bot, ev):
    version_path = os.path.join(os.path.dirname(__file__), 'version.json')
    with open(version_path, 'r', encoding="UTF-8") as f:
        version_data = json.load(f)
    version = version_data['version']
    commit_time = version_data['commit_time']
    msg = f'【马娘插件】\n基础版本：{version}\n更新时间：{commit_time}'
    await bot.send(ev, msg)

# 马娘速查，一些支援卡对比的子网站就不列举了，去百科里找就行了
@sv.on_fullmatch('马娘速查')
async def uma_query(bot, ev):
    query_path = os.path.join(os.path.dirname(__file__), 'query_data.json')
    with open(query_path, 'r', encoding='UTF-8') as f:
        query_data = json.load(f)
    msg = '◎赛马娘常用网站◎'
    for title in list(query_data.keys()):
        msg += '\n' + title + '：' + query_data[title]
    await bot.send(ev, msg)

# v1.5.2将图片文件夹合并至一个文件夹
root_path = R.img('umamusume').path
def move_dir(dir_name):
    if os.path.exists(R.img(dir_name).path):
        shutil.move(os.path.abspath(R.img(dir_name).path), os.path.abspath(root_path))
if not os.path.exists(root_path):
    os.mkdir(root_path)
    move_dir('uma_bir')
    move_dir('uma_comic')
    move_dir('uma_face')
    move_dir('uma_support_chart')
    move_dir('uma_voice')
    move_dir('umamusume_news')
# 这样独立版马娘抽卡删除后再装本整合版可以通用
move_dir('uma_gacha')

# v1.8将首次启动事件合并到一块，防止首次启动时过多线程同时工作导致触发反爬虫
async def update():
    await init_plugin()
    await asyncio.sleep(0.1)
    flag = await info_update()
    if not flag:
        logger.info('马娘基础数据库更新失败，后续更新操作已停止，请重新启动Bot更新')
        return
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

loop = asyncio.get_event_loop()
loop.run_until_complete(update())

# 部分统一自动更新时间点
@sv.scheduled_job('cron',id='daily_uma_res', day=f'1/{get_interval()}', hour='2', minute='30')
async def auto_update():
    _ = await info_auto()
    await asyncio.sleep(0.1)
    await comic_auto()
    await asyncio.sleep(0.1)
    await com_auto()
    await asyncio.sleep(0.1)
    await face_auto()
    await asyncio.sleep(0.1)
    await gacha_auto()
    await asyncio.sleep(0.1)
    await plugin_update_auto()

# 其他每小时自动对比是否有更新
@sv.scheduled_job('cron',id='hourly_uma_res', hour='0-23', minute='00')
async def auto_update_per():
    await skills_auto()
    await asyncio.sleep(0.1)
    await tasks_auto()