import asyncio
import datetime
import json
import operator
import os
import random
import re
from datetime import timedelta

import requests
from bs4 import BeautifulSoup
from hoshino import R

from .translator_lite.apis import youdao
from ..plugin_utils.base_util import get_img_cq, get_proxy

# 随机挑选一个小可爱作为header
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
]

# 新闻类
class news_class:
    def __init__(self, news_time, news_url, news_title):
        self.news_time = news_time
        self.news_url = news_url
        self.news_title = news_title


# 获取列表
async def get_item():
    await asyncio.sleep(0.5)
    url = 'https://umamusume.jp/api/ajax/pr_info_index?format=json'
    data = {
        'announce_label': 0,
        'limit': 10,
        'offset': 0
    }
    headers = {
        'User-Agent': random.choice(user_agent_list),
        'origin': 'https://umamusume.jp',
        'referer': 'https://umamusume.jp/news',
    }
    res_dict = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=15, proxies=get_proxy()).json()
    return res_dict


# 调整新闻列表
async def sort_news():
    res_dict = await get_item()
    news_list = []
    for n in range(0, 5):
        if not res_dict['information_list'][n]['update_at']:
            news_time = res_dict['information_list'][n]['post_at']
        else:
            news_time = res_dict['information_list'][n]['update_at']

        news_id = res_dict['information_list'][n]['announce_id']
        news_url = 'https://umamusume.jp/news/detail.php?id=' + str(news_id)
        res = requests.post('https://osdb.link/', json={'url': news_url}, headers={'Content-Type': 'application/json'})
        soup = BeautifulSoup(res.text, 'lxml')
        news_url = '▲[短链]' + soup.find('label', {"id": "surl"}).text.replace('Your shortened URL is:', '').strip()
        news_title = res_dict['information_list'][n]['title']
        news_list.append(news_class(news_time, news_url, news_title))

    news_key = operator.attrgetter('news_time')
    news_list.sort(key=news_key, reverse=True)
    return news_list


# 获取新闻
async def get_news():
    news_list = await sort_news()
    msg = '◎◎ 马娘官网新闻 ◎◎\n'
    for news in news_list:
        time_tmp = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
        news_time = time_tmp - timedelta(hours=1)
        msg += '\n' + str(news_time) + '\n' + news.news_title + '\n' + news.news_url + '\n'
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
    prev_time = news_list[0].news_time
    with open(current_dir, 'w', encoding="UTF-8") as f:
        f.write(str(prev_time))
    return msg


# 获取新闻更新
async def news_broadcast():
    news_list = await sort_news()
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
    with open(current_dir, 'r', encoding="UTF-8") as f:
        init_time = str(f.read())
    init_time = datetime.datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S')
    msg = '◎◎ 马娘官网新闻更新 ◎◎\n'
    for news in news_list:
        prev_time = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
        if init_time >= prev_time:
            break
        else:
            time_tmp = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
            news_time = time_tmp - timedelta(hours=1)
            msg += '\n' + str(news_time) + '\n' + news.news_title + '\n' + news.news_url + '\n'

    for news in news_list:
        set_time = news.news_time
        break
    with open(current_dir, 'w', encoding="UTF-8") as f:
        f.write(str(set_time))
    return msg


# 判断一下是否有更新，为什么要单独写一个函数呢
# 函数单独写一个是怎么回事呢？函数相信大家都很熟悉，但是函数单独写一个是怎么回事呢，下面就让小编带大家一起了解吧。
# 函数单独写一个，其实就是我想单独写一个函数，大家可能会很惊讶函数怎么会单独写一个呢？但事实就是这样，小编也感到非常惊讶。
# 这就是关于函数单独写一个的事情了，大家有什么想法呢，欢迎在评论区告诉小编一起讨论哦！
async def judge() -> bool:
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
    news_list = await sort_news()
    if os.path.exists(current_dir):
        with open(current_dir, 'r', encoding="UTF-8") as f:
            init_time = str(f.read())
    else:
        with open(current_dir, 'w', encoding="UTF-8") as f:
            f.write('2022-01-01 00:00:00')
        return True
    for news in news_list:
        prev_time = news.news_time
        break

    if (init_time != prev_time):
        return True
    else:
        return False


# 替换不必要的文本
async def replace_text(text_tmp):
    # 替换多余的html关键字
    text = text_tmp.replace('&nbsp;', ' ')
    text = re.sub(r'<div.*?>', '', text)
    text = text.replace('</div>', '')
    text = re.sub(r'<span.*?>', '', text)
    text = text.replace('</span>', '')
    text = re.sub(r'<strong.*?>', '', text)
    text = text.replace('</strong>', '')
    text = re.sub(r'<h2.*?>', '\n', text)
    text = text.replace('</h2>', '')
    text = re.sub(r'<h3.*?>', '\n', text)
    text = text.replace('</h3>', '')
    text = re.sub(r'<figure>.*?<\/figure>', '', text)
    text = re.sub(r'<exclusion-game>.*<\/exclusion-game>', '', text)
    text = re.sub(r'<br>', '\n\n', text)
    # 替换部分游戏术语
    current_dir = os.path.join(os.path.dirname(__file__), 'replace_dict.json')
    with open(current_dir, 'r', encoding='UTF-8') as other_file:
        other_dict = json.load(other_file)
    for key in list(other_dict.keys()):
        value = other_dict[key]
        text = text.replace(f'{key}', f'{value}')
    # 替换马娘名字，来自马娘基础数据库
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uma_info/config.json'), 'r',
              encoding='UTF-8') as f:
        f_data = json.load(f)
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for uma_name in name_list:
        jp_name = f_data[uma_name]['jp_name']
        cn_name = f_data[uma_name]['cn_name']
        text = text.replace(f'{jp_name}', f'{cn_name}')
    return text


# 翻译完如果把中文又翻译一遍导致出问题可以在这里，再次替换一下？
async def second_replace(news_text):
    # news_text = news_text.replace('', '') # 我先注释了
    return news_text


# 翻译新闻
async def translate_news(news_id):
    await asyncio.sleep(0.5)
    url = 'https://umamusume.jp/api/ajax/pr_info_detail?format=json'
    data = {'announce_id': news_id}
    headers = {
        'User-Agent': random.choice(user_agent_list),
        'origin': 'https://umamusume.jp',
        'referer': 'https://umamusume.jp/news',
    }
    head_img = ''
    try:
        res_dict = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=15,
                                 proxies=get_proxy()).json()
        if res_dict['detail']['title'] == '現在確認している不具合について':
            news_msg = re.match(r'([\s\S]+?【[\s\S]+?)【', res_dict['detail']['message']).group(1)
        else:
            news_msg = res_dict['detail']['message']
        news_msg = await replace_text(news_msg)
    except:
        news_text = '错误！马娘官网连接失败'
        return head_img, news_text
    try:
        news_text = youdao(news_msg, 'ja', 'zh')
        news_text = await second_replace(news_text)
        if res_dict['detail']['image_big']:
            img_url = res_dict['detail']['image_big']
            dir_path = os.path.join(R.img('umamusume').path, 'umamusume_news/')
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            save_dir = os.path.join(R.img('umamusume').path, f'umamusume_news/news_img_{news_id}.jpg')
            if not os.path.exists(save_dir):
                response = requests.get(url=img_url, proxies=get_proxy())
                with open(save_dir, 'wb') as f:
                    f.write(response.content)
            img_path = R.img(f'umamusume/umamusume_news/news_img_{news_id}.jpg').path
            head_img = await get_img_cq(img_path)
    except Exception as e:
        e_msg = e
        if str(e) == 'The length of the text to be translated exceeds the limit.':
            e_msg = '文章长度超过5000字符无法翻译！'
        news_text = f'错误！翻译失败！{e_msg}'
    return head_img, news_text
