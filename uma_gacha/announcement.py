import aiohttp
import os
import pickle
from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime
from .config import DRAW_PATH
from pathlib import Path
from asyncio.exceptions import TimeoutError
import hoshino
from hoshino import log

logger = log.new_logger('announcement', hoshino.config.DEBUG)

try:
    import ujson as json
except ModuleNotFoundError:
    import json

headers = {'User-Agent': '"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"'}
pretty_up_char = Path(DRAW_PATH + "/draw_card_up/pretty_up_char.json")
pretty_url = "https://wiki.biligame.com/umamusume/%E5%85%AC%E5%91%8A"

# 是否过时
def is_expired(data: dict):
    times = data['time'].split('-')
    for i in range(len(times)):
        times[i] = str(datetime.now().year) + '-' + times[i].split('日')[0].strip().replace('月', '-')
    start_date = datetime.strptime(times[0], '%Y-%m-%d').date()
    end_date = datetime.strptime(times[1], '%Y-%m-%d').date()
    now = datetime.now().date()
    return start_date <= now <= end_date


# 检查写入
def check_write(data: dict, up_char_file):
    try:
        if not is_expired(data['char']):
            for x in list(data.keys()):
                data[x]['title'] = ''
        else:
            with open(up_char_file, 'w', encoding='utf8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        if not up_char_file.exists():
            with open(up_char_file, 'w', encoding='utf8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            with open(up_char_file, 'r', encoding='utf8') as f:
                old_data = json.load(f)
            if is_expired(old_data['char']):
                return old_data
            else:
                with open(up_char_file, 'w', encoding='utf8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
    except ValueError:
        pass
    return data

class PrettyAnnouncement:

    def __init__(self):
        self.game_name = '赛马娘'

    async def _get_announcement_text(self):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(pretty_url, timeout=7) as res:
                soup = BeautifulSoup(await res.text(), 'lxml')
                divs = soup.find('div', {'id': 'mw-content-text'}).find('div').find_all('div')
                for div in divs:
                    a = div.find('a')
                    try:
                        title = a['title']
                    except (KeyError, TypeError):
                        continue
                    if title.find('支援卡卡池') != -1:
                        url = a['href']
                        break
                    elif title.find('支援卡登场') != -1:
                        url = a['href']
                        break
            # async with session.get(f'https://wiki.biligame.com/{url}', timeout=7) as res:
            #     return await res.text()
            text = requests.get(f'https://wiki.biligame.com/{url}', timeout=7)
            return text.text

    async def update_up_char(self):
        data = {
            'char': {'up_char': {'3': {}, '2': {}, '1': {}}, 'title': '', 'time': '', 'pool_img': ''},
            'card': {'up_char': {'3': {}, '2': {}, '1': {}}, 'title': '', 'time': '', 'pool_img': ''}
        }
        try:
            text= await self._get_announcement_text()
            soup = BeautifulSoup(text, 'lxml')
            context = soup.find('div', {'class': 'toc-sticky'})
            if not context:
                context = soup.find('div', {'class': 'mw-parser-output'})
            if context('big'):
                for big in context.find_all('big'):
                    r = re.search(r'\d{1,2}/\d{1,2} \d{1,2}:\d{1,2} ～', str(big.text))
                    if r:
                        time = str(big.text)
                        break
            else:
                for p in context.find_all('p'):
                    r = re.search(r'\d{1,2}/\d{1,2} \d{1,2}:\d{1,2} ～', str(p.text))
                    if r:
                        time = str(p.text)
                        break
                else:
                    logger.info('赛马娘UP无法找到活动日期....取消更新UP池子...')
                    return
            if '北京时间' in time:
                time = re.match(r'([\s\S]*)（', time).group().replace('（', '')
            time = time.replace('\n', '').replace('～', '-').replace('/', '月').split(' ')
            time = time[0] + '日 ' + time[1] + ' - ' + time[3] + '日 ' + time[4]
            data['char']['time'] = time
            data['card']['time'] = time
            flag = 0
            for p in context.find_all('p'):
                if str(p).find('当期UP赛马娘') != -1 and str(p).find('■') != -1:
                    r = re.findall(r'.*?当期UP赛马娘([\s\S]*)＜奖励内容＞.*?', str(p))
                    if r:
                        for x in r:
                            x = str(x).split('\n')
                            for msg in x:
                                if msg.find('★') != -1:
                                    msg = msg.replace('<br />', '')
                                    char_name = msg[msg.find('['):].strip()
                                    char_name = char_name.replace('<br/>', '').replace(']', '】').replace('[', '【')
                                    if (star := len(msg[:msg.find('[')].strip())) == 3:
                                        data['char']['up_char']['3'][char_name] = '70'
                                    elif star == 2:
                                        data['char']['up_char']['2'][char_name] = '70'
                                    elif star == 1:
                                        data['char']['up_char']['1'][char_name] = '70'
                elif str(p).find('新登场的育成赛马娘') != -1 and str(p).find('■') != -1:
                    r = re.findall(r'.*?（概率提升对象）([\s\S]*)■.*?', str(p))
                    if r:
                        for x in r:
                            x = str(x).split('\n')
                            for msg in x:
                                if msg.find('★') != -1:
                                    msg = msg.replace('<br />', '')
                                    char_name = msg[msg.find('['):].strip()
                                    char_name = char_name.replace('<br/>', '')
                                    if '（' in char_name and '）' in char_name:
                                        char_name = re.search(r'】([\s\S]*)', char_name).group().replace('）', '').replace('】', '')
                                    if (star := len(msg[:msg.find('[')].strip())) == 3:
                                        data['char']['up_char']['3'][char_name] = '70'
                                    elif star == 2:
                                        data['char']['up_char']['2'][char_name] = '70'
                                    elif star == 1:
                                        data['char']['up_char']['1'][char_name] = '70'
                elif str(p).find('全部赛马娘') != -1:
                    flag = 1
                    current_dir = os.path.join(os.path.dirname(__file__), 'char_atlas.txt')
                    with open(current_dir, 'rb') as f:
                        char_list = pickle.load(f)
                    for char in char_list:
                        if int(char.star) == 3:
                            data['char']['up_char']['3'][str(char.name)] = '70'
                if (str(p).find('（当期UP对象）') != -1 or str(p).find('（概率UP对象）') == -1 or str(p).find('（概率提升对象）') == -1) and str(p).find('■') != -1:
                    r = re.search(r'■ ?全?新?(登场的)?支援卡（(当期|概率)(UP|up|提升)对象）([\s\S]*)</p>', str(p))
                    if r:
                        rmsg = r.group(4).strip()
                        rmsg = rmsg.replace('<br />', '<br/>')
                        rmsg = rmsg.split('<br/>')
                        rmsg = [x for x in rmsg if x]
                        for x in rmsg:
                            x = x.replace('\n', '').replace('・', '').replace('·', '').replace('[', '【').replace(']', '】')
                            star = x[:x.find('【')].strip()
                            card_name = x[x.find('【'):].strip()
                            if '（' in card_name and '）' in card_name:
                                card_name = re.search(r'（([\s\S]*)）', card_name).group().replace('（', '').replace('）', '')
                            if star == 'SSR':
                                data['card']['up_char']['3'][card_name] = '70'
                            if star == 'SR':
                                data['card']['up_char']['2'][card_name] = '70'
                            if star == 'R':
                                data['card']['up_char']['1'][card_name] = '70'
            char_up_list = list(data['char']['up_char']['3'].keys())
            card_up_list = list(data['card']['up_char']['3'].keys())
            if flag == 0:
                data['char']['title'] = '赛马娘：' + ' & '.join(str(x) for x in char_up_list)
            elif flag == 1:
                data['char']['title'] = '赛马娘：全赛马娘UP'
            data['card']['title'] = '支援卡：' + ' & '.join(str(y) for y in card_up_list)
            img_url_list = []
            for center_img in context.find_all('center'):
                if center_img.find('img'):
                    img_url_list.append(center_img.find('img')['src'])
                else:
                    img_url_list.append('')
            data['char']['pool_img'] = img_url_list[1]
            data['card']['pool_img'] = img_url_list[2]
        except TimeoutError:
            logger.info(f'更新赛马娘UP池信息超时...')
            if pretty_up_char.exists():
                with open(pretty_up_char, 'r', encoding='utf8') as f:
                    data = json.load(f)
            if pretty_up_char.exists():
                with open(pretty_up_char, 'r', encoding='utf8') as f:
                    data = json.load(f)
        return check_write(data, pretty_up_char)