import json
import os

from yuiChyan import logger
from .detail_class import *


async def get_uma_id(name_tmp, need_log: bool = True):
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info')
    current_dir = os.path.join(config_dir, 'config_v2.json')
    with open(current_dir, 'r', encoding='UTF-8') as file:
        f_data = json.load(file)
    rep_dir = os.path.join(config_dir, 'replace_dict.json')
    with open(rep_dir, 'r', encoding='UTF-8') as file:
        replace_data = json.load(file)

    uma = await query_uma_by_name(name_tmp, f_data, replace_data, need_log)
    return uma.id if uma else None


# 根据名称查角色
async def query_uma_by_name(name_raw: str, f_data: dict, replace_data: dict, need_log: bool = True) -> Optional[Uma]:
    for uma_raw in f_data.values():
        uma = uma_from_dict(uma_raw)
        if (name_raw in [uma.name, uma.cn_name, uma.en]) or (name_raw in replace_data.get(uma.id, [])):
            return uma
    if need_log:
        logger.error(f'> uma [{name_raw}] can not be found!')
    return None


# 查询角色默认对外展示名称
async def query_uma_name(uma: Uma, replace_data: dict) -> str:
    replace_name_list = replace_data.get(uma.id, [])
    replace_name = replace_name_list[0] if replace_name_list else uma.name
    return uma.cn_name if uma.cn_name else replace_name
