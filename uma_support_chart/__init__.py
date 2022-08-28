import os

from .get_url import generate_img
from .get_url_tw import generate_img_tw
from hoshino import Service
from ..plugin_utils.send_img import get_img_cq

sv = Service('uma_support_chart', help_='![](https://img.gejiba.com/images/881d1f7010c79b8cfcc6b3dad8c17028.png)')

# 帮助界面
@sv.on_fullmatch("支援卡节奏榜帮助")
async def help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)

@sv.on_rex(r'^(台服)?(\S{1,2})卡节奏榜$')
async def SSR_speed_chart(bot, ev):
    sup_type = ev['match'].group(2)
    if sup_type not in ['速', '耐', '力', '根', '智', '友人']:
        return
    try:
        if not ev['match'].group(1):
            msg = await generate_img(sup_type)
        else:
            msg = await generate_img_tw(sup_type)
    except AttributeError:
        msg = f'{sup_type}卡节奏榜获取失败!'
    await bot.send(ev, msg)