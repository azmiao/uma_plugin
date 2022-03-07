'''
插件仓库：https://github.com/azmiao/uma_bir

作者：AZMIAO

版本：1.0.0
'''

import traceback
from hoshino import Service, priv
from hoshino.typing import MessageSegment
from hoshino.util import pic2b64
import hoshino
import os
import asyncio
import datetime
import json
from .spider import uma_spider, get_cn, ENABLE_OCR_SPACE, APIKEY
from .adaptability import get_adaptability
from .detail_info import get_detail

sv_help = '''
== 仅支持马娘 ==
[查今天生日马娘] 看看今天哪只马娘生日
[查马娘生日 xx] xx为马娘名字
[查生日马娘 m-d] m-d就是 m月d日
== 支持全部角色 ==
[查角色id xx] xx为角色名字
[查角色日文名 xx] xx为角色名字
[查角色中文名 xx] xx为角色名字
[查角色英文名 xx] xx为角色名字
[查角色分类 xx] xx为角色名字
[查角色语音 xx] xx为角色名字
[查角色头像 xx] xx为角色名字
[查角色cv xx] xx为角色名字
[查角色身高 xx] xx为角色名字
[查角色体重 xx] xx为角色名字
[查角色三围 xx] xx为角色名字
[查角色制服 xx] xx为角色名字
[查角色决胜服 xx] xx为角色名字
[查角色原案 xx] xx为角色名字
[查角色适应性 xx] xx为角色名字
[查角色详细信息 xx] xx为角色名字(显示全部信息)
== 维护组功能 ==
[手动更新马娘数据] 功能限维护组
'''.strip()

current_dir = os.path.join(os.path.dirname(__file__), 'config.json')

sv = Service('uma_info', help_ = sv_help, enable_on_default = True)
svbr = Service('uma_bir_push', enable_on_default = False)

@sv.on_fullmatch('马娘数据帮助')
async def get_help(bot, ev):
    await bot.send(ev, sv_help)

@sv.on_fullmatch('查今天生日马娘')
async def get_tod(bot, ev):
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
        f.close()
    tod = datetime.datetime.now().strftime('%m-%d')
    tod_list = tod.split('-', 1)
    tod = '-'.join(str(int(tod_num, 10)) for tod_num in tod_list)
    tod_list = []
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for uma_name in name_list:
        if f_data[uma_name]['category'] == 'umamusume':
            if str(f_data[uma_name]['bir']) == str(tod):
                cn_name = f_data[uma_name]['cn_name'] if f_data[uma_name]['cn_name'] else f_data[uma_name]['jp_name']
                tod_list.append(cn_name)
    if not tod_list:
        msg = f'今天没有马娘生日哟'
        await bot.finish(ev, msg)
    msg = '今天生日的马娘有：\n' + ' | '.join(tod_list)
    await bot.send(ev, msg)

@sv.on_prefix('查马娘生日')
async def search_bir(bot, ev):
    uma_name_tmp = ev.message
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
        f.close()
    with open(os.path.join(os.path.dirname(__file__), 'replace_dict.json'), 'r', encoding = 'UTF-8') as af:
        replace_data = json.load(af)
        af.close()
    uma_bir = ''
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for uma_name in name_list:
        if f_data[uma_name]['category'] == 'umamusume':
            other_name_list = list(replace_data[uma_name])
            cn_name = f_data[uma_name]['cn_name'] if f_data[uma_name]['cn_name'] else f_data[uma_name]['jp_name']
            if str(uma_name) == str(uma_name_tmp) or str(cn_name) == str(uma_name_tmp) or str(uma_name_tmp) in other_name_list:
                cn_name_tmp = cn_name
                uma_bir = f_data[uma_name]['bir']
    if not uma_bir:
        msg = f'这只马娘不存在或没有生日数据'
        await bot.finish(ev, msg)
    msg = f'{cn_name_tmp}的生日是：{uma_bir}'
    await bot.send(ev, msg)

@sv.on_prefix('查生日马娘')
async def search_uma(bot, ev):
    uma_bir_tmp = ev.message
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
        f.close()
    uma_list = []
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for uma_name in name_list:
        if f_data[uma_name]['category'] == 'umamusume':
            if str(f_data[uma_name]['bir']) == str(uma_bir_tmp):
                cn_name = f_data[uma_name]['cn_name'] if f_data[uma_name]['cn_name'] else f_data[uma_name]['jp_name']
                uma_list.append(cn_name)
    if not uma_list:
        msg = f'这天没有马娘生日哟'
        await bot.finish(ev, msg)
    msg = f'{uma_bir_tmp}生日的马娘有：\n' + ' | '.join(uma_list)
    await bot.send(ev, msg)

@svbr.scheduled_job('cron', hour='8', minute='31')
async def push_bir():
    bot = hoshino.get_bot()
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
    tod = datetime.datetime.now().strftime('%m-%d')
    tod_list = tod.split('-', 1)
    tod = '-'.join(str(int(tod_num, 10)) for tod_num in tod_list)
    tod_list = []
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for uma_name in name_list:
        if f_data[uma_name]['category'] == 'umamusume':
            if f_data[uma_name]['bir'] == str(tod):
                cn_name = f_data[uma_name]['cn_name'] if f_data[uma_name]['cn_name'] else f_data[uma_name]['jp_name']
                tod_list.append(cn_name)
    if not tod_list:
        sv.logger.info(f'今天没有马娘生日哟')
        return
    msg = '今天生日的马娘有：\n' + ' | '.join(tod_list)
    await svbr.broadcast(msg, 'uma_bir_push', 0.2)

@sv.on_prefix('查角色')
async def get_single_info(bot, ev):
    alltext = ev.message.extract_plain_text()
    try:
        text_list = alltext.split(' ', 1)
    except:
        msg = f'命令格式输入错误，请参考“马娘数据帮助”发送命令！'
        await bot.finish(ev, msg)
    info_type = text_list[0]
    if info_type not in ['id', '日文名', '中文名', '英文名', '分类', '语音', '头像', 'cv', '身高', '体重', '三围', '适应性', '详细信息', \
        '原案', '决胜服', '制服']:
        return
    uma_name_tmp = text_list[1]
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
        f.close()
    with open(os.path.join(os.path.dirname(__file__), 'replace_dict.json'), 'r', encoding = 'UTF-8') as af:
        replace_data = json.load(af)
        af.close()
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    msg = ''
    for uma_name in name_list:
        other_name_list = list(replace_data[uma_name])
        cn_name = f_data[uma_name]['cn_name'] if f_data[uma_name]['cn_name'] else f_data[uma_name]['jp_name']
        if str(uma_name) == str(uma_name_tmp) or str(cn_name) == str(uma_name_tmp) or str(uma_name_tmp) in other_name_list:
            if info_type == 'id':
                id = f_data[uma_name]['id']
                msg = f'{uma_name_tmp}的角色id为{id}'
            elif info_type == '日文名':
                jp_name = f_data[uma_name]['jp_name']
                msg = f'{uma_name_tmp}的日文名为{jp_name}'
            elif info_type == '中文名':
                cn_name = f_data[uma_name]['cn_name']
                if not cn_name:
                    msg = f'{uma_name_tmp}暂时还没有中文名哟'
                    await bot.finish(ev, msg)
                msg = f'{uma_name_tmp}的中文名为{cn_name}'
            elif info_type == '英文名':
                en_name = str(uma_name)
                msg = f'{uma_name_tmp}的英文名为{en_name}'
            elif info_type == '分类':
                category_tmp = str(f_data[uma_name]['category'])
                category = '赛马娘' if category_tmp == 'umamusume' else '学园关系角色'
                msg = f'{uma_name_tmp}的角色分类为{category}'
            elif info_type == '语音':
                voice = f_data[uma_name]['voice']
                if not voice:
                    msg = f'{uma_name_tmp}暂时还没有语音哟'
                    await bot.finish(ev, msg)
                msg = MessageSegment.record(file = voice)
            elif info_type == '头像':
                sns_icon = f_data[uma_name]['sns_icon']
                msg = MessageSegment.image(file = sns_icon)
            elif info_type == 'cv':
                cv = f_data[uma_name]['cv']
                if not cv:
                    msg = f'{uma_name_tmp}暂时还没公布cv哟'
                    await bot.finish(ev, msg)
                msg = f'{uma_name_tmp}的cv是:\n{cv}'
            elif info_type == '身高':
                height = f_data[uma_name]['height']
                if not height:
                    msg = f'{uma_name_tmp}暂时还没公布身高哟'
                    await bot.finish(ev, msg)
                msg = f'{uma_name_tmp}的身高是:\n{height}cm'
            elif info_type == '体重':
                weight = f_data[uma_name]['weight']
                if not weight:
                    msg = f'{uma_name_tmp}暂时还没公布体重哟'
                    await bot.finish(ev, msg)
                msg = f'{uma_name_tmp}的体重是:\n{weight}'
            elif info_type == '三围':
                measurements = f_data[uma_name]['measurements']
                if not measurements:
                    msg = f'{uma_name_tmp}暂时还没公布三围哟'
                    await bot.finish(ev, msg)
                msg = f'{uma_name_tmp}的三围是:\n{measurements}'
            elif info_type == '制服':
                uniform_img = f_data[uma_name]['uniform_img']
                if not uniform_img:
                    msg = f'{uma_name_tmp}暂时还没公布制服哟'
                    await bot.finish(ev, msg)
                msg = MessageSegment.image(file = uniform_img)
            elif info_type == '决胜服':
                winning_suit_img = f_data[uma_name]['winning_suit_img']
                if not winning_suit_img:
                    msg = f'{uma_name_tmp}暂时还没公布决胜服哟'
                    await bot.finish(ev, msg)
                msg = MessageSegment.image(file = winning_suit_img)
            elif info_type == '原案':
                original_img = f_data[uma_name]['original_img']
                if not original_img:
                    msg = f'{uma_name_tmp}暂时还没公布原案哟'
                    await bot.finish(ev, msg)
                msg = MessageSegment.image(file = original_img)
            elif info_type == '适应性':
                img_tmp = await get_adaptability(uma_name, f_data)
                img = pic2b64(img_tmp)
                if not img:
                    msg = f'{uma_name_tmp}暂时还没有适应性数据哟'
                    await bot.finish(ev, msg)
                msg = MessageSegment.image(img)
            elif info_type == '详细信息':
                img_tmp = await get_detail(uma_name, f_data)
                img = pic2b64(img_tmp)
                if not img:
                    msg = f'出现错误！未获取到详细信息！请到Github仓库反馈！'
                    await bot.finish(ev, msg)
                msg = MessageSegment.image(img)
    if not msg:
        msg = f'这个角色可能不存在或者角色名称对不上'
    await bot.send(ev, msg)

@sv.on_fullmatch('手动更新马娘数据')
async def update_info(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.send(ev, msg)
        return
    if not os.path.exists(current_dir):
        sv.logger.info('本地配置文件不存在，正在开始创建')
        data = {}
        with open(current_dir, 'w', encoding = 'UTF-8') as af:
            json.dump(data, af, indent=4, ensure_ascii=False)
        sv.logger.info('本地配置文件创建完成，开始更新数据库数据')
    if ENABLE_OCR_SPACE:
        msg = '正在开始更新马娘数据库\n由于使用了ocrspace接口，可能不稳定，稍后会将部分图片保存至本地res目录下的uma_bir文件夹'
        if not APIKEY:
            msg = '您已使用了ocrspace接口，但未获取到APIKEY，请到`spider.py`添加后重启hoshino再使用本功能。\n若不需要请到`spider.py`关闭ocrspace接口'
            await bot.finish(ev, msg)
    else:
        # msg = '正在开始更新马娘数据库\n由于使用了自带 QQ接口，比较稳定，但会发送私聊图片至维护组QQ，不会将图片保存在本地'
        msg = 'QQ接口目前有有尚未解决的问题因此不可用！（近期应该都解决不了）请换ocrspace接口使用！'
        await bot.finish(ev, msg)
    await bot.send(ev, msg)
    try:
        except_uma = await uma_spider()
        if not except_uma:
            msg = f'马娘数据库更新完成，开始更新对应中文名'
            sv.logger.info(msg)
            await bot.send(ev, msg)
        else:
            msg = f'马娘数据库更新在更新{except_uma}时遇到问题，1分钟后将从该马娘开始继续更新'
            sv.logger.info(msg)
            await bot.send(ev, msg)
            await asyncio.sleep(60)
            await auto_update_info()
            return
    except Exception as e:
        msg = f'马娘数据库更新失败，将在1分钟后继续自动更新，原因：{e}'
        sv.logger.info(msg)
        traceback.print_exc()
        await bot.send(ev, msg)
        await asyncio.sleep(60)
        await auto_update_info()
        return
    await get_cn()
    msg = '马娘数据库中文名更新完成！任务结束！'
    sv.logger.info(msg)
    await bot.send(ev, msg)

# 自动更新
@sv.scheduled_job('cron', hour='1', minute='31')
async def auto_update_info():
    bot = hoshino.get_bot()
    superid = hoshino.config.SUPERUSERS[0]
    sv.logger.info(f'开始自动更新马娘数据库')
    try:
        except_uma = await uma_spider()
        if not except_uma:
            msg = f'马娘数据库自动更新完成，开始更新对应中文名'
            sv.logger.info(msg)
            await bot.send_private_msg(user_id=superid, message=msg)
        else:
            msg = f'马娘数据库更新在更新{except_uma}时遇到问题，1分钟后将从该马娘开始继续更新'
            sv.logger.info(msg)
            await bot.send_private_msg(user_id=superid, message=msg)
            await asyncio.sleep(60)
            await auto_update_info()
            return
    except Exception as e:
        msg = f'马娘数据库自动更新失败，将在1分钟后继续自动更新，原因：{e}'
        sv.logger.info(msg)
        await bot.send_private_msg(user_id=superid, message=msg)
        await asyncio.sleep(60)
        await auto_update_info()
        return
    await get_cn()
    msg = '马娘数据库中文名更新完成！任务结束！'
    sv.logger.info(msg)
    await bot.send_private_msg(user_id=superid, message=msg)