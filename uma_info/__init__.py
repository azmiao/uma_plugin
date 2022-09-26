import os
import base64
import datetime
import json

from .spider import uma_update
from .adaptability import get_adaptability
from .detail_info import get_detail
from hoshino import Service, priv, R
from hoshino.util import pic2b64
from ..plugin_utils.base_util import get_img_cq

current_dir = os.path.join(os.path.dirname(__file__), 'config.json')

sv = Service('uma_info', enable_on_default = True)
with open(os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png'), 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
sv.help = f'![](data:image/jpeg;base64,{s})'
svbr = Service('uma_bir_push', enable_on_default = False)

@sv.on_fullmatch('马娘数据帮助')
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)

@sv.on_fullmatch('查今天生日马娘')
async def get_tod(bot, ev):
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
    rep_dir = os.path.join(os.path.dirname(__file__), 'replace_dict.json')
    with open(rep_dir, 'r', encoding = 'UTF-8') as f:
        rep_data = json.load(f)
    tod = datetime.datetime.now().strftime('%m-%d')
    tod_list = tod.split('-', 1)
    tod = '-'.join(str(int(tod_num, 10)) for tod_num in tod_list)
    tod_list = []
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for uma_name in name_list:
        if f_data[uma_name]['category'] == 'umamusume':
            if str(f_data[uma_name]['bir']) == str(tod):
                cn_name = f_data[uma_name]['cn_name'] if f_data[uma_name]['cn_name'] else rep_data[uma_name][0]
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
    rep_dir = os.path.join(os.path.dirname(__file__), 'replace_dict.json')
    with open(rep_dir, 'r', encoding = 'UTF-8') as f:
        rep_data = json.load(f)
    uma_list = []
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for uma_name in name_list:
        if f_data[uma_name]['category'] == 'umamusume':
            if str(f_data[uma_name]['bir']) == str(uma_bir_tmp):
                cn_name = f_data[uma_name]['cn_name'] if f_data[uma_name]['cn_name'] else rep_data[uma_name][0]
                uma_list.append(cn_name)
    if not uma_list:
        msg = f'这天没有马娘生日哟'
        await bot.finish(ev, msg)
    msg = f'{uma_bir_tmp}生日的马娘有：\n' + ' | '.join(uma_list)
    await bot.send(ev, msg)

@svbr.scheduled_job('cron', hour='8', minute='31')
async def push_bir():
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
    rep_dir = os.path.join(os.path.dirname(__file__), 'replace_dict.json')
    with open(rep_dir, 'r', encoding = 'UTF-8') as f:
        rep_data = json.load(f)
    tod = datetime.datetime.now().strftime('%m-%d')
    tod_list = tod.split('-', 1)
    tod = '-'.join(str(int(tod_num, 10)) for tod_num in tod_list)
    tod_list = []
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for uma_name in name_list:
        if f_data[uma_name]['category'] == 'umamusume':
            if f_data[uma_name]['bir'] == str(tod):
                cn_name = f_data[uma_name]['cn_name'] if f_data[uma_name]['cn_name'] else rep_data[uma_name][0]
                tod_list.append(cn_name)
    if not tod_list:
        svbr.logger.info(f'今天没有马娘生日哟')
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
                save_path = os.path.join(R.img('umamusume').path, 'base_data/voice_data')
                mp3_name = uma_name + '.mp3'
                voice_file = os.path.join(save_path, mp3_name)
                msg = f'[CQ:record,file=file:///{os.path.abspath(voice_file)}]'
            elif info_type == '头像':
                sns_icon = f_data[uma_name]['sns_icon']
                msg = f'[CQ:image,file={sns_icon}]'
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
                msg = f'[CQ:image,file={uniform_img}]'
            elif info_type == '决胜服':
                winning_suit_img = f_data[uma_name]['winning_suit_img']
                if not winning_suit_img:
                    msg = f'{uma_name_tmp}暂时还没公布决胜服哟'
                    await bot.finish(ev, msg)
                msg = f'[CQ:image,file={winning_suit_img}]'
            elif info_type == '原案':
                original_img = f_data[uma_name]['original_img']
                if not original_img:
                    msg = f'{uma_name_tmp}暂时还没公布原案哟'
                    await bot.finish(ev, msg)
                msg = f'[CQ:image,file={original_img}]'
            elif info_type == '适应性':
                img_tmp = await get_adaptability(uma_name, f_data)
                img = pic2b64(img_tmp)
                if not img:
                    msg = f'{uma_name_tmp}暂时还没有适应性数据哟'
                    await bot.finish(ev, msg)
                msg = f'[CQ:image,file={img}]'
            elif info_type == '详细信息':
                img_tmp = await get_detail(uma_name, f_data)
                img = pic2b64(img_tmp)
                if not img:
                    msg = f'出现错误！未获取到详细信息！请到Github仓库反馈！'
                    await bot.finish(ev, msg)
                msg = f'[CQ:image,file={img}]'
    if not msg:
        msg = f'这个角色可能不存在或者角色名称对不上'
    await bot.send(ev, msg)

@sv.on_fullmatch('手动更新马娘数据')
async def update_info(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.finish(ev, msg)
    await bot.send(ev, '正在更新数据，请耐心等待...')
    try:
        await uma_update(current_dir)
        msg = '马娘数据更新完成'
    except Exception as e:
        msg = f'马娘数据更新失败{e}'
    await bot.send(ev, msg)