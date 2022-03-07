import os
import shutil
import hoshino
from hoshino import Service, R, priv
from hoshino.typing import *
from hoshino.util import FreqLimiter, concat_pic, pic2b64, silence
from .news_spider import *

sv_help = '''=====功能=====
[马娘新闻] 查看最近五条新闻

[新闻翻译] 查看翻译命令和新闻编号（限近5条）

[新闻翻译 1] 翻译第1条新闻，编号可选值(1/2/3/4/5)

（自动推送） 该功能没有命令'''.strip()

_limtime = 20    # 单个人翻译冷却时间（单位：喵）
_flmt = FreqLimiter(_limtime)

if os.path.exists(R.img('umamusume_news').path):
    shutil.rmtree(R.img('umamusume_news').path)  #删除目录，包括目录下的所有文件
    os.mkdir(R.img('umamusume_news').path)
else:
    os.mkdir(R.img('umamusume_news').path)

sv = Service('umamusume_news', help_=sv_help, enable_on_default=True, bundle='马娘新闻订阅')
svuma = Service('umamusume-news-poller', enable_on_default=False, help_='马娘新闻播报')

# 帮助界面
@sv.on_fullmatch("马娘新闻帮助")
async def help(bot, ev):
    await bot.send(ev, sv_help)

# 主动获取新闻功能
@sv.on_fullmatch(('马娘新闻', '赛马娘新闻'))
async def uma_news(bot, ev):
    try:
        msg = get_news()
    except:
        msg = '获取新闻失败，请等5分钟后再次尝试'
    await bot.send(ev, msg)

# 马娘新闻播报
@svuma.scheduled_job('cron', minute='*/5')
async def uma_news_poller():
    try:
        if (judge() == True):
            svuma.logger.info('检测到马娘新闻更新！')
            await svuma.broadcast(news_broadcast(), 'umamusume-news-poller', 0.2)
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
        news_list = sort_news()
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
            msg = msg + translate_news(news_id)
            await bot.send(ev, msg)