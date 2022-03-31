import os
import json
import asyncio

from hoshino import Service, priv
from .face import update_info, get_face_uma, get_face_id, get_face_random, get_imgurl, create_config, \
    download_img, get_mean_id, get_mean_uma

# 启动时该干的事
current_dir = os.path.join(os.path.dirname(__file__), f'img_config.json')
if not os.path.exists(current_dir):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_info())

sv_help = '''=====功能=====
[马娘表情包] 随机一张马娘游戏内的表情包

[xxx表情包] xxx为角色名字，没有该角色的表情包就不会有反应

[x号表情包] x为数字，是表情包的编号，编号不是整数就不会有反应

[查表情包含义 xxx] xxx为角色名字，没有该角色的表情包就不会有反应

[查表情包含义 x号] x为数字，是表情包的编号，编号不是整数就不会有反应
'''.strip()

sv = Service('uma_face', help_ = sv_help)

@sv.on_fullmatch('马娘表情包帮助')
async def get_help(bot, ev):
    await bot.send(ev, sv_help)

# 支持1到10个字符的马娘名字
@sv.on_rex(r'^(\S{1,10})表情包$')
async def get_umaface(bot, ev):
    uma_name_tmp = ev['match'].group(1)
    if uma_name_tmp == '马娘':
        msg = await get_face_random()
    elif uma_name_tmp.endswith('号'):
        try:
            id = int(uma_name_tmp.replace('号', ''))
        except:
            id = 0
            return
        msg = await get_face_id(str(id+100000))
    else:
        msg = await get_face_uma(uma_name_tmp)
        if not msg:
            return
    await bot.send(ev, msg)

@sv.on_prefix(('查表情包含义', '查表情包涵义'))
async def check_meanings(bot, ev):
    uma_name_tmp = str(ev.message)
    if uma_name_tmp.endswith('号'):
        try:
            id = int(uma_name_tmp.replace('号', ''))
        except:
            id = 0
            return
        msg = await get_mean_id(str(id+100000))
    else:
        msg = await get_mean_uma(uma_name_tmp)
        if not msg:
            return
    await bot.send(ev, msg)

# 手动更新，已存在图片的话会自动跳过
@sv.on_fullmatch('手动更新马娘表情包')
async def force_update(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.send(ev, msg)
        return
    await update_info()
    await bot.send(ev, '马娘表情包更新完成')

# 自动对比是否有更新，有更新就更新，没有就跳过，但目前不能自动匹配这张表情包是哪个角色
@sv.scheduled_job('cron', hour='4', minute='01')
async def auto_update():
    img_dict = await get_imgurl()
    current_dir = os.path.join(os.path.dirname(__file__), f'img_config.json')
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        img_data = json.load(f)
    if len(list(img_dict.keys())) > len(list(img_data.keys())):
        sv.logger.info('马娘表情包检测到更新，正在开始更新')
        for id in list(img_dict.keys()):
            # 只更新没有下载的表情包
            if id not in list(img_data.keys()):
                await download_img(id, img_dict[id]['url'])
        await create_config(img_dict)
    else:
        sv.logger.info('马娘表情包已是最新')
