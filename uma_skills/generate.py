import os

from fuzzywuzzy import process

from yuiChyan import logger, base_res_path
from yuiChyan.util.chart_generator import create_table, save_fig_as_image
from ..plugin_utils.base_util import get_img_cq


async def create_msg(skill_name: str, f_data):
    msg = f'''
技能名：{skill_name}
中文名：{f_data['skills'][skill_name]['中文名']}
稀有度：{f_data['skills'][skill_name]['稀有度']}
颜色：{f_data['skills'][skill_name]['颜色']}
繁中译名：{f_data['skills'][skill_name]['繁中译名']}
条件限制：{f_data['skills'][skill_name]['条件限制']}
技能数值：{f_data['skills'][skill_name]['技能数值']}
持续时间：{f_data['skills'][skill_name]['持续时间']}
需要PT：{f_data['skills'][skill_name]['需要PT']}
评价分：{f_data['skills'][skill_name]['评价分']}
PT评价比：{f_data['skills'][skill_name]['PT评价比']}
触发条件：{f_data['skills'][skill_name]['触发条件']}
技能类型：{f_data['skills'][skill_name]['技能类型']}
    '''.strip()
    return msg


# 获取马娘技能内容
async def get_skill_info(skill_name: str, f_data):
    jp_name_list = list(f_data['skills'].keys())
    # 若名字在日文名里
    if skill_name in jp_name_list:
        msg = await create_msg(skill_name, f_data)
        return msg
    cn_name_dict = f_data['cn_name_dict']
    tw_name_dict = f_data['tw_name_dict']
    cn_name_list = list(cn_name_dict.keys())
    tw_name_list = list(tw_name_dict.keys())
    # 若名字在中文名里
    if skill_name in cn_name_list:
        jp_name_tmp = cn_name_dict[skill_name]
        msg = await create_msg(jp_name_tmp, f_data)
        return msg
    # 若名字在繁中文名里
    if skill_name in tw_name_list:
        jp_name_tmp = tw_name_dict[skill_name]
        msg = await create_msg(jp_name_tmp, f_data)
        return msg
    # 全部中日名字的列表
    all_name_list = jp_name_list + cn_name_list + tw_name_list
    # 去重
    all_name_list = list(set(all_name_list))
    # 如果都不在，就进行相似度检测
    skill_name, score = process.extractOne(skill_name, all_name_list)
    msg = f'未找到相关技能，您有{score}%的可能在查询技能：{skill_name}'
    return msg


# 获取马娘技能列表
async def get_skill_list(rarity: str, limit: str, color: str, skill_type_list: list, f_data):
    data_dict = {
        'title': '',
        'info': {}
    }
    for skill_jp_name in f_data['skills']:
        # 如果前面三个值为空就等于当前稀有度，以便过判断
        rarity_tmp = rarity if rarity else f_data['skills'][skill_jp_name]['稀有度']
        limit_tmp = limit if limit else f_data['skills'][skill_jp_name]['条件限制']
        color_tmp = color if color else f_data['skills'][skill_jp_name]['颜色']
        # 当前技能类型列表
        text = f_data['skills'][skill_jp_name]['技能类型'].replace('条件1: ', '、').replace('条件2: ', '、').replace(
            '条件3: ', '、')
        currrent_type_list = text.split('、')
        # 去除空值
        currrent_type_list = list(set(currrent_type_list))
        if '' in currrent_type_list:
            currrent_type_list.remove('')
        # 类型列表为空就等于当前列表
        type_list_tmp = skill_type_list if skill_type_list else currrent_type_list
        # 判断条件
        if rarity_tmp == f_data['skills'][skill_jp_name]['稀有度'] and \
                limit_tmp == f_data['skills'][skill_jp_name]['条件限制'] and \
                color_tmp == f_data['skills'][skill_jp_name]['颜色'] and \
                all(elem in currrent_type_list for elem in type_list_tmp):
            data_dict['info'][skill_jp_name] = f_data['skills'][skill_jp_name]
    # 如果未找到任何数据
    if not data_dict['info']:
        return f'没有搜索出任何马娘技能呢，请确保你输入的检索条件正确且无冲突！'
    # 如果结果就一个就不需要合成图片了
    if len(list(data_dict['info'].keys())) == 1:
        jp_name_tmp = list(data_dict['info'].keys())[0]
        msg = await create_msg(jp_name_tmp, f_data)
        return msg
    # 结果大于一个就将所有结果合成一张图片
    name_list = [rarity, limit, color] + skill_type_list
    name_list = list(set(name_list))
    if '' in name_list:
        name_list.remove('')
    # 文件名
    filename_tmp = '_'.join(name_list) + '.png'
    data_dict['title'] = '检索：' + ' + '.join(name_list) + ' 的结果'
    # 图片文件不存在就创建图片
    res_path = os.path.join(base_res_path, 'umamusume')
    img_dir = os.path.join(res_path, 'uma_skills', f'{filename_tmp}')
    if not os.path.exists(img_dir):
        logger.info(f'检测到{filename_tmp}图片不存在正在开始生成')
        await create_img(data_dict, filename_tmp)
        logger.info(f'检测到{filename_tmp}图片生成完成，即将发送图片')
    else:
        logger.info(f'{filename_tmp}图片本地已存在，即将发送图片')
    msg = await get_img_cq(img_dir)
    return msg


# 生成图片
async def create_img(info_data, filename_tmp):
    raw_data = {
        'title': info_data['title'],
        'index_column': 'skill_name',
        'show_columns': {
            'skill_name': '技能名',
            'cn_name': '中文名',
            'rarity': '稀有度',
            'color': '颜色',
            'tw_name': '繁中译名',
            'limit': '条件限制',
            'value': '技能数值',
            'time': '持续时间',
            'point': '评价分',
            'pt': '需要PT',
            'pt_per_point': 'PT评价比',
            'condition': '触发条件',
            'skill_type': '技能类型',
        }
    }

    data_list = []
    for skill_name in list(info_data['info'].keys()):
        cn_name = info_data['info'][skill_name]['中文名']
        rarity = info_data['info'][skill_name]['稀有度'].replace('·', '')
        color = info_data['info'][skill_name]['颜色']
        tw_name = info_data['info'][skill_name]['繁中译名']
        limit = info_data['info'][skill_name]['条件限制']
        value = info_data['info'][skill_name]['技能数值']
        time = info_data['info'][skill_name]['持续时间']
        point = info_data['info'][skill_name]['评价分']
        pt = info_data['info'][skill_name]['需要PT']
        pt_per_point = info_data['info'][skill_name]['PT评价比']
        condition = info_data['info'][skill_name]['触发条件']
        skill_type = info_data['info'][skill_name]['技能类型']

        data_list.append({
            'cn_name': cn_name,
            'rarity': rarity,
            'color': color,
            'tw_name': tw_name,
            'limit': limit,
            'value': value,
            'time': time,
            'point': point,
            'pt': pt,
            'pt_per_point': pt_per_point,
            'condition': condition,
            'skill_type': skill_type
        })
    raw_data['data_list'] = data_list

    fig = await create_table(raw_data)

    res_path = os.path.join(base_res_path, 'umamusume')
    save_dir = os.path.join(res_path, 'uma_skills')
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    path_dir = os.path.join(save_dir, filename_tmp)
    await save_fig_as_image(fig, path_dir)
