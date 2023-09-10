import base64
import os

from hoshino import Service

from .get_url import generate_img
from ..plugin_utils.base_util import get_img_cq, get_server_default

sv = Service('uma_support_chart')
with open(os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png'), 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
sv.help = f'![](data:image/jpeg;base64,{s})'


# 帮助界面
@sv.on_fullmatch("支援卡节奏榜帮助")
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)


@sv.on_rex(r'^(\S服)?(\S{1,2})卡节奏榜$')
async def ssr_speed_chart(bot, ev):
    sup_type = ev['match'].group(2)
    if sup_type not in ['速', '耐', '力', '根', '智', '友人']:
        return
    default_server = await get_server_default()
    try:
        if not ev['match'].group(1):
            if default_server == 'jp':
                msg = await generate_img(sup_type, '日服')
            elif default_server == 'tw':
                msg = await generate_img(sup_type, '繁中服')
            elif default_server == 'bili':
                msg = await generate_img(sup_type, '简中服')
            else:
                msg = f'该服务器"{default_server}"暂未支持节奏榜'
        else:
            if ev['match'].group(1) == '日服':
                msg = await generate_img(sup_type, '日服')
            elif ev['match'].group(1) in ['台服', '繁中服']:
                msg = await generate_img(sup_type, '繁中服')
            elif ev['match'].group(1) in ['b服', 'B服', '国服', '简中服']:
                msg = await generate_img(sup_type, '简中服')
            else:
                msg = f'该服务器"{ev["match"].group(1)}"暂未支持节奏榜'
    except AttributeError:
        msg = f'{sup_type}卡节奏榜获取失败，请检查节奏榜页面是否有图片或联系维护组反馈BUG'
        sv.logger.error(msg)
    await bot.send(ev, msg)
