from .detail_class import *


# 根据名称查角色
async def query_uma_by_name(name_raw: str, f_data: dict, replace_data: dict) -> Optional[Uma]:
    for uma_raw in f_data.values():
        uma = uma_from_dict(uma_raw)
        if (name_raw in [uma.name, uma.cn_name, uma.en]) or (name_raw in replace_data.get(uma.id, [])):
            return uma
    return None


# 查询角色默认对外展示名称
async def query_uma_name(uma: Uma, replace_data: dict) -> str:
    replace_name_list = replace_data.get(uma.id, [])
    replace_name = replace_name_list[0] if replace_name_list else uma.name
    return uma.cn_name if uma.cn_name else replace_name
