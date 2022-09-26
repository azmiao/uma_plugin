import os
import base64
import asyncio

from hoshino import Service, priv
from .news_spider import get_news, judge, news_broadcast, sort_news, translate_news
from .news_spider_tw import get_news_tw, judge_tw, news_broadcast_tw
from ..plugin_utils.base_util import get_img_cq, get_server_default

sv = Service('umamusume_news', enable_on_default=True)
with open(os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png'), 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
sv.help = f'![](data:image/jpeg;base64,{s})'
svuma = Service('umamusume-news-poller', enable_on_default=False)
svumatw = Service('umamusume-news-poller-tw', enable_on_default=False)

# 帮助界面
@sv.on_fullmatch("马娘新闻帮助")
async def help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)

# 主动获取新闻功能
@sv.on_rex(r'^(\S服)?马娘新闻$')
async def uma_news(bot, ev):
    default_server = await get_server_default()
    try:
        if not ev['match'].group(1):
            if default_server == 'jp':
                msg = await get_news()
            elif default_server == 'tw':
                msg = await get_news_tw()
            else:
                msg = f'该服务器"{default_server}"暂未支持马娘新闻'
        else:
            if ev['match'].group(1) == '日服':
                msg = await get_news()
            elif ev['match'].group(1) == '台服':
                msg = await get_news_tw()
            else:
                msg = f'该服务器"{ev["match"].group(1)}"暂未支持马娘新闻'
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

# 台服马娘新闻播报
@svumatw.scheduled_job('cron', minute='*/5')
async def uma_news_poller_tw():
    try:
        flag = await judge_tw()
        if flag:
            svumatw.logger.info('检测到台服马娘新闻更新！')
            await svumatw.broadcast(await news_broadcast_tw(), 'umamusume-news-poller-tw', 0.2)
        else:
            svumatw.logger.info('暂未检测到台服马娘新闻更新')
            return
    except Exception as e:
        svumatw.logger.info(f'台服马娘官网连接失败，具体原因：{e}')

# 选择翻译新闻
@sv.on_prefix('新闻翻译')
async def select_source(bot, ev):
    group_id = ev['group_id']
    self_id = ev['self_id']
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
    if alltext not in ['1', '2', '3', '4', '5']:
        msg = '新闻编号错误！(可选值有：1/2/3/4/5)' + '\n\n' + msg_c
        await bot.send(ev, msg)
        return
    news = news_list[int(alltext)-1]
    msg = '正在龟速翻译，请耐心等待...'
    await bot.send(ev, msg)
    news_id = int(news.news_url.replace('▲https://umamusume.jp/news/detail.php?id=', ''))
    await asyncio.sleep(0.5)
    head_img, msg = await translate_news(news_id)
    if msg == '错误！马娘官网连接失败':
        await bot.send(ev, '翻译失败，马娘官网连接失败')
        return
    current_dir = os.path.join(os.path.dirname(__file__), 'mode.txt')
    with open(current_dir, 'r', encoding='utf-8') as f:
        mode = f.read().strip()
    if mode == 'off':
        await bot.send(ev, head_img + msg)
        return
    forward_msg = [
        {
            "type": "node",
            "data": {
                "name": "马娘新闻翻译",
                "uin": self_id,
                "content": f'标题：\n{news.news_title}'
            }
        }
    ]
    if head_img:
        forward_msg.append({
            "type": "node",
            "data": {
                "name": "马娘BOT",
                "uin": self_id,
                "content": head_img
            }
        })
    msg_list = [msg[i:i+1000].strip() for i in range(0, len(msg), 1000)]
    for msg_i in msg_list:
        forward_msg.append({
            "type": "node",
            "data": {
                "name": "马娘BOT",
                "uin": self_id,
                "content": msg_i
            }
        })
    await bot.send_group_forward_msg(group_id=group_id, messages=forward_msg)

# 选择模式
@sv.on_prefix('马娘新闻翻译转发模式')
async def change_mode(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.finish(ev, msg)
    mode = ev.message.extract_plain_text()
    current_dir = os.path.join(os.path.dirname(__file__), 'mode.txt')
    with open(current_dir, 'r', encoding='utf-8') as f:
        mode_tmp = f.read().strip()
    if mode not in ['on', 'off']:
        msg = f'模式选择错误(on/off)，默认on，当前{mode_tmp}'
        await bot.finish(ev, msg)
    with open(current_dir, 'w', encoding='utf-8') as f:
        f.write(mode)
    await bot.send(ev, f'已更换转发模式为{mode}')