import json
import os

from .gacha_class import Gacha
from .util import get_pool, get_chart_name_dict

# 抽卡目标 | 每次池子更新都将会重置
target_path = os.path.join(os.path.dirname(__file__), 'gacha_target.json')
if not os.path.exists(target_path):
    with open(target_path, 'w', encoding='utf-8') as default_f:
        # noinspection PyTypeChecker
        json.dump({}, default_f, ensure_ascii=False, indent=4)


# 设置目标配置
async def set_target_config(user_id: str, target_id_list: list):
    with open(target_path, 'r', encoding='utf-8') as f:
        target_config = json.load(f)
    target_config[user_id] = target_id_list
    with open(target_path, 'w', encoding='utf-8') as f:
        # noinspection PyTypeChecker
        json.dump(target_config, f, ensure_ascii=False, indent=4)


# 清除目标
async def reset_target_config(user_id: str):
    with open(target_path, 'r', encoding='utf-8') as f:
        target_config = json.load(f)
    target_config[user_id] = []
    with open(target_path, 'w', encoding='utf-8') as f:
        # noinspection PyTypeChecker
        json.dump(target_config, f, ensure_ascii=False, indent=4)


# 查询目标名称列表
async def query_target_config(user_id: str) -> list:
    with open(target_path, 'r', encoding='utf-8') as f:
        target_config = json.load(f)
    _, chart_id_dict = await get_chart_name_dict()
    chart_name_list = [chart_id_dict.get(key, '') for key in target_config.get(user_id, [])]
    if '' in chart_name_list:
        chart_name_list.remove('')
    return chart_name_list


# 获取当前UP的支援卡名称列表
async def get_current_up_name(group_id) -> list:
    server, pool_id = await get_pool(group_id)
    pool = Gacha.get_pool(pool_id, server)
    chart_up = pool.get('chart_up', {})
    return chart_up.get('SSR', [])


# 获取当前UP的支援卡ID-名称关系字典
async def get_current_up_id_dict(group_id) -> dict:
    current_up_name = await get_current_up_name(group_id)
    chart_name_dict, _ = await get_chart_name_dict()
    chart_up_id_dict = {chart_name_dict.get(value, ''): value for value in current_up_name}
    return chart_up_id_dict
