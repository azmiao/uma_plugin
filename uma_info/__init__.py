import platform
from collections import defaultdict

from yuiChyan import base_res_path, LakePermissionException
from yuiChyan.permission import check_permission, SUPERUSER
from yuiChyan.service import Service
from yuiChyan.util import pic2b64
from .adaptability import get_adaptability
from .detail_class import *
from .detail_info import get_detail
from .info_utils import *
from .spider import uma_update
from ..plugin_utils.base_util import get_img_cq

current_dir = os.path.join(os.path.dirname(__file__), 'config_v2.json')
date_format = '%#m月%#d日' if platform.system() == 'Windows' else '%-m月%-d日'

sv = Service('uma_info')
sv_br = Service('uma_bir_push', use_exclude=False)


@sv.on_match('马娘数据帮助')
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)


@sv.on_match('查今天生日马娘')
async def get_tod(bot, ev):
    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    rep_dir = os.path.join(os.path.dirname(__file__), 'replace_dict.json')
    with open(rep_dir, 'r', encoding='UTF-8') as file:
        replace_data = json.load(file)

    # 今天
    today = datetime.now().strftime(date_format)

    # 解析处理
    uma_name_list = []
    for uma_raw in f_data.values():
        print(uma_raw)
        uma = uma_from_dict(uma_raw)
        if not uma.category or 'ウマ娘' not in uma.category:
            continue
        if uma.birthday and today == uma.birthday:
            uma_name_list.append(await query_uma_name(uma, replace_data))

    # 结果
    if not uma_name_list:
        msg = f'今天没有马娘生日哟'
    else:
        msg = '今天生日的马娘有：\n' + ' | '.join(uma_name_list)
    await bot.send(ev, msg)


@sv.on_prefix('查马娘生日')
async def search_bir(bot, ev):
    name_raw = str(ev.message).strip()
    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    rep_dir = os.path.join(os.path.dirname(__file__), 'replace_dict.json')
    with open(rep_dir, 'r', encoding='UTF-8') as file:
        replace_data = json.load(file)

    # 查询名称
    uma = await query_uma_by_name(name_raw, f_data, replace_data)
    if not uma:
        msg = f'这只马娘不存在哦'
    else:
        birthday = uma.birthday
        uma_name = await query_uma_name(uma, replace_data)
        if birthday:
            msg = f'{uma_name}的生日是：{birthday}'
        else:
            msg = f'{uma_name}还没有生日数据哦！'
    await bot.send(ev, msg)


@sv.on_prefix('查生日马娘')
async def search_uma(bot, ev):
    uma_bir_tmp = str(ev.message).strip()
    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    rep_dir = os.path.join(os.path.dirname(__file__), 'replace_dict.json')
    with open(rep_dir, 'r', encoding='UTF-8') as file:
        replace_data = json.load(file)

    # 解析日期
    try:
        date = datetime.strptime(uma_bir_tmp, '%m-%d')
        formatted_date = date.strftime(date_format)
    except Exception as _:
        await bot.send(ev, f'时间解析失败，请检查输入日期：' + uma_bir_tmp)
        return

    # 分组
    uma_list = [uma_from_dict(uma) for uma in f_data.values()]
    grouped_uma_dict = defaultdict(list, {uma.birthday: [] for uma in uma_list if uma.birthday})
    for uma in uma_list:
        grouped_uma_dict[uma.birthday].append(uma)

    # 获取当天的
    uma_name_list = [await query_uma_name(uma, replace_data) for uma in grouped_uma_dict.get(formatted_date, [])]

    if not uma_name_list:
        msg = f'这天没有马娘生日哟'
    else:
        msg = f'{formatted_date} 生日的马娘有：\n' + ' | '.join(uma_name_list)
    await bot.send(ev, msg)


@sv_br.scheduled_job(hour='8', minute='31')
async def push_bir():
    group_list = await sv_br.get_enable_groups()
    if not group_list:
        sv_br.logger.info('所有群均已禁用马娘生日推送服务，将跳过')
        return

    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    rep_dir = os.path.join(os.path.dirname(__file__), 'replace_dict.json')
    with open(rep_dir, 'r', encoding='UTF-8') as file:
        replace_data = json.load(file)

    today = datetime.now().strftime(date_format)

    # 分组
    uma_list = [uma_from_dict(uma) for uma in f_data.values()]
    grouped_uma_dict = defaultdict(list, {uma.birthday: [] for uma in uma_list if uma.birthday})
    for uma in uma_list:
        grouped_uma_dict[uma.birthday].append(uma)

    # 获取当天的
    uma_name_list = [await query_uma_name(uma, replace_data) for uma in grouped_uma_dict.get(today, [])]

    if not uma_name_list:
        sv_br.logger.info(f'今天没有马娘生日哟')
        return
    msg = '今天生日的马娘有：\n' + ' | '.join(uma_name_list)
    await sv_br.broadcast(msg, 'uma_bir_push', 0.2)


@sv.on_prefix('查角色')
async def get_single_info(bot, ev):
    all_text = ev.message.extract_plain_text()
    try:
        text_list = all_text.split(' ', 1)
    except:
        msg = f'命令格式输入错误，请参考“马娘数据帮助”发送命令！'
        await bot.send(ev, msg)
        return
    info_type = text_list[0]
    if info_type not in ['id', '日文名', '中文名', '英文名', '分类', '语音', '头像', 'cv', '身高',
                         '体重', '三围', '适应性', '详细信息', '原案', '决胜服', '制服']:
        return
    uma_name_tmp = text_list[1]

    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    rep_dir = os.path.join(os.path.dirname(__file__), 'replace_dict.json')
    with open(rep_dir, 'r', encoding='UTF-8') as file:
        replace_data = json.load(file)

    uma = await query_uma_by_name(uma_name_tmp, f_data, replace_data)
    if not uma:
        msg = f'角色[{uma_name_tmp}]不存在哦'
        await bot.send(ev, msg)
        return

    msg = ''
    if info_type == 'id':
        uma_id = uma.id
        msg = f'{uma_name_tmp}的角色id为：\n{uma_id}'
    elif info_type == '日文名':
        jp_name = uma.name
        msg = f'{uma_name_tmp}的日文名为：\n{jp_name}'
    elif info_type == '中文名':
        replace_name_list = replace_data.get(uma.id, [])
        replace_name = replace_name_list[0] if replace_name_list else None
        cn_name = uma.cn_name if uma.cn_name else replace_name
        if not cn_name:
            msg = f'{uma_name_tmp}暂时还没有中文名哟'
        else:
            msg = f'{uma_name_tmp}的中文名为：\n{cn_name}'
    elif info_type == '英文名':
        en_name = uma.en
        msg = f'{uma_name_tmp}的英文名为：\n{en_name}'
    elif info_type == '分类':
        category_list = uma.category
        if not category_list:
            msg = f'{uma_name_tmp}的暂时没有角色分类哟'
        else:
            msg = f'{uma_name_tmp}的角色分类为：\n{" | ".join(category_list)}'
    elif info_type == '语音':
        voice = uma.voice.url
        if not voice:
            msg = f'{uma_name_tmp}暂时还没有语音哟'
        else:
            res_path = os.path.join(base_res_path, 'umamusume')
            save_path = os.path.join(res_path, 'base_data', 'voice_data')
            mp3_name = uma.id + '.mp3'
            voice_file = os.path.join(save_path, mp3_name)
            msg = f'[CQ:record,file=file:///{os.path.abspath(voice_file)}]'
    elif info_type == '头像':
        icon = uma.download.icon.url
        msg = f'[CQ:image,file={icon}]'
    elif info_type == 'cv':
        cv = uma.cv
        if not cv:
            msg = f'{uma_name_tmp}暂时还没公布cv哟'
        else:
            msg = f'{uma_name_tmp}的cv是：\n{cv}'
    elif info_type == '身高':
        height = uma.height
        if not height:
            msg = f'{uma_name_tmp}暂时还没公布身高哟'
        else:
            msg = f'{uma_name_tmp}的身高是：\n{height}'
    elif info_type == '体重':
        weight = uma.weight
        if not weight:
            msg = f'{uma_name_tmp}暂时还没公布体重哟'
        else:
            msg = f'{uma_name_tmp}的体重是：\n{weight}'
    elif info_type == '三围':
        size = uma.size
        if not size:
            msg = f'{uma_name_tmp}暂时还没公布三围哟'
        else:
            msg = f'{uma_name_tmp}的三围是：\n{size}'
    elif info_type == '制服':
        visual_list = uma.visual
        image_dict = {visual.name.title: visual.image.url for visual in visual_list if visual.name.title}
        uniform_img = image_dict.get('制服', None)
        if not uniform_img:
            msg = f'{uma_name_tmp}暂时还没公布制服哟'
        else:
            msg = f'[CQ:image,file={uniform_img}]'
    elif info_type == '决胜服':
        visual_list = uma.visual
        image_dict = {visual.name.title: visual.image.url for visual in visual_list if visual.name.title}
        winning_suit_img = image_dict.get('勝負服', None)
        if not winning_suit_img:
            msg = f'{uma_name_tmp}暂时还没公布决胜服哟'
        else:
            msg = f'[CQ:image,file={winning_suit_img}]'
    elif info_type == '原案':
        visual_list = uma.visual
        image_dict = {visual.name.title: visual.image.url for visual in visual_list if visual.name.title}
        original_img = image_dict.get('原案', None)
        if not original_img:
            msg = f'{uma_name_tmp}暂时还没公布原案哟'
        else:
            msg = f'[CQ:image,file={original_img}]'
    elif info_type == '适应性':
        img_tmp = await get_adaptability(uma.id, f_data)
        img = pic2b64(img_tmp)
        if not img:
            msg = f'{uma_name_tmp}暂时还没有适应性数据哟'
        else:
            msg = f'[CQ:image,file={img}]'
    elif info_type == '详细信息':
        img_tmp = await get_detail(uma.id, f_data)
        img = pic2b64(img_tmp)
        if not img:
            msg = f'出现错误！未获取到详细信息！请到Github仓库反馈！'
        else:
            msg = f'[CQ:image,file={img}]'
    await bot.send(ev, msg)


@sv.on_match('手动更新马娘数据')
async def update_info(bot, ev):
    if not check_permission(ev,  SUPERUSER):
        raise LakePermissionException(ev, None, SUPERUSER)

    try:
        await uma_update(current_dir)
        msg = '马娘数据更新完成'
    except Exception as e:
        msg = f'马娘数据更新失败{e}'
    await bot.send(ev, msg)
