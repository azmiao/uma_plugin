import os
import shutil
import asyncio
from hoshino import Service, R
from hoshino.util import FreqLimiter
from .news_spider import *

sv_help = '''=====功能=====
[马娘新闻] 查看最近五条新闻

[新闻翻译] 查看翻译命令和新闻编号（限近5条）

[新闻翻译 1] 翻译第1条新闻，编号可选值(1/2/3/4/5)

（自动推送） 该功能没有命令'''.strip()

_limtime = 20    # 单个人翻译冷却时间（单位：喵）
_flmt = FreqLimiter(_limtime)

dir_path = os.path.join(R.img('umamusume').path, 'umamusume_news/')
if os.path.exists(dir_path):
    shutil.rmtree(dir_path)  #删除目录，包括目录下的所有文件
    os.mkdir(dir_path)
else:
    os.mkdir(dir_path)

sv = Service('umamusume_news', enable_on_default=True)
svuma = Service('umamusume-news-poller', enable_on_default=False)

# 帮助界面
@sv.on_fullmatch("马娘新闻帮助")
async def help(bot, ev):
    await bot.send(ev, sv_help)

# 主动获取新闻功能
@sv.on_fullmatch(('马娘新闻', '赛马娘新闻'))
async def uma_news(bot, ev):
    try:
        msg = await get_news()
    except:
        msg = '获取新闻失败，请等5分钟后再次尝试'
    await bot.send(ev, msg)

# 马娘新闻播报
@svuma.scheduled_job('cron', minute='*/5')
async def uma_news_poller():
    try:
        flag = await judge()
        if flag:
            svuma.logger.info('检测到马娘新闻更新！')
            await svuma.broadcast(await news_broadcast(), 'umamusume-news-poller', 0.2)
        else:
            svuma.logger.info('暂未检测到马娘新闻更新')
            return
    except Exception as e:
        svuma.logger.info(f'马娘官网连接失败，具体原因：{e}')

# 选择翻译新闻
@sv.on_prefix('新闻翻译')
async def select_source(bot, ev):
    uid = ev['user_id']
    if not _flmt.check(uid):
        await bot.send(ev, f'请勿频繁操作，冷却时间为{_limtime}秒！', at_sender=True)
        return
    try:
        news_list = await sort_news()
    except Exception as e:
        msg = f'错误！马娘官网连接失败，原因：{e}'
        await bot.send(ev, msg)
        return
    num_i = 0
    msg_c = '马娘新闻列表：'
    for news in news_list:
        num_i += 1
        msg_c = msg_c + f'\n{num_i}. ' + news.news_title
    alltext = ev.message.extract_plain_text()
    if alltext != '1' and alltext != '2' and alltext != '3' and alltext != '4'and alltext != '5':
        msg = '新闻编号错误！(可选值有：1/2/3/4/5)' + '\n\n' + msg_c
        await bot.send(ev, msg)
        return
    num_j = 0
    for news in news_list:
        num_j += 1
        if str(num_j) == alltext:
            msg = '正在龟速翻译，请耐心等待...'
            await bot.send(ev, msg)
            msg = f'马娘新闻《{news.news_title}》翻译内容如下：\n\n'
            news_url_tmp = news.news_url
            news_id = int(news_url_tmp.replace('▲https://umamusume.jp/news/detail.php?id=', ''))
            await asyncio.sleep(0.5)
            msg += await translate_news(news_id)
            try:
                await bot.send(ev, msg)
            except Exception as err:
                if err == '<ActionFailed, retcode=100>':
                    await bot.send(ev, "翻译内容被风控，发送失败！请稍后尝试！")