from hoshino import Service, priv
from .comic import update_info, get_comic_random, get_comic_id, get_comic_uma

sv_help = '''
=====功能=====

[马娘漫画] 随机一张马娘游戏内的一格漫画

[马娘漫画 xxx] xxx为角色名字，没有该角色的一格漫画就不会有反应

[马娘漫画 x号] x为数字，是一格漫画的编号，编号不是整数就不会有反应
'''.strip()

sv = Service('uma_comic', help_ = sv_help)

@sv.on_fullmatch('马娘漫画帮助')
async def get_help(bot, ev):
    await bot.send(ev, sv_help)

@sv.on_prefix('马娘漫画')
async def check_meanings(bot, ev):
    uma_name_tmp = str(ev.message)
    if not uma_name_tmp:
        msg = await get_comic_random()
    elif uma_name_tmp.endswith('号'):
        try:
            id = int(uma_name_tmp.replace('号', ''))
        except:
            id = 0
            return
        msg = await get_comic_id(str(id))
    else:
        msg = await get_comic_uma(uma_name_tmp)
        if not msg:
            return
    await bot.send(ev, msg)

# 手动更新，已存在图片的话会自动跳过
@sv.on_fullmatch('手动更新马娘漫画')
async def force_update(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.send(ev, msg)
        return
    await update_info()
    await bot.send(ev, '马娘漫画更新完成')