import os
import json
import base64

from hoshino import Service, priv, R
from .update_skills import del_img, update_info, del_img
from .generate import get_skill_list, get_skill_info
from ..plugin_utils.base_util import get_img_cq

current_dir = os.path.join(os.path.dirname(__file__), f'skills_config.json')

# 分类
rarity = ['普通', '传说', '独特', '普通·继承', '独特·继承', '剧情', '活动']
limit = ['通用', '短距离', '英里', '中距离', '长距离', '泥地', '逃马', '先行', '差行', '追马']
color = ['绿色', '紫色', '黄色', '蓝色', '红色']
skill_type = ['被动（速度）', '被动（耐力）', '被动（力量）', '被动（毅力）', '被动（智力）',
    '耐力恢复', '速度', '加速度', '出闸', '视野', '切换跑道',
    '妨害（速度）', '妨害（加速度）', '妨害（心态）', '妨害（智力）', '妨害（耐力恢复）', '妨害（视野）',
    '(未知)'
]
params = rarity + limit + color + skill_type

sv = Service('uma_skills')
with open(os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png'), 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
sv.help = f'![](data:image/jpeg;base64,{s})'

@sv.on_fullmatch('马娘技能帮助')
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)

@sv.on_prefix('查技能')
async def check_skill(bot, ev):
    alltext = ev.message.extract_plain_text().replace(')', '）').replace('(', '（')
    skill_list = alltext.split(' ')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        f_data = json.load(f)
    if not skill_list:
        return
    elif len(skill_list) == 1 and not all(elem in params for elem in skill_list):
        # 按技能名查询
        skill_name = skill_list[0]
        msg = await get_skill_info(skill_name, f_data)
    else:
        # 多于一个参数或在参数列表中就按分类查询
        # 去重
        skill_list = list(set(skill_list))
        rarity_list, limit_list, color_list, skill_type_list = [], [], [], []
        for param in skill_list:
            if param in rarity:
                rarity_list.append(param)
            elif param in limit:
                limit_list.append(param)
            elif param in color:
                color_list.append(param)
            elif param in skill_type:
                skill_type_list.append(param)
        # 未识别出技能类型
        if not (rarity_list + limit_list + color_list + skill_type_list):
            await bot.finish(ev, f'没有识别出任何检索条件呢')
        # 当 稀有度 或 条件限制 或 颜色 不止一个参数输入时，那返回必然无结果
        if len(rarity_list) > 1 or len(limit_list) > 1 or len(color_list) > 1:
            await bot.finish(ev, f'没有搜索出任何马娘技能呢，请确保你输入的检索条件正确且无冲突！')
        msg = await get_skill_list(
            rarity_list[0] if rarity_list else '',
            limit_list[0] if limit_list else '',
            color_list[0] if color_list else '',
            skill_type_list,
            f_data
        )
    await bot.send(ev, msg)

# 手动更新本地数据
@sv.on_fullmatch('手动更新马娘技能')
async def force_update(bot, ev):
    if not priv.check_priv(ev, priv.SUPERUSER):
        msg = '很抱歉您没有权限进行此操作，该操作仅限维护组'
        await bot.finish(ev, msg)
    try:
        await update_info()
        await del_img(R.img('umamusume').path)
        await bot.send(ev, '马娘技能信息刷新完成')
    except Exception as e:
        await bot.send(ev, f'马娘技能信息刷新失败：{e}')