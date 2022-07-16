import os

from hoshino import Service, priv
from .face import update_info, get_face_uma, get_face_id, get_face_random, get_mean_id, get_mean_uma

sv = Service('uma_face', help_='![](https://img.gejiba.com/images/ca1e78b1faf8a2a58bfbe62d04cff247.png)')

@sv.on_fullmatch('马娘表情包帮助')
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = f'[CQ:image,file=file:///{os.path.abspath(img_path)}]'
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