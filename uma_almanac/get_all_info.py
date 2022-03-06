import os
import json
import random
import datetime
from .update_data import *

def get_json():
    current_dir = os.path.join(os.path.dirname(__file__), 'data.json')
    file = open(current_dir, 'r', encoding = 'utf-8')
    config = json.load(file)
    return config

def get_time():
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    return now_time

def get_msg(group_id, user_id):
    config = get_json()
    msg = f'[CQ:at,qq={user_id}]签到成功'
    fortune = random.choice(config['fortune'])
    now_time = str(get_time())
    characters = get_chara()
    suitable_key = random.choice(list(config['suitable'].keys()))
    suitable_value = config['suitable'][suitable_key]
    suitable = suitable_key + '：' + suitable_value
    unsuit_list = list(config['unsuitable'].keys())
    unsuit_list.remove(suitable_key)
    unsuitable_key = random.choice(unsuit_list)
    unsuitable_value = config['unsuitable'][unsuitable_key]
    unsuitable = unsuitable_key + '：' + unsuitable_value
    prefertime = f'{int(random.random() * 24)}时' + f'{int(random.random() * 60)}分' + f'{int(random.random() * 60)}秒'
    position = random.choice(config['position'])
    actions = random.choice(config['actions'])
    write_info(group_id, user_id, actions, characters, fortune, position, prefertime, suitable_key, suitable_value, unsuitable_key, unsuitable_value)
    msg = '{}\n今日运势：{}\n当前时间：{}\n今日幸运角色：{}\n宜：{}\n忌：{}\n抽卡加成时间：{}\n抽卡加成方向：{}\n抽卡加成动作：{}'.format(msg, fortune, now_time, characters, suitable, unsuitable, prefertime, position, actions)
    return msg

def get_chara():
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info/config.json'), 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
        f.close()
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    chara_list = []
    for uma_name in name_list:
        if f_data[uma_name]['cn_name']:
            chara_list.append(f_data[uma_name]['cn_name'])
    return random.choice(chara_list)

def judge(group_id, user_id):
    current_dir = os.path.join(os.path.dirname(__file__), f'data\{group_id}.json')
    if not os.path.exists(os.path.join(os.path.dirname(__file__), f'data/')):
        os.mkdir(os.path.join(os.path.dirname(__file__), f'data/'))
    if os.path.exists(current_dir):
        file = open(current_dir, 'r', encoding = 'UTF-8')
        config = json.load(file)
        if str(user_id) in list(config.keys()):
            return True
    return False