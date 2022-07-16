import json
import os

from hoshino import Service, priv
from .caculate import judge_name, get_relation
from .update_type import update as com_update

sv = Service('uma_compatibility', help_='![](https://img.gejiba.com/images/3aff9b9882954e3f8206328444627a93.png)')

# 帮助界面
@sv.on_fullmatch("马娘相性帮助")
async def help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = f'[CQ:image,file=file:///{os.path.abspath(img_path)}]'
    await bot.send(ev, sv_help)

@sv.on_prefix('查相性')
async def caculate(bot, ev):
    alltext = ev.message.extract_plain_text()
    if not alltext:
        await bot.finish(ev, '格式错误，请参考“马娘相性帮助”')
    text_list = alltext.split(' ')
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info/config.json'), 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
        f.close()
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info/replace_dict.json'), 'r', encoding = 'UTF-8') as af:
        replace_data = json.load(af)
        af.close()
    with open(os.path.join(os.path.dirname(__file__), 'relation_type.json'), 'r', encoding = 'UTF-8') as sf:
        r_data_list = json.load(sf)
        sf.close()
    self = judge_name(text_list[0], f_data, replace_data)
    mother = judge_name(text_list[1], f_data, replace_data)
    # 仅查两者之间的相性
    try:
        grandmother = text_list[2]
    except:
        msg_list = []
        if not self:
            msg_list.append(f'输入错误，你输入的 马娘1：{text_list[0]} 无法识别！')
        if not mother:
            msg_list.append(f'输入错误，你输入的 马娘2：{text_list[1]} 无法识别！')
        if msg_list:
            msg = '\n'.join(msg_list)
            await bot.finish(ev, msg)
        relation = get_relation(r_data_list, [self, mother])
        msg = f'{self} 和 {mother} 的相性值为：{relation}'
        await bot.finish(ev, msg)
    # 查总相性
    grandmother = judge_name(text_list[2], f_data, replace_data)
    grandfather = judge_name(text_list[3], f_data, replace_data)
    father = judge_name(text_list[4], f_data, replace_data)
    grandmother_in_law = judge_name(text_list[5], f_data, replace_data)
    grandfather_in_law = judge_name(text_list[6], f_data, replace_data)
    msg_list = []
    if not self:
        msg_list.append(f'输入错误，你输入的 本体：{text_list[0]} 无法识别！')
    if not mother:
        msg_list.append(f'输入错误，你输入的 父母1：{text_list[1]} 无法识别！')
    if not grandmother:
        msg_list.append(f'输入错误，你输入的 祖父母1：{text_list[2]} 无法识别！')
    if not grandfather:
        msg_list.append(f'输入错误，你输入的 祖父母2：{text_list[3]} 无法识别！')
    if not father:
        msg_list.append(f'输入错误，你输入的 父母2：{text_list[4]} 无法识别！')
    if not grandmother_in_law:
        msg_list.append(f'输入错误，你输入的 祖父母3：{text_list[5]} 无法识别！')
    if not grandfather_in_law:
        msg_list.append(f'输入错误，你输入的 祖父母4：{text_list[6]} 无法识别！')
    if msg_list:
        msg = '\n'.join(msg_list)
        await bot.finish(ev, msg)
    try:
        winsaddle = int(text_list[7])
    except:
        winsaddle = 0
    relation = get_relation(r_data_list, [self, mother])
    relation += get_relation(r_data_list, [self, mother, grandmother])
    relation += get_relation(r_data_list, [self, mother, grandfather])
    relation += get_relation(r_data_list, [self, father])
    relation += get_relation(r_data_list, [self, father, grandmother_in_law])
    relation += get_relation(r_data_list, [self, father, grandfather_in_law])
    relation += get_relation(r_data_list, [mother, father])
    end_relation = relation + winsaddle
    if end_relation < 51 and end_relation >= 0:
        msg = f'最终计算出的相性值为：{end_relation}\n匹配符号：△'
    elif end_relation > 51 and end_relation < 151:
        msg = f'最终计算出的相性值为：{end_relation}\n匹配符号：◯'
    else:
        msg = f'最终计算出的相性值为：{end_relation}\n匹配符号：◎'
    await bot.send(ev, msg)

@sv.on_prefix('相性榜')
async def best_com(bot, ev):
    self_tmp = ev.message
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info/config.json'), 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
        f.close()
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info/replace_dict.json'), 'r', encoding = 'UTF-8') as af:
        replace_data = json.load(af)
        af.close()
    self = judge_name(self_tmp, f_data, replace_data)
    if not self:
        msg = f'输入错误，你输入的 马娘：{self_tmp} 无法识别！'
        await bot.finish(ev, msg)
    with open(os.path.join(os.path.dirname(__file__), 'relation_type.json'), 'r', encoding = 'UTF-8') as sf:
        r_data_list = json.load(sf)
        sf.close()
    relation_dict = {}
    for uma_name in name_list:
        cn_name = f_data[uma_name]['cn_name']
        if cn_name:
            relation = get_relation(r_data_list, [self, cn_name])
            relation_dict[cn_name] = relation
    relation_order_list = sorted(relation_dict.items(), key=lambda x:x[1], reverse=True)
    msg, i = f'和 {self} 相性前十的马娘为：', 0
    for name_tuple in relation_order_list:
        cn_name = name_tuple[0]
        relation = name_tuple[1]
        if cn_name != self:
            if i < 10:
                msg += f'\n{cn_name}：相性值 {str(relation)}'
                i += 1
            else:
                break
    await bot.send(ev, msg)

@sv.on_fullmatch("手动更新相性信息")
async def update_com(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.finish(ev, msg)
    await com_update()
    await bot.send(ev, f'已更新至最新相性组文件')