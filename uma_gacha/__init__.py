from .pretty_handle import update_pretty_info, pretty_draw, reload_pretty_pool, get_gacha_pool
import hoshino
import asyncio
import os
import json
import re
import datetime
from hoshino import Service, priv, log, R
from .config import check_config
from .async_update_game_info import async_update_game
from .util import _check_dir

logger = log.new_logger('announcement', hoshino.config.DEBUG)

check_config()
loop = asyncio.get_event_loop()
loop.run_until_complete(async_update_game())
_check_dir()
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'char_atlas.txt')):
    logger.info('检测到本地图鉴信息不存在，即将开始创建...')
    try:
        loop.run_until_complete(update_pretty_info())
    except Exception as e:
        logger.info(f'马娘信息更新失败：{e}')

sv_help = '''=====功能=====
（@bot就是@机器人）

[查看马娘卡池] 看马娘当前的池子

[@bot马娘单抽] 马娘池子单抽
[@bot马娘十连] 马娘池子十连
[@bot马之井] 马娘池子抽一井

[@bot育成卡单抽] 育成卡池子单抽
[@bot育成卡十连] 育成卡池子十连
[@bot育成卡井] 育成卡池子抽一井'''.strip()

sv = Service('uma_gacha', help_=sv_help, enable_on_default=True, bundle='马娘抽卡')

# 帮助界面
@sv.on_fullmatch("马娘抽卡帮助")
async def help(bot, ev):
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
@sv.on_fullmatch('育成卡单抽', only_to_me=True)
async def uma_gacha_card_one(bot, ev):
    msg = await pretty_draw(1, 'card')
    await bot.send(ev, msg, at_sender=True)

# 育成卡十连
@sv.on_fullmatch('育成卡十连', only_to_me=True)
async def uma_gacha_card_ten(bot, ev):
    msg = await pretty_draw(10, 'card')
    await bot.send(ev, msg, at_sender=True)

# 育成卡井
@sv.on_fullmatch(('育成卡井', '育成卡一井'), only_to_me=True)
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

# 自动检测是否有更新，若有则自动更新赛马娘up卡池
@sv.scheduled_job('cron', hour='4', minute='00')
async def auto_update():
    sv.logger.info('开始检测马娘卡池是否有更新')
    draw_path = R.img('uma_gacha').path
    with open(f'{draw_path}/draw_card_up/pretty_up_char.json', encoding='UTF-8') as f:
        data = json.load(f)
    up_time = str(data['char']['time'])
    end_time = re.search(r'- (\d{1,2})月(\d{1,2})日', up_time)
    now_time = datetime.datetime.now()
    startTime = datetime.datetime(int(now_time.year), int(end_time.group(1)), int(end_time.group(2))+1, 4, 00, 0)
    if now_time < startTime:
        sv.logger.info(f'未检测到更新！当前池子结束时间：{str(now_time.year)}年{str(end_time.group(1))}月{str(end_time.group(2))}日 11:00')
        return
    bot = hoshino.get_bot()
    superid = hoshino.config.SUPERUSERS[0]
    sv.logger.info('检测到更新！正在更新赛马娘信息和up卡池')
    try:
        await update_pretty_info()
    except Exception as e:
        sv.logger.info(f'自动更新赛马娘信息和up卡池失败，{e}')
        msg = f'自动更新赛马娘信息和up卡池失败，{e}'
        msg = msg + '\n可能是公告界面布局变动导致，请先使用命令“更新马娘信息”手动更新查看报错日志然后反馈，或等待插件更新，一般来说插件更新的还是蛮勤快的'
        await bot.send_private_msg(user_id=superid, message=msg)
        return
    sv.logger.info('自动更新赛马娘信息和up卡池成功')
    msg = '自动更新赛马娘信息和up卡池成功'
    await bot.send_private_msg(user_id=superid, message=msg)# 若不想要自动更新成功的提醒，吧这整行注释了就行