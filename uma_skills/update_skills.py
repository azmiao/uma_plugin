from bs4 import BeautifulSoup
import os
import json
import re
from datetime import datetime
import shutil

from hoshino import aiorequests

url = 'https://wiki.biligame.com/umamusume/技能速查表'
current_dir = os.path.join(os.path.dirname(__file__), f'skills_config.json')

# 获取最新的更新时间
async def get_update_time():
    update_url = 'https://wiki.biligame.com/umamusume/index.php?title=技能速查表&action=history'
    rep = await aiorequests.get(update_url, timeout=10)
    soup = BeautifulSoup(await rep.text, 'lxml')
    last_time_tmp = soup.find('a', {'class': 'mw-changeslist-date'}).text.replace(' ', '')
    group = re.search(r'^([0-9]{4})年([0-9]{1,2})月([0-9]{1,2})日\S*([0-9]{2}):([0-9]{2})$', last_time_tmp)
    last_time = datetime(int(group.group(1)), int(group.group(2)), int(group.group(3)), int(group.group(4)), int(group.group(5)))
    return last_time

# 更新数据
async def update_info():
    rep = await aiorequests.get(url, timeout=10)
    soup = BeautifulSoup(await rep.text, 'lxml')
    with open(current_dir, 'r', encoding='UTF-8') as f:
        f_data = json.load(f)
    # 获取最新版的更新时间
    last_time = await get_update_time()
    f_data['last_time'] = str(last_time)
    f_data['cn_name_dict'] = {}
    # 获取所有技能
    f_data['skills'] = {}
    res_tag = soup.find('table', {'class': 'CardSelect wikitable sortable'})
    # 删除影响查找的多余标签
    res_tag.find('tr', {'id': 'CardSelectTabHeader'}).decompose()
    # 这样就全部都市谷有咲的标签
    tr_list = res_tag.find_all('tr', {'class': 'divsort'})
    for each_tr in tr_list:
        rarity = each_tr.get('data-param1')
        color = each_tr.get('data-param3')
        each_tr_list = []
        for each_td in each_tr.find_all('td'):
            each_td = each_td.text.replace('\n', '')
            each_tr_list.append(each_td)
        skill_name_jp = each_tr_list[1].replace(' ', '_')
        skill_name_cn = each_tr_list[2].replace(' ', '_')
        # 额外处理一下继承技能
        if rarity == '普通·继承':
            skill_name_jp = '继承技/' + skill_name_jp
            skill_name_cn = '继承技/' + skill_name_cn
        # 对异常的结果修改
        skill_type = '条件1: 速度条件2: 速度、加速度' if each_tr_list[11] == '加速度条件2: 速度、条件1: 速度' else each_tr_list[11]
        # 注：嘉年华活动技能就不做额外处理了，仅保留最新的
        each_tr_dict = {
            '中文名': skill_name_cn,
            '稀有度': rarity,
            '颜色': color,
            '条件限制': each_tr_list[3],
            '技能描述': each_tr_list[4],
            '技能数值': each_tr_list[5],
            '持续时间': each_tr_list[6],
            '评价分': each_tr_list[7],
            '需要PT': each_tr_list[8],
            'PT评价比': each_tr_list[9],
            '触发条件': each_tr_list[10],
            '技能类型': skill_type
        }
        f_data['cn_name_dict'][skill_name_cn] = skill_name_jp
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