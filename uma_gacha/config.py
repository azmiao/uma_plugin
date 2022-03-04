import os
import hoshino
from pathlib import Path
from hoshino import R, log
try:
    import ujson as json
except ModuleNotFoundError:
    import json

logger = log.new_logger('config', hoshino.config.DEBUG)
DRAW_PATH = R.img('uma_gacha').path

if not os.path.exists(DRAW_PATH):
    os.mkdir(f'{DRAW_PATH}')
    os.mkdir(f'{DRAW_PATH}/draw_card')
    os.mkdir(f'{DRAW_PATH}/draw_card/pretty')
    os.mkdir(f'{DRAW_PATH}/draw_card_up')

_draw_config = Path(rf"{DRAW_PATH}/draw_card_config/draw_card_config.json")

# 赛马娘概率
PRETTY_THREE_P = 0.03
PRETTY_TWO_P = 0.18
PRETTY_ONE_P = 0.79

path_dict = {
    'pretty': '赛马娘'
}

config_default_data = {

    'path_dict': {
        'pretty': '赛马娘',
    },

    'pretty': {
        'PRETTY_THREE_P': 0.03,
        'PRETTY_TWO_P': 0.18,
        'PRETTY_ONE_P': 0.79,
    }
}

def check_config():
    global config_default_data, path_dict, PRETTY_THREE_P, PRETTY_ONE_P, PRETTY_TWO_P
    _draw_config.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = json.load(open(_draw_config, 'r', encoding='utf8'))
    except (FileNotFoundError, ValueError):
        _draw_config.parent.mkdir(parents=True, exist_ok=True)
        json.dump(config_default_data, open(_draw_config, 'w', encoding='utf8'), indent=4, ensure_ascii=False)
        logger.info('配置文件不存在或格式错误，已重新生成配置文件.....')
    else:
        try:
            PRETTY_THREE_P = float(data['pretty']['PRETTY_THREE_P'])
            PRETTY_TWO_P = float(data['pretty']['PRETTY_TWO_P'])
            PRETTY_ONE_P = float(data['pretty']['PRETTY_ONE_P'])
        except KeyError:
            data['pretty'] = {}
            data['pretty']['PRETTY_THREE_P'] = config_default_data['pretty']['PRETTY_THREE_P']
            data['pretty']['PRETTY_TWO_P'] = config_default_data['pretty']['PRETTY_TWO_P']
            data['pretty']['PRETTY_ONE_P'] = config_default_data['pretty']['PRETTY_ONE_P']
        json.dump(data, open(_draw_config, 'w', encoding='utf8'), indent=4, ensure_ascii=False)





