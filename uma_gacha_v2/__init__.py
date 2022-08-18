import os

from .gacha import Gacha
from . update_init import auto_update
from .util import get_pool, get_img_path, generate_img, random_comment, server_list, \
    switch_server, switch_pool_id, get_pool_detail
from hoshino import Service, priv
from ..plugin_utils.send_img import get_img_cq

sv = Service('uma_gacha_v2', help_='![](https://img.gejiba.com/images/4d0aa3a260363002bb4edabb689c141e.png)')

# 帮助界面
@sv.on_fullmatch("马娘抽卡帮助")
async def help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)

# 马娘单抽
@sv.on_fullmatch(('马娘单抽', '单抽马娘'), only_to_me=True)
async def one_gacha_uma(bot, ev):
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await one_gacha(group_id, user_id, 'uma')
    await bot.send(ev, msg)

# 支援卡单抽
@sv.on_fullmatch(('育成卡单抽', '支援卡单抽','s卡单抽','S卡单抽'), only_to_me=True)
async def one_gacha_chart(bot, ev):
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await one_gacha(group_id, user_id, 'chart')
    await bot.send(ev, msg)

# 马娘十连
@sv.on_fullmatch(('马娘十连', '马十连'), only_to_me=True)
async def ten_gacha_uma(bot, ev):
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await ten_gacha(group_id, user_id, 'uma')
    await bot.send(ev, msg)

# 育成卡十连
@sv.on_fullmatch(('育成卡十连', '支援卡十连','s卡十连','S卡十连'), only_to_me=True)
async def ten_gacha_chart(bot, ev):
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await ten_gacha(group_id, user_id, 'chart')
    await bot.send(ev, msg)

# 马娘井
@sv.on_fullmatch(('马之井', '马娘井', '马娘一井'), only_to_me=True)
async def tenjou_gacha_uma(bot, ev):
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await tenjou_gacha(group_id, user_id, 'uma')
    await bot.send(ev, msg)

# 育成卡井
@sv.on_fullmatch(('育成卡井', '育成卡一井', '支援卡井', '支援卡一井','s卡井','s卡一井','S卡井','S卡一井'), only_to_me=True)
async def tenjou_gacha_chart(bot, ev):
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await tenjou_gacha(group_id, user_id, 'chart')
    await bot.send(ev, msg)

# 育成卡抽满破
@sv.on_fullmatch(('育成卡抽满破', '支援卡抽满破'), only_to_me=True)
async def full_singer_gacha_chart(bot, ev):
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await full_singer_gacha(group_id, user_id, 'chart')
    await bot.send(ev, msg)

# 选择卡池
@sv.on_prefix('切换马娘服务器')
async def change_server(bot, ev):
    group_id = str(ev.group_id)
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '切换服务器仅限群管理员操作哦~')
    server = str(ev.message)
    if not server in server_list:
        await bot.finish(ev, f'切换失败！目前仅支持服务器：\n{" | ".join(server_list)}')
    msg = await switch_server(group_id, server)
    await bot.send(ev, msg)

# 选择卡池
@sv.on_prefix('切换马娘卡池')
async def change_pool(bot, ev):
    group_id = str(ev.group_id)
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '切换卡池仅限群管理员操作哦~')
    pool_id = str(ev.message)
    msg = await switch_pool_id(group_id, pool_id)
    await bot.send(ev, msg)

# 查看卡池
@sv.on_fullmatch('查看马娘卡池')
async def change_pool(bot, ev):
    group_id = str(ev.group_id)
    msg = await get_pool_detail(group_id)
    await bot.send(ev, msg)

# 手动更新卡池
@sv.on_fullmatch('更新马娘卡池')
async def uma_gacha_update(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.finish(ev, msg)
    msg = await auto_update()
    await bot.send(ev, msg)

async def one_gacha(group_id, user_id, gacha_type):
    server, pool_id = await get_pool(group_id)
    gacha = Gacha(pool_id, gacha_type, server)
    chara, res_type = gacha.gacha_one(gacha.up_prob, gacha.s3_prob, gacha.s2_prob, gacha.s1_prob)
    img_path = await get_img_path(chara, gacha_type)
    img = await get_img_cq(img_path)
    msg = f'{img}\n[CQ:at,qq={user_id}]\n抽到了 {chara}'
    if res_type == 'up':
        msg += '\nPS.兄弟姐妹们，有挂！'
    elif res_type == 's3':
        msg += '\nPS.这就是欧皇附体吗？'
    return msg

async def ten_gacha(group_id, user_id, gacha_type):
    server, pool_id = await get_pool(group_id)
    gacha = Gacha(pool_id, gacha_type, server)
    first_up, result = gacha.gacha_ten(gacha.result, gacha.first_up)
    result_list = result['up'] + result['s3'] + result['s2'] + result['s1']
    result_image = await generate_img(result_list, gacha_type)
    msg_com = await random_comment(result, gacha_type, first_up, '十连')
    msg = f'[CQ:image,file={result_image}]\n[CQ:at,qq={user_id}]\n{msg_com}'
    return msg

async def tenjou_gacha(group_id, user_id, gacha_type):
    server, pool_id = await get_pool(group_id)
    gacha = Gacha(pool_id, gacha_type, server)
    first_up, result = gacha.gacha_tenjou(gacha.result, gacha.first_up)
    result_list = result['up'] + result['s3']
    result_image = await generate_img(result_list, gacha_type)
    msg_com = await random_comment(result, gacha_type, first_up, '天井')
    msg = f'[CQ:image,file={result_image}]\n[CQ:at,qq={user_id}]\n{msg_com}'
    return msg

async def full_singer_gacha(group_id, user_id, gacha_type):
    server, pool_id = await get_pool(group_id)
    if pool_id == '000000':
        return '初始卡池000000不支持该功能哦'
    gacha = Gacha(pool_id, gacha_type, server)
    select_chart, up_num, ten_num, exchange, first_up, result = gacha.gacha_full_singer(gacha.result, gacha.first_up)
    result_list = result['up'] + result['s3']
    result_image = await generate_img(result_list, gacha_type)
    msg_com = await random_comment(result, gacha_type, first_up, '抽满破')
    msg = f'[CQ:image,file={result_image}]\n[CQ:at,qq={user_id}]\n{msg_com}\n'
    msg += f'▼目标：{select_chart}\n最终获得{up_num}张\n其中兑换了{exchange}张\n总共花费{ten_num * 10}抽'
    return msg