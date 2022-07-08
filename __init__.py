import os
import shutil
import asyncio

from hoshino import Service, R, logger

from .uma_comic.update_init import update as comic_update, auto_update as comic_auto
from .uma_compatibility.update_init import update as com_update, auto_update as com_auto
from .uma_face.update_init import update as face_update, auto_update as face_auto
from .uma_info.update_init import update as info_update, update_info_auto as info_auto
from .uma_skills.update_init import update as skills_update, auto_update as skills_auto
from .uma_tasks.update_init import update as tasks_update, auto_update as tasks_auto
from .uma_gacha.update_init import update as gacha_update, auto_update as gacha_auto
from .uma_support_chart.update_init import update as sup_update

sv_help = '''
马娘相关功能命令列表：

马娘签到
马娘数据帮助
支援卡节奏榜帮助
马娘新闻帮助
马娘抽卡帮助
马娘耐力帮助
马娘相性帮助
马娘表情包帮助
马娘漫画帮助
马娘限时任务帮助
马娘技能帮助
育成目标帮助

注：数据来自马娘官网和Bwiki
'''.strip()

sv = Service('uma_help', help_ = sv_help)

@sv.on_fullmatch('马娘帮助')
async def get_help(bot, ev):
    await bot.send(ev, sv_help)

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
@sv.scheduled_job('cron', hour='2', minute='30')
async def auto_update():
    flag = await info_auto()
    await asyncio.sleep(0.1)
    await comic_auto()
    await asyncio.sleep(0.1)
    await com_auto()
    await asyncio.sleep(0.1)
    await face_auto()
    await asyncio.sleep(0.1)
    await gacha_auto()

# 其他每小时自动对比是否有更新
@sv.scheduled_job('cron', hour='0-23', minute='00')
async def auto_update_per():
    await skills_auto()
    await asyncio.sleep(0.1)
    await tasks_auto()