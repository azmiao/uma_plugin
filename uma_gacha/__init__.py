import os

from .pretty_handle import update_pretty_info, pretty_draw, reload_pretty_pool, get_gacha_pool
from hoshino import Service, priv

sv = Service('uma_gacha', help_='![](https://img.gejiba.com/images/b7fe400d61fbefc8cfa52f87683ce507.png)', enable_on_default=True, bundle='马娘抽卡')

# 帮助界面
@sv.on_fullmatch("马娘抽卡帮助")
async def help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = f'[CQ:image,file=file:///{os.path.abspath(img_path)}]'
    await bot.send(ev, sv_help)

# 马娘单抽
@sv.on_fullmatch(('马娘单抽', '单抽马娘'), only_to_me=True)
async def uma_gacha_char_one(bot, ev):
    msg = await pretty_draw(1, 'char')
    await bot.send(ev, msg, at_sender=True)

# 马娘十连
@sv.on_fullmatch(('马娘十连', '马十连'), only_to_me=True)
async def uma_gacha_char_ten(bot, ev):
    msg = await pretty_draw(10, 'char')
    await bot.send(ev, msg, at_sender=True)

# 马娘井
@sv.on_fullmatch(('马之井', '马娘井', '马娘一井'), only_to_me=True)
async def uma_gacha_char_jing(bot, ev):
    msg = await pretty_draw(200, 'char')
    await bot.send(ev, msg, at_sender=True)

# 育成卡单抽
@sv.on_fullmatch(('育成卡单抽', '支援卡单抽','s卡单抽','S卡单抽'), only_to_me=True)
async def uma_gacha_card_one(bot, ev):
    msg = await pretty_draw(1, 'card')
    await bot.send(ev, msg, at_sender=True)

# 育成卡十连
@sv.on_fullmatch(('育成卡十连', '支援卡十连','s卡十连','S卡十连'), only_to_me=True)
async def uma_gacha_card_ten(bot, ev):
    msg = await pretty_draw(10, 'card')
    await bot.send(ev, msg, at_sender=True)

# 育成卡井
@sv.on_fullmatch(('育成卡井', '育成卡一井', '支援卡井', '支援卡一井','s卡井','s卡一井','S卡井','S卡一井'), only_to_me=True)
async def uma_gacha_card_jing(bot, ev):
    msg = await pretty_draw(200, 'card')
    await bot.send(ev, msg, at_sender=True)

# 查看马娘卡池
@sv.on_fullmatch('查看马娘卡池')
async def see_uma_poor(bot, ev):
    char_pool, time = await get_gacha_pool('char')
    card_pool, time = await get_gacha_pool('card')
    msg = f'当前池子时间：\n{time}\n{char_pool}\n{card_pool}'
    await bot.send(ev, msg)

# 更新马娘信息
@sv.on_fullmatch('更新马娘信息')
async def uma_gacha_update(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.send(ev, msg)
        return
    msg_head = '正在更新马娘信息，请稍后'
    await bot.send(ev, msg_head)
    try:
        data = await update_pretty_info()
    except Exception as e:
        msg = f'马娘信息更新失败：{e}'
        await bot.send(ev, msg)
        return
    msg = f'马娘信息更新完成！'
    await bot.send(ev, msg)
    await bot.send(ev, data)

# 重载赛马娘卡池
@sv.on_fullmatch('重载赛马娘卡池')
async def uma_gacha_reload(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.send(ev, msg)
        return
    try:
        text = await reload_pretty_pool()
    except Exception as e:
        msg = f'马娘卡池重载失败：{e}'
        await bot.send(ev, msg)
        return
    msg = f'马娘卡池重载成功！'
    await bot.send(ev, msg)
    await bot.send(ev, text)
