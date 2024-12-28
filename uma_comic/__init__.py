import os

from yuiChyan import LakePermissionException
from yuiChyan.permission import check_permission, SUPERUSER
from yuiChyan.service import Service
from .comic import update_info, get_comic_random, get_comic_id, get_comic_uma
from ..plugin_utils.base_util import get_img_cq

sv = Service('uma_comic')


@sv.on_match('马娘漫画帮助')
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)


@sv.on_prefix('马娘漫画')
async def check_meanings(bot, ev):
    uma_name_tmp = str(ev.message).strip()
    if not uma_name_tmp:
        msg = await get_comic_random()
    elif uma_name_tmp.endswith('号'):
        try:
            comic_id = int(uma_name_tmp.replace('号', ''))
        except:
            return
        msg = await get_comic_id(str(comic_id))
    else:
        msg = await get_comic_uma(uma_name_tmp)
        if not msg:
            return
    await bot.send(ev, msg)


# 手动更新，已存在图片的话会自动跳过
@sv.on_match('手动更新马娘漫画')
async def force_update(bot, ev):
    if not check_permission(ev,  SUPERUSER):
        raise LakePermissionException(ev, None, SUPERUSER)
    await update_info()
    await bot.send(ev, '马娘漫画更新完成')
