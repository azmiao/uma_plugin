import os
import json
import base64

from hoshino import Service
from .get_target import get_tar
from ..plugin_utils.base_util import get_img_cq

sv = Service('uma_target')
with open(os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png'), 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
sv.help = f'![](data:image/jpeg;base64,{s})'

@sv.on_fullmatch('育成目标帮助')
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)

@sv.on_prefix('查目标')
async def search_target(bot, ev):
    uma_name_tmp = str(ev.message).replace('-f', '')
    is_force = True if str(ev.message).endswith('-f') else False
    current_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info/config.json')
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info/replace_dict.json'), 'r', encoding = 'UTF-8') as af:
        replace_data = json.load(af)
    uma_target = ''
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for uma_name in name_list:
        if f_data[uma_name]['category'] == 'umamusume':
            other_name_list = list(replace_data[uma_name]) if uma_name in replace_data else []
            if f_data[uma_name]['cn_name']:
                cn_name = f_data[uma_name]['cn_name']
            else:
                continue
            if str(uma_name) == uma_name_tmp or str(cn_name) == uma_name_tmp or\
                str(f_data[uma_name]['jp_name']) == uma_name_tmp or str(uma_name_tmp) in other_name_list:
                try:
                    uma_target = await get_tar(cn_name, is_force)
                except:
                    await bot.finish(ev, f'这只马娘不存在或暂时没有育成目标')
    if not uma_target:
        await bot.finish(ev, f'这只马娘不存在或暂时没有育成目标')
    await bot.send(ev, uma_target)