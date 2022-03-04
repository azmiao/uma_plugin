from hoshino import Service
from hoshino.typing import MessageSegment
from hoshino.util import pic2b64
from .get_url import generate_img

sv_help = '''
[速卡节奏榜] 对应速度卡
[耐卡节奏榜] 对应耐力卡
[力卡节奏榜] 对应力量卡
[根卡节奏榜] 对应根性卡
[智卡节奏榜] 对应智力卡
'''.strip()

sv = Service('uma_support_chart', help_=sv_help)

# 帮助界面
@sv.on_fullmatch("支援卡节奏榜帮助")
async def help(bot, ev):
    await bot.send(ev, sv_help)

@sv.on_rex(r'^(\S{2})节奏榜')
async def SSR_speed_chart(bot, ev):
    sup_type = ev['match'].group(1)
    if sup_type not in ['速卡', '耐卡', '力卡', '根卡', '根卡', '智卡']:
        return
    end_img_tmp = generate_img(sup_type)
    end_img = pic2b64(end_img_tmp)
    msg = MessageSegment.image(end_img)
    await bot.send(ev, msg)