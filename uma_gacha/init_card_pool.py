from typing import Any
from .config import DRAW_PATH
from pathlib import Path
from .util import remove_prohibited_str
try:
    import ujson as json
except ModuleNotFoundError:
    import json


def init_game_pool(game: str, data: dict, Operator: Any):
    tmp_lst = []
    if game == 'pretty':
        for key in data.keys():
            tmp_lst.append(Operator(name=key, star=data[key]['初始星级'], limited=False))
    if game == 'pretty_card':
        for key in data.keys():
            limited = False
            if '卡池' not in data[key]['获取方式']:
                limited = True
            if not data[key]['获取方式']:
                limited = False
            tmp_lst.append(Operator(name=remove_prohibited_str(data[key]['中文名']), star=len(data[key]['稀有度']), limited=limited))

    up_char_file = Path(f'{DRAW_PATH}/draw_card_up/{game.split("_")[0]}_up_char.json')
    char_name_lst = [x.name for x in tmp_lst]
    if up_char_file.exists():
        data = json.load(open(up_char_file, 'r', encoding='utf8'))
        if len(game.split('_')) == 1:
            key = 'char'
        else:
            key = list(data.keys())[1]
        for x in data[key]['up_char']:
            for char in data[key]['up_char'][x]:
                if char not in char_name_lst:
                    if game.find('prts') != -1:
                        tmp_lst.append(Operator(name=char, star=int(x),
                                                recruit_only=False, event_only=False, limited=False))
                    else:
                        tmp_lst.append(Operator(name=char, star=int(x), limited=False))
    return tmp_lst