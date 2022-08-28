import os

from .get_url import generate_img
from .get_url_tw import generate_img_tw
from hoshino import Service
from ..plugin_utils.base_util import get_img_cq, get_server_default

sv = Service('uma_support_chart', help_='![](https://img.gejiba.com/images/881d1f7010c79b8cfcc6b3dad8c17028.png)')

# 帮助界面
@sv.on_fullmatch("支援卡节奏榜帮助")
async def help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)

@sv.on_rex(r'^(\S服)?(\S{1,2})卡节奏榜$')
async def SSR_speed_chart(bot, ev):
    sup_type = ev['match'].group(2)
    if sup_type not in ['速', '耐', '力', '根', '智', '友人']:
        return
    default_server = await get_server_default()
    try:
        if not ev['match'].group(1):
            if default_server == 'jp':
                msg = await generate_img(sup_type)
            elif default_server == 'tw':
                msg = await generate_img_tw(sup_type)
            else:
                msg = f'该服务器"{default_server}"暂未支持节奏榜'
        else:
            if ev['match'].group(1) == '日服':
                msg = await generate_img(sup_type)
            elif ev['match'].group(1) == '台服':
                msg = await generate_img_tw(sup_type)
            else:
                msg = f'该服务器"{ev["match"].group(1)}"暂未支持节奏榜'
    except AttributeError:
        msg = f'{sup_type}卡节奏榜获取失败!'
    await bot.send(ev, msg)