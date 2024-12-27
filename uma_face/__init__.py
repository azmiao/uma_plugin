import os

from yuiChyan import LakePermissionException
from yuiChyan.permission import check_permission, SUPERUSER
from yuiChyan.service import Service
from .face import update_info, get_face_uma, get_face_id, get_face_random, get_mean_id, get_mean_uma
from ..plugin_utils.base_util import get_img_cq

sv = Service('uma_face')


@sv.on_match('马娘表情包帮助')
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)


# 支持1到10个字符的马娘名字
@sv.on_rex(r'^(\S{1,10})表情包$')
async def get_uma_face(bot, ev):
    uma_name_tmp = ev['match'].group(1).strip()
    if uma_name_tmp == '马娘':
        msg = await get_face_random()
    elif uma_name_tmp.endswith('号'):
        try:
            face_id = int(uma_name_tmp.replace('号', ''))
        except:
            return
        msg = await get_face_id(str(face_id + 100000))
    else:
        msg = await get_face_uma(uma_name_tmp)
        if not msg:
            return
    await bot.send(ev, msg)


@sv.on_prefix(('查表情包含义', '查表情包涵义'))
async def check_meanings(bot, ev):
    uma_name_tmp = str(ev.message).strip()
    if uma_name_tmp.endswith('号'):
        try:
            face_id = int(uma_name_tmp.replace('号', ''))
        except:
            return
        msg = await get_mean_id(str(face_id + 100000))
    else:
        msg = await get_mean_uma(uma_name_tmp)
        if not msg:
            return
    await bot.send(ev, msg)


# 手动更新，已存在图片的话会自动跳过
@sv.on_match('手动更新马娘表情包')
async def force_update(bot, ev):
    if not check_permission(ev,  SUPERUSER):
        raise LakePermissionException(ev, None, SUPERUSER)
    await update_info()
    await bot.send(ev, '马娘表情包更新完成')
