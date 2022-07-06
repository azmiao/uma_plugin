import os
import json
import random
import datetime
from .update_data import write_info

# 获取当前时间
async def get_time():
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    return now_time

# 获取消息
async def get_msg(group_id, user_id):
    # 获取可选文件
    current_dir = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(current_dir, 'r', encoding = 'utf-8') as f:
        config = json.load(f)
    # 生成消息
    fortune = random.choice(config['fortune'])
    now_time = str(await get_time())
    characters = await get_chara()
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
    # 写入信息到文件
    await write_info(
        group_id, user_id, actions, characters, fortune, position, prefertime,
        suitable_key, suitable_value, unsuitable_key, unsuitable_value
    )
    # 结果消息
    msg = f'''
[CQ:at,qq={user_id}]签到成功
今日运势：{fortune}
当前时间：{now_time}
今日幸运角色：{characters}
宜：{suitable}
忌：{unsuitable}
抽卡加成时间：{prefertime}
抽卡加成方向：{position}
抽卡加成动作：{actions}
    '''.strip()
    return msg

# 获取角色
async def get_chara():
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info/config.json'), 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    chara_list = []
    for uma_name in name_list:
        if f_data[uma_name]['cn_name']:
            chara_list.append(f_data[uma_name]['cn_name'])
    return random.choice(chara_list)

# 判断是否已经签到过
async def judge(group_id, user_id):
    current_dir = os.path.join(os.path.dirname(__file__), f'data/{group_id}.json')
    if not os.path.exists(os.path.join(os.path.dirname(__file__), f'data/')):
        os.mkdir(os.path.join(os.path.dirname(__file__), f'data/'))
    if os.path.exists(current_dir):
        file = open(current_dir, 'r', encoding = 'UTF-8')
        config = json.load(file)
        if str(user_id) in list(config.keys()):
            return True
    return False

# 若签到过就获取已经签到过的信息
async def get_almanac_info(group_id, user_id):
    current_dir = os.path.join(os.path.dirname(__file__), f'data/{group_id}.json')
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        config = json.load(f)
    user_id = str(user_id)
    msg = f'''
[CQ:at,qq={user_id}]您今天已经签到过了哟，之前的签到结果如下
今日运势：{config[user_id]['fortune']}
今日幸运角色：{config[user_id]['characters']}
宜：{config[user_id]['suitable'][0]}：{config[user_id]['suitable'][1]}
忌：{config[user_id]['unsuitable'][0]}：{config[user_id]['unsuitable'][1]}
抽卡加成时间：{config[user_id]['prefertime']}
抽卡加成方向：{config[user_id]['position']}
抽卡加成动作：{config[user_id]['actions']}
    '''.strip()
    return msg