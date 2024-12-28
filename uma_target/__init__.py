from yuiChyan.service import Service
from .get_target import get_tar
from ..plugin_utils.base_util import get_img_cq
from ..uma_info.info_utils import *

sv = Service('uma_target')

config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info')
current_dir = os.path.join(config_dir, 'config_v2.json')


@sv.on_match('育成目标帮助')
async def get_help(bot, ev):
    img_path = os.path.join(os.path.dirname(__file__), f'{sv.name}_help.png')
    sv_help = await get_img_cq(img_path)
    await bot.send(ev, sv_help)


@sv.on_prefix('查目标')
async def search_target(bot, ev):
    uma_name_tmp = str(ev.message).strip().replace('-f', '')
    is_force = True if str(ev.message).strip().endswith('-f') else False

    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    rep_dir = os.path.join(config_dir, 'replace_dict.json')
    with open(rep_dir, 'r', encoding='UTF-8') as file:
        replace_data = json.load(file)

    uma = await query_uma_by_name(uma_name_tmp, f_data, replace_data)
    if not uma:
        return

    uma_target = await get_tar(uma.cn_name, is_force)
    if not uma_target:
        msg = f'马娘 [{uma.cn_name}] 暂时没有育成模板呢'
    else:
        msg = uma_target
    await bot.send(ev, msg)
