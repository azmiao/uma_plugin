import json
import os
import re
import shutil
from datetime import datetime

from bs4 import BeautifulSoup
from hoshino import aiorequests

url = 'https://wiki.biligame.com/umamusume/技能速查表'
current_dir = os.path.join(os.path.dirname(__file__), f'skills_config.json')


# 获取最新的更新时间
async def get_update_time():
    headers = {
        'Host': 'wiki.biligame.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image'
                  '/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd'
    }
    update_url = 'https://wiki.biligame.com/umamusume/index.php?title=技能速查表&action=history'
    rep = await aiorequests.get(update_url, timeout=10, headers=headers)
    soup = BeautifulSoup(await rep.text, 'lxml')
    last_time_tmp = soup.find('a', {'class': 'mw-changeslist-date'}).text.replace(' ', '')
    group = re.search(r'^([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日\S*([0-9]{2}):([0-9]{2})$', last_time_tmp)
    last_time = datetime(int(group.group(1)), int(group.group(2)), int(group.group(3)), int(group.group(4)),
                         int(group.group(5)))
    return last_time


# 23-04-03新版更新数据
async def update_info():
    rep = await aiorequests.get(url, timeout=10)
    soup = BeautifulSoup(await rep.text, 'lxml')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        f_data = json.load(f)
    # 获取最新版的更新时间
    last_time = await get_update_time()
    f_data['last_time'] = str(last_time)
    f_data['cn_name_dict'] = {}
    f_data['tw_name_dict'] = {}
    # 获取所有技能
    f_data['skills'] = {}
    res_tag = soup.find('div', {'id': 'jn-json'})
    data_list_str = res_tag.text.replace(' ', '').replace('<br/>', '').replace('&#160;', '_').replace(',]', ']')
    # print(data_list_str)
    data_list = json.loads(data_list_str)
    for data in data_list:
        rarity = data['5']
        skill_name_jp = data['1']
        skill_name_cn = data['4']
        skill_name_tw = data['21']
        # 额外处理一下继承技能
        if rarity == '普通·继承':
            skill_name_jp = '继承技/' + skill_name_jp
            skill_name_cn = '继承技/' + skill_name_cn
            skill_name_tw = '继承技/' + skill_name_tw
        # 注：嘉年华活动技能就不做额外处理了，仅保留最新的
        each_tr_dict = {
            '中文名': skill_name_cn,
            '稀有度': rarity,
            '颜色': data['7'],
            '繁中译名': skill_name_tw,
            '条件限制': data['6'],
            '技能数值': data['12'],
            '持续时间': data['13'],
            '评价分': data['18'],
            '需要PT': data['19'],
            'PT评价比': data['20'],
            '触发条件': data['10'],
            '技能类型': data['11']
        }
        f_data['cn_name_dict'][skill_name_cn] = skill_name_jp
        f_data['tw_name_dict'][skill_name_tw] = skill_name_jp
        f_data['skills'][skill_name_jp] = each_tr_dict
    # 都做完了再写入
    with open(current_dir, 'w', encoding='UTF-8') as f:
        json.dump(f_data, f, indent=4, ensure_ascii=False)


# 判断是否有更新
async def judge_update():
    last_time = await get_update_time()
    with open(current_dir, 'r', encoding='UTF-8') as f:
        f_data = json.load(f)
    set_time = datetime.strptime(f_data['last_time'], "%Y-%m-%d %H:%M:%S")
    if last_time > set_time:
        return True
    else:
        return False


# 若有更新就删除已经生成过的所有图片
async def del_img(root_path):
    path = os.path.join(root_path, 'uma_skills/')
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)
