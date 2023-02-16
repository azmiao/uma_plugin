from bs4 import BeautifulSoup
import os
import json
import re
from datetime import datetime
import shutil

from hoshino import aiorequests

url = 'https://wiki.biligame.com/umamusume/期间限定任务'
current_dir = os.path.join(os.path.dirname(__file__), f'tasks_config.json')

# 获取标题列表
async def get_title_list(soup):
    title_list = []
    rep_list = soup.find_all('span', {'class': 'panel-title pull-left'})
    for title in rep_list:
        title_list.append(title.text.replace('\u3000', ''))
    return title_list

# 获取最新的更新时间
async def get_update_time():
    update_url = 'https://wiki.biligame.com/umamusume/index.php?title=期间限定任务&action=history'
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
    # 获取任务名列表
    title_list = await get_title_list(soup)
    number = len(title_list)
    all_number = number
    f_data['number'] = all_number
    f_data['tasks'] = {}
    rep_list = soup.find_all('table', {'class': 'wikitable'})
    for res in rep_list:
        # 删除影响查找的多余标签，以便后续操作
        no_need_list = res.find_all('table') + res.find_all('center')
        for tag in no_need_list:
            tag.decompose()
        f_data['tasks'][str(number)] = {}
        f_data['tasks'][str(number)]['title'] = title_list[all_number - number]
        f_data['tasks'][str(number)]['task_list'] = {}
        rep_tr = res.find_all('tr')
        # m是每个限时任务内的小任务编号
        m = 0
        for each_tr in rep_tr:
            # 寻找无属性的tr
            if each_tr.find('th'):
                continue
            m += 1
            each_tr_list = []
            for each_td in each_tr.find_all('td'):
                each_td = each_td.text.replace('\n', '')
                each_tr_list.append(each_td)
            if len(each_tr_list) == 4:
                each_tr_dict = {
                    '任务名': each_tr_list[0],
                    '达成条件': each_tr_list[1],
                    '推荐赛马娘': each_tr_list[2],
                    '奖励': each_tr_list[3]
                }
            else:
                each_tr_dict = {
                    '任务名': each_tr_list[0],
                    '达成条件': each_tr_list[1],
                    '比赛时间': each_tr_list[2],
                    '比赛环境': each_tr_list[3],
                    '推荐赛马娘': each_tr_list[4],
                    '奖励': each_tr_list[5]
                }
            f_data['tasks'][str(number)]['task_list'][str(m)] = each_tr_dict
        number -= 1
        # 都做完了再写入
        if number <= 0:
            with open(current_dir, 'w', encoding='UTF-8') as f:
                json.dump(f_data, f, indent=4, ensure_ascii=False)
            break

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
    path = os.path.join(root_path, 'uma_tasks/')
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)