#coding:utf-8
import aiohttp
import requests
from .config import DRAW_PATH
from asyncio.exceptions import TimeoutError
from bs4 import BeautifulSoup
from .util import download_img, remove_prohibited_str
from urllib.parse import unquote
import hoshino
from hoshino import log
import bs4
import re
try:
    import ujson as json
except ModuleNotFoundError:
    import json

logger = log.new_logger('update_game_info', hoshino.config.DEBUG)
headers = {'User-Agent': '"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"'}


async def update_info(url: str, game_name: str, info_list: list = None):
    try:
        with open(f'{DRAW_PATH}/{game_name}.json', 'r', encoding='utf8') as f:
            data = json.load(f)
    except (ValueError, FileNotFoundError):
        data = {}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            response = requests.get(url, timeout=7)
            soup = BeautifulSoup(response.text, 'lxml')
            _tbody = get_tbody(soup, game_name, url)
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
            for tr in trs[1:]:
                member_dict = {}
                tds = tr.find_all('td')
                if not info_list:
                    info_list = att_dict.keys()
                for key in info_list:
                    if key == '名称' and game_name == 'pretty':
                        last_tag = get_name(td, attr)
                    else:
                        attr = ''
                        td = tds[att_dict[key]]
                        last_tag = unquote(_find_last_tag(td, attr, game_name), 'utf-8')
                    member_dict[key] = last_tag
                    member_dict = intermediate_check(member_dict, key, game_name, td)
                avatar_img = await _modify_avatar_url(session, game_name, member_dict["名称"])
                member_dict['头像'] = avatar_img if avatar_img else member_dict['头像']
                if game_name == 'pretty_card':
                    member_dict, name = replace_update_name(member_dict, game_name)
                elif game_name == 'pretty':
                    name = member_dict['名称']
                    name = remove_prohibited_str(name)
                await download_img(member_dict['头像'], game_name, name)
                data[name] = member_dict
                logger.info(f'{name} is update...')
            data = await _last_check(data, game_name, session)
    except TimeoutError:
        logger.info(f'更新 {game_name} 超时...')
        return {}, 999
    with open(f'{DRAW_PATH}/{game_name}.json', 'w', encoding='utf8') as wf:
        wf.write(json.dumps(data, ensure_ascii=False, indent=4))
    return data, 200


def _find_last_tag(element: bs4.element.Tag, attr: str, game_name: str) -> str:
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

    if game_name not in ['pretty', 'pretty_card'] and last_tag.find('http') == -1:
        last_tag = last_tag.split('.')[0]

    return last_tag

# 拿到名称
def get_name(element: bs4.element.Tag, attr: str):
    last_tag = []
    for des in element.descendants:
        last_tag.append(des)
    return last_tag[0]['title']

# 育成卡换中文
def replace_update_name(member_dict: dict, game_name: str):
    name = member_dict['名称']
    if game_name == 'pretty_card':
        name = member_dict['中文名']
        name = remove_prohibited_str(name)
        member_dict['中文名'] = name
    else:
        name = remove_prohibited_str(name)
        member_dict['名称'] = name
    return member_dict, name

# 获取大图（小图快爬）
async def _modify_avatar_url(session: aiohttp.ClientSession, game_name: str, char_name: str):
    if game_name == 'pretty_card':
        char_name = char_name.replace('?', '%3F')
        async with session.get(f'https://wiki.biligame.com/umamusume/{char_name}', timeout=7) as res:
            soup = BeautifulSoup(await res.text(), 'lxml')
            img_url = soup.find('div', {'class': 'support_card-left'}).find('div').find('img').get('src')
            return img_url


# 数据最后处理（是否需要额外数据或处理数据）
async def _last_check(data: dict, game_name: str, session: aiohttp.ClientSession):
    if game_name == 'pretty':
        for keys in data.keys():
            for key in data[keys].keys():
                r = re.search(r'.*?40px-(.*)图标.png', str(data[keys][key]))
                if r:
                    data[keys][key] = r.group(1)
                    # logger.info(f'赛马娘额外修改数据...{keys}[{key}]=> {r.group(1)}')
    return data


# 对抓取每行数据是否需要额外处理？
def intermediate_check(member_dict: dict, key: str, game_name: str, td: bs4.element.Tag):
    if game_name == 'pretty':
        if key == '初始星级':
            member_dict['初始星级'] = len(td.find_all('img'))
    if game_name == 'pretty_card':
        if key == '获取方式':
            obtain = []
            for x in str(td.text).replace('\n', '').strip().split('、'):
                if x:
                    obtain.append(x)
            member_dict['获取方式'] = obtain
    return member_dict


# 拿到tbody，不同游戏tbody可能不同
def get_tbody(soup: bs4.BeautifulSoup, game_name: str, url: str):
    max_count = 0
    _tbody = None
    if game_name == 'guardian_arms':
        if url[-2:] == '盾牌':
            div = soup.find('div', {'class': 'resp-tabs-container'}).find_all('div', {'class': 'resp-tab-content'})[1]
            _tbody = div.find('tbody')
        else:
            div = soup.find('div', {'class': 'resp-tabs-container'}).find_all('div', {'class': 'resp-tab-content'})[0]
            _tbody = div.find('table', {'id': 'CardSelectTr'}).find('tbody')
    else:
        for tbody in soup.find_all('tbody'):
            if len(tbody.find_all('tr')) > max_count:
                _tbody = tbody
                max_count = len(tbody.find_all('tr'))
    return _tbody
