import httpx
import datetime
import json
import os
import re
from bs4 import BeautifulSoup

from hoshino import R
from .util import server_list, init_data, get_differ, get_correspond

gacha_path = os.path.join(R.img('umamusume').path, 'uma_gacha')

# 其他服的卡池
async def add_other_server(server, start_time, end_time, now, pool_data, uma_title, uma_title_img, uma_up, chart_title, chart_title_img, chart_up):
    differ = await get_differ(server, 'jp')
    # 卡池时间
    start_time_ot = start_time + datetime.timedelta(days=differ + 1)
    start_time_ot_show = datetime.datetime.strftime(start_time_ot, '%Y/%m/%d %H:%M')
    end_time_ot = end_time + datetime.timedelta(days=differ + 1)
    end_time_ot_show = datetime.datetime.strftime(end_time_ot, '%Y/%m/%d %H:%M')
    pool_time_ot = f'{start_time_ot_show}~{end_time_ot_show}'
    # 卡池ID
    pool_id_ot = str(start_time_ot).replace('-', '')[:8]
    # 数据
    if now >= start_time_ot:
        pool_data[server][pool_id_ot] = {
            'pool_time': pool_time_ot,
            'start_time': start_time_ot_show,
            'end_time': end_time_ot_show,
            'uma_title': uma_title,
            'uma_title_img': uma_title_img,
            'uma_up': uma_up,
            'chart_title': chart_title,
            'chart_title_img': chart_title_img,
            'chart_up': chart_up
        }
    return pool_data

# 特殊UP调整
async def UP_modify(pool_data):
    for server in server_list:
        for pool_id in list(pool_data[server].keys()):
            cal_pool_id = await get_correspond(server, 'jp', pool_id)
            if cal_pool_id == '20220224':
                pool_data[server][pool_id]['uma_up']['3'] = ['北部玄驹']
                pool_data[server][pool_id]['uma_up']['2'] = ['待兼诗歌剧']
                pool_data[server][pool_id]['chart_up']['R'] = ['【トレセン学園】メジロブライト']
            if cal_pool_id == '20220729':
                pool_data[server][pool_id]['chart_up']['R'] = ['【トレセン学園】ツルマルツヨシ']
            if cal_pool_id == '20220111':
                pool_data[server][pool_id]['chart_up']['SR'] = ['【これがウチらのいか焼きや！】タマモクロス']
                pool_data[server][pool_id]['chart_up']['SSR'] = ['【ブスッといっとく？】安心沢刺々美']
    return pool_data

# 特殊R卡调整，一般是由于活动SSR卡导致的
async def sp_modify(uma_name_list):
    # 一般只需要在这里加上缺少的即可
    uma_name_list.append('【トレセン学園】テイエムオペラオー')
    uma_name_list.append('【トレセン学園】メジロマックイーン')
    # 下面比较特殊，一般不需要动
    if '【トレセン学園】安心沢刺々美' in uma_name_list:
        uma_name_list.remove('【トレセン学園】安心沢刺々美')
        uma_name_list.append('【笹針師】安心沢刺々美')
    if '【トレセン学園】玉座に集いし者たち' in uma_name_list:
        uma_name_list.remove('【トレセン学園】玉座に集いし者たち')
    if '【トレセン学園】ライトハロー' in uma_name_list:
        uma_name_list.remove('【トレセン学園】ライトハロー')
        uma_name_list.append('【イベントプロデューサー】ライトハロー')
    # 去重
    uma_name_list = list(set(uma_name_list))
    return uma_name_list

# 获取其他马娘/支援卡数据
async def get_other_uma(pool_data, server):
    if not pool_data[server]:
        return pool_data
    for gacha_type in ['uma', 'chart']:
        id_list = list(pool_data[server].keys())
        id_list.reverse()
        pool_data[server][id_list[0]][f'other_{gacha_type}'] = init_data[f'other_{gacha_type}']
        for i in range(1, len(id_list)):
            last_pool = pool_data[server][id_list[i-1]][f'other_{gacha_type}']
            new_pool_data = {}
            for rank in list(last_pool.keys()):
                new_pool_data[rank] = last_pool[rank] + pool_data[server][id_list[i-1]][f'{gacha_type}_up'][rank]
            pool_data[server][id_list[i]][f'other_{gacha_type}'] = new_pool_data
            if re.search('全体', pool_data[server][id_list[i]][f'{gacha_type}_title']):
                high_rank = list(last_pool.keys())[0]
                pool_data[server][id_list[i]][f'{gacha_type}_up'][high_rank] = last_pool[high_rank]
                pool_data[server][id_list[i]][f'other_{gacha_type}'][high_rank] = []
    pool_data = await get_R(pool_data, server)
    return pool_data

# 支援卡增加R卡数据
async def get_R(pool_data, server):
    for pool_id in list(pool_data[server].keys()):
        uma_name_list = []
        for rank in list(pool_data[server][pool_id]['chart_up'].keys()):
            chart_uma = ['【トレセン学園】' + x.split('】', 1)[1] for x in pool_data[server][pool_id]['chart_up'][rank]]
            uma_name_list += chart_uma
        for rank in list(pool_data[server][pool_id]['other_chart'].keys()):
            chart_uma = ['【トレセン学園】' + x.split('】', 1)[1] for x in pool_data[server][pool_id]['other_chart'][rank]]
            uma_name_list += chart_uma
        # 特殊情况
        uma_name_list = await sp_modify(uma_name_list)
        pool_data[server][pool_id]['other_chart']['R'] = uma_name_list
    return pool_data

# 增加初始卡池
async def add_init_pool(pool_data):
    for server in server_list:
        pool_data[server]['000000'] = {
            'pool_time': '',
            'start_time': '',
            'end_time': '',
            'uma_title': '开服初始马娘池',
            'uma_title_img': '',
            'uma_up': {'3':[], '2':[], '1': []},
            'chart_title': '开服初始支援卡池',
            'chart_title_img': '',
            'chart_up': {'SSR':[], 'SR':[], 'R': []},
            'other_uma': init_data['other_uma'],
            'other_chart': init_data['other_chart'],
        }
    return pool_data

# 获取卡池数据
async def get_pool_data():
    pool_url = 'https://wiki.biligame.com/umamusume/卡池'
    res = httpx.get(pool_url, timeout=15)
    soup = BeautifulSoup(res.text, 'lxml')
    soup = soup.find('table', {"style": "width:100%;text-align:center"})
    tr_all = [tr for tr in soup.find_all('tr') if tr.find('div', {"class": "floatnone"})]
    pool_list = [(tr_all[i], tr_all[i+1]) for i in range(0, len(tr_all), 2)]
    pool_data, now = {}, datetime.datetime.now()
    for server in server_list:
        pool_data[server] = {}
    for pool in pool_list:
        # 日服卡池时间
        pool_time_edge = pool[0].find('td', {"rowspan": "2"}).text.strip().split('~', 1)
        start_time = datetime.datetime.strptime(pool_time_edge[1], '%Y/%m/%d %H:%M') - datetime.timedelta(hours=1)
        start_time_show = datetime.datetime.strftime(start_time, '%Y/%m/%d %H:%M')
        end_time = datetime.datetime.strptime(pool_time_edge[0], '%Y/%m/%d %H:%M') - datetime.timedelta(hours=1)
        end_time_show = datetime.datetime.strftime(end_time, '%Y/%m/%d %H:%M')
        pool_time = f'{start_time_show}~{end_time_show}'
        # 日服卡池ID
        pool_id = str(start_time).replace('-', '')[:8]
        # 马娘
        uma_title = pool[0].find('div', {"class": "floatnone"}).find('a').get('title')
        uma_title_id = pool[0].find('div', {"class": "floatnone"}).find('img').get('alt').replace(' ', '_')
        uma_title_img = pool[0].find('div', {"class": "floatnone"}).find('img').get('src').replace('thumb/', '')\
            .replace('/400px-'+ uma_title_id, '')
        uma_up_list = [span.find('a').get('title') for span in pool[0].find_all('span', {"style": "display: table-cell;"})]
        uma_up = {'3': uma_up_list, '2': [], '1': []}
        # 支援卡
        chart_title = pool[1].find('div', {"class": "floatnone"}).find('a').get('title')
        chart_title_id = pool[1].find('div', {"class": "floatnone"}).find('img').get('alt').replace(' ', '_')
        chart_title_img = pool[1].find('div', {"class": "floatnone"}).find('img').get('src').replace('thumb/', '')\
            .replace('/400px-'+ chart_title_id, '')
        chart_up_list = [span.find('a').get('title') for span in pool[1].find_all('span', {"style": "display:inline-block;"})]
        if re.search('、SR', chart_title):
            chart_SR_up_list = [x for x in chart_up_list if x != chart_up_list[0]]
            chart_up = {'SSR': [chart_up_list[0]], 'SR': chart_SR_up_list, 'R': []}
        else:
            chart_up = {'SSR': chart_up_list, 'SR': [], 'R': []}
        # 日服数据
        pool_data['jp'][pool_id] = {
            'pool_time': pool_time,
            'start_time': start_time_show,
            'end_time': end_time_show,
            'uma_title': uma_title,
            'uma_title_img': uma_title_img,
            'uma_up': uma_up,
            'chart_title': chart_title,
            'chart_title_img': chart_title_img,
            'chart_up': chart_up
        }
        # 其他服
        for server in server_list:
            if server == 'jp':
                continue
            pool_data = await add_other_server(server, start_time, end_time, now, pool_data, uma_title, uma_title_img, uma_up, chart_title, chart_title_img, chart_up)
    pool_data = await UP_modify(pool_data)
    pool_data = await add_init_pool(pool_data)
    for server in server_list:
        pool_data = await get_other_uma(pool_data, server)
    with open(os.path.join(gacha_path, 'uma_pool.json'), 'w', encoding='utf-8') as f:
        json.dump(pool_data, f, ensure_ascii=False, indent=4)