import base64
import os

from hoshino import Service, priv
from hoshino.util import DailyNumberLimiter, FreqLimiter

from .gacha_class import Gacha
from .gacha_target import set_target_config, get_current_up_id_dict, reset_target_config, \
    query_target_config
from .update_init import auto_update
from .util import get_pool, get_img_path, generate_img, random_comment, server_list, \
    switch_server, switch_pool_id, get_pool_detail
from ..plugin_utils.base_util import get_img_cq

# 自定义配置
#############################

# 每个人的指令冷却 | 默认10秒
lmt = FreqLimiter(10)

# 单抽和十连的萝卜上限 | 默认每天30000萝卜
single_limit = DailyNumberLimiter(30000)

# 抽井的次数(马娘池和支援卡池次数共通) | 默认每天15次
tenjou_limit = DailyNumberLimiter(15)

# 抽满破的次数 | 默认每天10次
full_limit = DailyNumberLimiter(10)

# 超过次数的消息
SINGLE_EXCEED_NOTICE = f'您今天已经抽过{single_limit.max}颗萝卜了，欢迎明早5点后再来哦！'
TENJOU_EXCEED_NOTICE = f'您今天已经抽过{tenjou_limit.max}张天井券了，欢迎明早5点后再来哦！'
FULL_EXCEED_NOTICE = f'您今天已经抽过{full_limit.max}次支援卡满破了，欢迎明早5点后再来哦！'

#############################


sv = Service('uma_gacha_v2')
with open(os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png'), 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
sv.help = f'![](data:image/jpeg;base64,{s})'


# 帮助界面
@sv.on_fullmatch("马娘抽卡帮助")
async def sv_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help_img = await get_img_cq(img_path)
    await bot.send(ev, sv_help_img)


# 马娘单抽
@sv.on_fullmatch(('马娘单抽', '单抽马娘'), only_to_me=True)
async def one_gacha_uma(bot, ev):
    if not lmt.check(ev.user_id):
        await bot.finish(ev, f'马娘抽卡功能冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
    if not single_limit.check(ev.user_id):
        await bot.finish(ev, SINGLE_EXCEED_NOTICE, at_sender=True)
    lmt.start_cd(ev.user_id)
    single_limit.increase(ev.user_id, 150)
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await one_gacha(group_id, user_id, 'uma')
    await bot.send(ev, msg)


# 支援卡单抽
@sv.on_fullmatch(('育成卡单抽', '支援卡单抽', 's卡单抽', 'S卡单抽'), only_to_me=True)
async def one_gacha_chart(bot, ev):
    if not lmt.check(ev.user_id):
        await bot.finish(ev, f'马娘抽卡功能冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
    if not single_limit.check(ev.user_id):
        await bot.finish(ev, SINGLE_EXCEED_NOTICE, at_sender=True)
    lmt.start_cd(ev.user_id)
    single_limit.increase(ev.user_id, 150)
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await one_gacha(group_id, user_id, 'chart')
    await bot.send(ev, msg)


# 马娘十连
@sv.on_fullmatch(('马娘十连', '马十连'), only_to_me=True)
async def ten_gacha_uma(bot, ev):
    if not lmt.check(ev.user_id):
        await bot.finish(ev, f'马娘抽卡功能冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
    if not single_limit.check(ev.user_id):
        await bot.finish(ev, SINGLE_EXCEED_NOTICE, at_sender=True)
    lmt.start_cd(ev.user_id)
    single_limit.increase(ev.user_id, 1500)
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await ten_gacha(group_id, user_id, 'uma')
    await bot.send(ev, msg)


# 育成卡十连
@sv.on_fullmatch(('育成卡十连', '支援卡十连', 's卡十连', 'S卡十连'), only_to_me=True)
async def ten_gacha_chart(bot, ev):
    if not lmt.check(ev.user_id):
        await bot.finish(ev, f'马娘抽卡功能冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
    if not single_limit.check(ev.user_id):
        await bot.finish(ev, SINGLE_EXCEED_NOTICE, at_sender=True)
    lmt.start_cd(ev.user_id)
    single_limit.increase(ev.user_id, 1500)
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await ten_gacha(group_id, user_id, 'chart')
    await bot.send(ev, msg)


# 马娘井
@sv.on_fullmatch(('马之井', '马娘井', '马娘一井'), only_to_me=True)
async def tenjou_gacha_uma(bot, ev):
    if not lmt.check(ev.user_id):
        await bot.finish(ev, f'马娘抽卡功能冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
    if not tenjou_limit.check(ev.user_id):
        await bot.finish(ev, TENJOU_EXCEED_NOTICE, at_sender=True)
    lmt.start_cd(ev.user_id)
    tenjou_limit.increase(ev.user_id)
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await tenjou_gacha(group_id, user_id, 'uma')
    await bot.send(ev, msg)


# 育成卡井
@sv.on_fullmatch(('育成卡井', '育成卡一井', '支援卡井', '支援卡一井', 's卡井', 's卡一井', 'S卡井', 'S卡一井'),
                 only_to_me=True)
async def tenjou_gacha_chart(bot, ev):
    if not lmt.check(ev.user_id):
        await bot.finish(ev, f'马娘抽卡功能冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
    if not tenjou_limit.check(ev.user_id):
        await bot.finish(ev, TENJOU_EXCEED_NOTICE, at_sender=True)
    lmt.start_cd(ev.user_id)
    tenjou_limit.increase(ev.user_id)
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await tenjou_gacha(group_id, user_id, 'chart')
    await bot.send(ev, msg)


# 育成卡抽满破
@sv.on_fullmatch(('育成卡抽满破', '支援卡抽满破'), only_to_me=True)
async def full_singer_gacha_chart(bot, ev):
    if not lmt.check(ev.user_id):
        await bot.finish(ev, f'马娘抽卡功能冷却中(剩余 {int(lmt.left_time(ev.user_id)) + 1}秒)', at_sender=True)
    if not full_limit.check(ev.user_id):
        await bot.finish(ev, FULL_EXCEED_NOTICE, at_sender=True)
    lmt.start_cd(ev.user_id)
    full_limit.increase(ev.user_id)
    group_id, user_id = str(ev.group_id), str(ev.user_id)
    msg = await full_singer_gacha(group_id, user_id, 'chart')
    await bot.send(ev, msg)


# 选择支援卡满破目标
@sv.on_prefix(('育成卡选择满破目标', '支援卡选择满破目标'), only_to_me=True)
async def select_target_on_full(bot, ev):
    user_id = str(ev.user_id)
    group_id = str(ev.group_id)
    target_raw = str(ev.message).strip()

    chart_up_id_dict = await get_current_up_id_dict(group_id)
    if not target_raw:
        # 没选目标就展示可选列表
        msg = '您未输入目标，请从以下目标选择，输入数字ID即可，多个目标用英文逗号间隔，需要添加全部UP请输入"all"，输错将会跳过：\n'
        msg += '\n'.join([f'> {key}: {value}' for key, value in chart_up_id_dict.items()])
    else:
        # 选目标就按照目标存入
        if target_raw == 'all':
            # 全部UP
            chart_up_id_dict = await get_current_up_id_dict(group_id)
            raw_id_list = list(chart_up_id_dict.keys())
        else:
            raw_id_list = target_raw.split(',')
        await set_target_config(user_id, raw_id_list)
        chart_name_list = [chart_up_id_dict.get(x, '') for x in raw_id_list]
        if '' in chart_name_list:
            chart_name_list.remove('')
        msg = '已将以下目标设置为您的目标，注意卡池更新后将会重置，需要清除目标请使用“支援卡清除满破目标”命令：\n'
        msg += '\n'.join(chart_name_list)
    await bot.send(ev, msg, at_sender=True)


# 查询支援卡满破目标
@sv.on_fullmatch(('育成卡查询满破目标', '支援卡查询满破目标'), only_to_me=True)
async def query_target_on_full(bot, ev):
    user_id = str(ev.user_id)
    current_name_list = await query_target_config(user_id)
    if not current_name_list:
        msg = '您当前没有任何满破目标呢！'
    else:
        msg = '当前您的目标为下列支援卡，需要清除目标请使用“支援卡清除满破目标”命令：\n'
        msg += '\n'.join(current_name_list)
    await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch(('育成卡清除满破目标', '支援卡清除满破目标'), only_to_me=True)
async def clear_target_on_full(bot, ev):
    user_id = str(ev.user_id)
    await reset_target_config(user_id)
    msg = '已为你清除满破目标选择'
    await bot.send(ev, msg, at_sender=True)


# 选择卡池
@sv.on_prefix('切换马娘服务器')
async def change_server(bot, ev):
    group_id = str(ev.group_id)
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '切换服务器仅限群管理员操作哦~')
    server = str(ev.message)
    if server not in server_list:
        await bot.finish(ev, f'切换失败！目前仅支持服务器：\n{" | ".join(server_list)}')
    msg = await switch_server(group_id, server)
    await bot.send(ev, msg)


# 选择卡池
@sv.on_prefix('切换马娘卡池')
async def change_pool(bot, ev):
    group_id = str(ev.group_id)
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '切换卡池仅限群管理员操作哦~')
    pool_id = str(ev.message).strip()
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
    try:
        chara, res_type = gacha.gacha_one(gacha.up_prob, gacha.s3_prob, gacha.s2_prob, gacha.s1_prob)
        img_path = await get_img_path(chara, gacha_type)
        img = await get_img_cq(img_path)
        msg = f'{img}\n[CQ:at,qq={user_id}]\n抽到了 {chara}'
        if res_type == 'up':
            msg += '\nPS.兄弟姐妹们，有挂！'
        elif res_type == 's3':
            msg += '\nPS.这就是欧皇附体吗？'
    except IndexError as _:
        msg = f'卡池数据还未自动更新完全，请耐心等待几小时后再尝试'
    return msg


async def ten_gacha(group_id, user_id, gacha_type):
    server, pool_id = await get_pool(group_id)
    gacha = Gacha(pool_id, gacha_type, server)
    try:
        first_up, result = gacha.gacha_ten(gacha.result, gacha.first_up)
        result_list = result['up'] + result['s3'] + result['s2'] + result['s1']
        result_image = await generate_img(result_list, gacha_type)
        msg_com = await random_comment(result, gacha_type, first_up, '十连')
        msg = f'[CQ:image,file={result_image}]\n[CQ:at,qq={user_id}]\n{msg_com}'
    except IndexError as _:
        msg = f'卡池数据还未自动更新完全，请耐心等待几小时后再尝试'
    return msg


async def tenjou_gacha(group_id, user_id, gacha_type):
    server, pool_id = await get_pool(group_id)
    gacha = Gacha(pool_id, gacha_type, server)
    try:
        first_up, result = gacha.gacha_tenjou(gacha.result, gacha.first_up)
        result_list = result['up'] + result['s3']
        result_image = await generate_img(result_list, gacha_type)
        msg_com = await random_comment(result, gacha_type, first_up, '天井')
        msg = f'[CQ:image,file={result_image}]\n[CQ:at,qq={user_id}]\n{msg_com}'
    except IndexError as _:
        msg = f'卡池数据还未自动更新完全，请耐心等待几小时后再尝试'
    return msg


async def full_singer_gacha(group_id, user_id, gacha_type):
    server, pool_id = await get_pool(group_id)
    if pool_id == '00000000':
        return '初始卡池00000000不支持该功能哦'
    gacha = Gacha(pool_id, gacha_type, server)
    try:
        # 选择的目标
        chart_name_list = await query_target_config(user_id)
        need_dict, ten_num, exchange, first_up, result = gacha.gacha_full_singer(
            gacha.result,
            gacha.first_up,
            chart_name_list
        )
        up_msg_tmp = [f'✦ 获得{str(value)}张{key}' for key, value in need_dict.items()]
        up_msg = '\n'.join(up_msg_tmp)
        result_list = result['up'] + result['s3']
        result_image = await generate_img(result_list, gacha_type)
        msg_com = await random_comment(result, gacha_type, first_up, '抽满破')

        msg = f'[CQ:image,file={result_image}]\n[CQ:at,qq={user_id}]\n{msg_com}\n'
        msg += f'{up_msg}\n✦ 其中兑换了{exchange}张\n总共花费{ten_num * 10}抽'
    except IndexError as _:
        msg = f'卡池数据还未自动更新完全，请耐心等待几小时后再尝试'
    return msg
