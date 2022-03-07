from bs4 import BeautifulSoup
from urllib.parse import unquote
import bs4
import re
from hoshino import aiorequests

headers = {'User-Agent': '"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"'}

async def get_cn_name():
    url = 'https://wiki.biligame.com/umamusume/支援卡图鉴'
    response = await aiorequests.get(url, timeout=7)
    resp_data = await response.text
    soup = BeautifulSoup(resp_data, 'lxml')
    _tbody = get_tbody(soup)
    trs = _tbody.find_all('tr')
    att_dict = {'头像': 0, '名称': 1}
    start_index = 2
    index = 2
    for th in trs[0].find_all('th')[start_index:]:
        text = th.text
        if text[-1] == '\n':
            text = text[:-1]
        att_dict[text] = index
        index += 1
    uma_dict = {}
    for tr in trs[1:]:
        member_dict = {}
        tds = tr.find_all('td')
        info_list = att_dict.keys()
        for key in info_list:
            attr = ''
            td = tds[att_dict[key]]
            last_tag = unquote(_find_last_tag(td, attr), 'utf-8')
            member_dict[key] = last_tag
            member_dict = intermediate_check(member_dict, key, td)
        # print(member_dict) # 这是全部的数据
        jp_name_tmp = re.search(r'\S+】(\S+)', member_dict['名称'])
        jp_name = jp_name_tmp.group(1)
        uma_dict[jp_name] = {}
        uma_dict[jp_name]['cn_name'] = member_dict['关联角色']
        try:
            uma_dict[jp_name]['grass'] = re.search(r'(\S)图标', member_dict['草地']).group(1)
            uma_dict[jp_name]['mud'] = re.search(r'(\S)图标', member_dict['泥地']).group(1)
            uma_dict[jp_name]['short'] = re.search(r'(\S)图标', member_dict['短距']).group(1)
            uma_dict[jp_name]['mile'] = re.search(r'(\S)图标', member_dict['英里']).group(1)
            uma_dict[jp_name]['middle'] = re.search(r'(\S)图标', member_dict['中距']).group(1)
            uma_dict[jp_name]['long'] = re.search(r'(\S)图标', member_dict['长距']).group(1)
            uma_dict[jp_name]['run_away'] = re.search(r'(\S)图标', member_dict['逃']).group(1)
            uma_dict[jp_name]['first'] = re.search(r'(\S)图标', member_dict['先行']).group(1)
            uma_dict[jp_name]['center'] = re.search(r'(\S)图标', member_dict['差行']).group(1)
            uma_dict[jp_name]['chase'] = re.search(r'(\S)图标', member_dict['追']).group(1)
        except:
            uma_dict[jp_name]['grass'] = ''
            uma_dict[jp_name]['mud'] = ''
            uma_dict[jp_name]['short'] = ''
            uma_dict[jp_name]['mile'] = ''
            uma_dict[jp_name]['middle'] = ''
            uma_dict[jp_name]['long'] = ''
            uma_dict[jp_name]['run_away'] = ''
            uma_dict[jp_name]['first'] = ''
            uma_dict[jp_name]['center'] = ''
            uma_dict[jp_name]['chase'] = ''
        # 什么？我绿帽难道不应该是马娘战神吗？
        if uma_dict[jp_name]['cn_name'] == '骏川缰绳':
            uma_dict[jp_name]['grass'] = 'S'
            uma_dict[jp_name]['mud'] = 'S'
            uma_dict[jp_name]['short'] = 'S'
            uma_dict[jp_name]['mile'] = 'S'
            uma_dict[jp_name]['middle'] = 'S'
            uma_dict[jp_name]['long'] = 'S'
            uma_dict[jp_name]['run_away'] = 'S'
            uma_dict[jp_name]['first'] = 'S'
            uma_dict[jp_name]['center'] = 'S'
            uma_dict[jp_name]['chase'] = 'S'
    return uma_dict

def get_tbody(soup: bs4.BeautifulSoup):
    max_count = 0
    _tbody = None
    for tbody in soup.find_all('tbody'):
        if len(tbody.find_all('tr')) > max_count:
            _tbody = tbody
            max_count = len(tbody.find_all('tr'))
    return _tbody

def _find_last_tag(element: bs4.element.Tag, attr: str) -> str:
    last_tag = []
    for des in element.descendants:
        last_tag.append(des)
    if len(last_tag) == 1 and last_tag[0] == '\n':
        last_tag = ''
    elif last_tag[-1] == '\n':
        last_tag = last_tag[-2]
    else:
        last_tag = last_tag[-1]
    if attr and str(last_tag):
        last_tag = last_tag[attr]
    elif str(last_tag).find('<img') != -1:
        if last_tag.get('srcset'):
            last_tag = str(last_tag.get('srcset')).strip().split(' ')[-2].strip()
        else:
            last_tag = last_tag['src']
    else:
        last_tag = str(last_tag)
    if str(last_tag) and str(last_tag)[-1] == '\n':
        last_tag = str(last_tag)[:-1]
    return last_tag

def intermediate_check(member_dict: dict, key: str, td: bs4.element.Tag):
    if key == '获取方式':
        obtain = []
        for x in str(td.text).replace('\n', '').strip().split('、'):
            if x:
                obtain.append(x)
        member_dict['获取方式'] = obtain
    return member_dict