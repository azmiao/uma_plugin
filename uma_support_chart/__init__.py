from hoshino import Service
from hoshino.typing import MessageSegment
from hoshino.util import pic2b64
from .get_url import generate_img
import httpx

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
    try:
        end_img_tmp, update_info = await generate_img(sup_type)
    except httpx.ConnectError:
        msg = 'biwiki连接失败，请重新输入命令重试！'
        await bot.finish(ev, msg)
    if not end_img_tmp:
        msg = f'新版{sup_type}节奏榜还未出炉，本地也未检测到旧版{sup_type}节奏榜。请等待新版节奏榜更新'
        await bot.finish(ev, msg)
    if update_info == 'old':
        msg = f'新版{sup_type}节奏榜已更新，但未获取到图片可能是还没上传，因此即将发送本地缓存的旧版{sup_type}节奏榜'
        await bot.send(ev, msg)
    end_img = pic2b64(end_img_tmp)
    msg = MessageSegment.image(end_img)
    await bot.send(ev, msg)