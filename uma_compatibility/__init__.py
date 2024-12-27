import base64
import json
import os

from yuiChyan import LakePermissionException
from yuiChyan.permission import check_permission, SUPERUSER
from yuiChyan.service import Service
from .caculate import get_relation
from .update_type import update as com_update
from ..plugin_utils.base_util import get_img_cq
from ..uma_info.info_utils import *

sv = Service('uma_compatibility')
with open(os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png'), 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
sv.help = f'![](data:image/jpeg;base64,{s})'

config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info')
current_dir = os.path.join(config_dir, 'config_v2.json')


# 帮助界面
@sv.on_match("马娘相性帮助")
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)


@sv.on_prefix('查相性')
async def calculate(bot, ev):
    all_text = ev.message.extract_plain_text()
    if not all_text:
        await bot.send(ev, '格式错误，请参考“马娘相性帮助”')
        return
    text_list = all_text.split(' ')

    if len(text_list) not in [2, 7, 8]:
        await bot.send(ev, '格式错误，请参考“马娘相性帮助”')
        return

    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    rep_dir = os.path.join(config_dir, 'replace_dict.json')
    with open(rep_dir, 'r', encoding='UTF-8') as file:
        replace_data = json.load(file)
    with open(os.path.join(os.path.dirname(__file__), 'relation_type.json'), 'r', encoding='UTF-8') as sf:
        r_data_list = json.load(sf)

    self_uma = await query_uma_by_name(text_list[0], f_data, replace_data)
    mother_uma = await query_uma_by_name(text_list[1], f_data, replace_data)

    # 仅查两者之间的相性
    if len(text_list) == 2:
        msg_list = []
        if not self_uma:
            msg_list.append(f'输入错误，你输入的 父母1：{text_list[0]} 无法识别！')
        if not mother_uma:
            msg_list.append(f'输入错误，你输入的 父母2：{text_list[1]} 无法识别！')
        if msg_list:
            msg = '\n'.join(msg_list)
            await bot.send(ev, msg)
            return

        self = self_uma.cn_name
        mother = mother_uma.cn_name

        relation = get_relation(r_data_list, [self, mother])
        msg = f'{self} 和 {mother} 的相性值为：{relation}'
        await bot.send(ev, msg)
        return

    # 查总相性
    grandmother_uma = await query_uma_by_name(text_list[2], f_data, replace_data)
    grandfather_uma = await query_uma_by_name(text_list[3], f_data, replace_data)
    father_uma = await query_uma_by_name(text_list[4], f_data, replace_data)
    grandmother_in_law_uma = await query_uma_by_name(text_list[5], f_data, replace_data)
    grandfather_in_law_uma = await query_uma_by_name(text_list[6], f_data, replace_data)

    msg_list = []
    if not self_uma:
        msg_list.append(f'输入错误，你输入的 本体：{text_list[0]} 无法识别！')
    if not mother_uma:
        msg_list.append(f'输入错误，你输入的 父母1：{text_list[1]} 无法识别！')
    if not grandmother_uma:
        msg_list.append(f'输入错误，你输入的 祖父母1：{text_list[2]} 无法识别！')
    if not grandfather_uma:
        msg_list.append(f'输入错误，你输入的 祖父母2：{text_list[3]} 无法识别！')
    if not father_uma:
        msg_list.append(f'输入错误，你输入的 父母2：{text_list[4]} 无法识别！')
    if not grandmother_in_law_uma:
        msg_list.append(f'输入错误，你输入的 祖父母3：{text_list[5]} 无法识别！')
    if not grandfather_in_law_uma:
        msg_list.append(f'输入错误，你输入的 祖父母4：{text_list[6]} 无法识别！')
    if msg_list:
        msg = '\n'.join(msg_list)
        await bot.send(ev, msg)
        return

    try:
        win_saddle = int(text_list[7])
    except:
        win_saddle = 0
    relation = get_relation(r_data_list, [self_uma.cn_name, mother_uma.cn_name])
    relation += get_relation(r_data_list, [self_uma.cn_name, mother_uma.cn_name, grandmother_uma.cn_name])
    relation += get_relation(r_data_list, [self_uma.cn_name, mother_uma.cn_name, grandfather_uma.cn_name])
    relation += get_relation(r_data_list, [self_uma.cn_name, father_uma.cn_name])
    relation += get_relation(r_data_list, [self_uma.cn_name, father_uma.cn_name, grandmother_in_law_uma.cn_name])
    relation += get_relation(r_data_list, [self_uma.cn_name, father_uma.cn_name, grandfather_in_law_uma.cn_name])
    relation += get_relation(r_data_list, [mother_uma.cn_name, father_uma.cn_name])
    end_relation = relation + win_saddle
    if 51 > end_relation >= 0:
        msg = f'最终计算出的相性值为：{end_relation}\n匹配符号：△'
    elif 51 < end_relation < 151:
        msg = f'最终计算出的相性值为：{end_relation}\n匹配符号：◯'
    else:
        msg = f'最终计算出的相性值为：{end_relation}\n匹配符号：◎'
    await bot.send(ev, msg)


@sv.on_prefix('相性榜')
async def best_com(bot, ev):
    self_tmp = str(ev.message).strip()

    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    rep_dir = os.path.join(config_dir, 'replace_dict.json')
    with open(rep_dir, 'r', encoding='UTF-8') as file:
        replace_data = json.load(file)
    with open(os.path.join(os.path.dirname(__file__), 'relation_type.json'), 'r', encoding='UTF-8') as sf:
        r_data_list = json.load(sf)

    self_uma = await query_uma_by_name(self_tmp, f_data, replace_data)
    if not self_uma:
        await bot.send(ev, f'输入错误，你输入的马娘：{self_tmp} 无法识别！')
        return

    relation_dict = {}
    for uma_raw in f_data.values():
        uma = uma_from_dict(uma_raw)
        cn_name = uma.cn_name
        if cn_name:
            relation = get_relation(r_data_list, [self_uma.cn_name, cn_name])
            relation_dict[cn_name] = relation
    relation_order_list = sorted(relation_dict.items(), key=lambda x: x[1], reverse=True)
    msg, i = f'和 {self_uma.cn_name} 相性前十的马娘为：', 0
    for name_tuple in relation_order_list:
        cn_name = name_tuple[0]
        relation = name_tuple[1]
        if cn_name != self_uma.cn_name:
            if i < 10:
                msg += f'\n{cn_name}：相性值 {str(relation)}'
                i += 1
            else:
                break
    await bot.send(ev, msg)


@sv.on_match("手动更新相性信息")
async def update_com(bot, ev):
    if not check_permission(ev,  SUPERUSER):
        raise LakePermissionException(ev, None, SUPERUSER)
    await com_update()
    await bot.send(ev, f'已更新至最新相性组文件')
