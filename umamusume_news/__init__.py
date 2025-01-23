import asyncio
import os

from yuiChyan import LakePermissionException
from yuiChyan.permission import check_permission, SUPERUSER
from yuiChyan.service import Service
from .news_spider import get_news, judge, news_broadcast, sort_news, translate_news, query_dict
from ..plugin_utils.base_util import get_img_cq, get_server_default

sv = Service('umamusume_news')
sv_uma = Service('umamusume-news-poller', use_exclude=False)
sv_uma_tw = Service('umamusume-news-poller-tw', use_exclude=False)
sv_uma_bili = Service('umamusume-news-poller-bili', use_exclude=False)


# 帮助界面
@sv.on_match("马娘新闻帮助")
async def _help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)


# 主动获取新闻功能
@sv.on_rex(r'^(\S服)?马娘新闻$')
async def uma_news(bot, ev):
    default_server = await get_server_default()
    try:
        if not ev['match'].group(1):
            if default_server in query_dict:
                msg = await get_news(default_server)
            else:
                msg = f'该服务器"{default_server}"暂未支持马娘新闻'
        else:
            if ev['match'].group(1) == '日服':
                msg = await get_news('jp')
            elif ev['match'].group(1) == '台服':
                msg = await get_news('tw')
            elif ev['match'].group(1) in ['B服', 'b服', '国服']:
                msg = await get_news('bili')
            else:
                msg = f'该服务器"{ev["match"].group(1)}"暂未支持马娘新闻'
    except:
        msg = '获取新闻失败，请等5分钟后再次尝试'
    await bot.send(ev, msg)


# 马娘新闻播报
@sv_uma.scheduled_job(minute='*/5')
async def uma_news_poller():
    try:
        news_list = await sort_news('jp')
        flag = await judge('jp', news_list)
        if flag:
            sv_uma.logger.info('检测到马娘新闻更新！')
            await sv_uma.broadcast(await news_broadcast('jp', news_list), 'umamusume-news-poller', 0.2)
        else:
            sv_uma.logger.info('暂未检测到马娘新闻更新')
            return
    except Exception as e:
        sv_uma.logger.info(f'马娘官网连接失败，具体原因：{e}')


# 台服马娘新闻播报
@sv_uma_tw.scheduled_job(minute='*/5')
async def uma_news_poller_tw():
    try:
        news_list = await sort_news('tw')
        flag = await judge('tw', news_list)
        if flag:
            sv_uma_tw.logger.info('检测到台服马娘新闻更新！')
            await sv_uma_tw.broadcast(await news_broadcast('tw', news_list), 'umamusume-news-poller-tw', 0.2)
        else:
            sv_uma_tw.logger.info('暂未检测到台服马娘新闻更新')
            return
    except Exception as e:
        sv_uma_tw.logger.info(f'台服马娘官网连接失败，具体原因：{e}')


# B服马娘新闻播报
@sv_uma_bili.scheduled_job(minute='*/5')
async def uma_news_poller_bili():
    try:
        news_list = await sort_news('bili')
        flag = await judge('bili', news_list)
        if flag:
            sv_uma_bili.logger.info('检测到B服马娘新闻更新！')
            await sv_uma_bili.broadcast(await news_broadcast('bili', news_list), 'umamusume-news-poller-bili', 0.2)
        else:
            sv_uma_bili.logger.info('暂未检测到B服马娘新闻更新')
            return
    except Exception as e:
        sv_uma_bili.logger.info(f'B服马娘官网连接失败，具体原因：{e}')


# 选择翻译新闻
@sv.on_prefix('新闻翻译')
async def select_source(bot, ev):
    group_id = ev['group_id']
    self_id = ev['self_id']
    try:
        news_list = await sort_news('jp')
    except Exception as e:
        msg = f'错误！马娘官网连接失败，原因：{e}'
        await bot.send(ev, msg)
        return
    num_i = 0
    msg_c = '马娘新闻列表：'
    for news in news_list:
        num_i += 1
        msg_c = msg_c + f'\n{num_i}. ' + news.news_title
    all_text = ev.message.extract_plain_text()
    if all_text not in ['1', '2', '3', '4', '5']:
        msg = '新闻编号错误！(可选值有：1/2/3/4/5)' + '\n\n' + msg_c
        await bot.send(ev, msg)
        return
    news = news_list[int(all_text) - 1]
    msg = '正在龟速翻译，请耐心等待...'
    await bot.send(ev, msg)
    news_id = int(news.news_url.replace('https://umamusume.jp/news/detail.php?id=', ''))
    await asyncio.sleep(0.5)
    head_img, msg = await translate_news(news_id)
    if msg == '错误！马娘官网连接失败':
        await bot.send(ev, '翻译失败，马娘官网连接失败')
        return
    current_dir = os.path.join(os.path.dirname(__file__), 'mode.txt')
    with open(current_dir, 'r', encoding='utf-8') as cf:
        mode = cf.read().strip()
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
    msg_list = [msg[i:i + 1000].strip() for i in range(0, len(msg), 1000)]
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
    if not check_permission(ev,  SUPERUSER):
        raise LakePermissionException(ev, None, SUPERUSER)
    mode = ev.message.extract_plain_text()
    current_dir = os.path.join(os.path.dirname(__file__), 'mode.txt')
    with open(current_dir, 'r', encoding='utf-8') as cf:
        mode_tmp = cf.read().strip()
    if mode not in ['on', 'off']:
        msg = f'模式选择错误(on/off)，默认on，当前{mode_tmp}'
        await bot.send(ev, msg)
        return
    with open(current_dir, 'w', encoding='utf-8') as cf:
        cf.write(mode)
    await bot.send(ev, f'已更换转发模式为{mode}')
