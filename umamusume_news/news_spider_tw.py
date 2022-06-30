import os
import time
import requests
import operator
import random
import asyncio
import datetime
from datetime import timedelta

from .news_spider import proxy

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
    def __init__(self,news_time,news_url,news_title):
        self.news_time = news_time
        self.news_url = news_url
        self.news_title = news_title

# 获取列表
async def get_item():
    await asyncio.sleep(0.5)
    url = 'https://l11-web-api.komoejoy.com/game/website/content/107075/2/list?pageNum=1&pageSize=10&region=3'
    headers = {
        'User-Agent': random.choice(user_agent_list),
        'origin': 'https://uma.komoejoy.com',
        'referer': 'https://uma.komoejoy.com',
    }
    res_dict = requests.get(url=url, headers=headers, timeout=15, proxies=proxy).json()
    return res_dict

# 调整新闻列表
async def sort_news():
    res_dict = await get_item()
    news_list = []
    for n in range(0, 5):
        publish_time = res_dict['data'][n]['publish_time']
        time_tuple = time.localtime(int(str(publish_time)[:10]))
        news_time = time.strftime('%Y-%m-%d %H:%M:%S', time_tuple)
        news_id = res_dict['data'][n]['code']
        news_url = '▲https://uma.komoejoy.com/news.html?detail=' + str(news_id)
        news_title = res_dict['data'][n]['title']
        news_list.append(news_class(news_time, news_url ,news_title))

    news_key = operator.attrgetter('news_time')
    news_list.sort(key = news_key, reverse = True)
    return news_list

# 获取新闻
async def get_news_tw():
    news_list = await sort_news()
    msg = '◎◎ 台服马娘新闻 ◎◎\n'
    for news in news_list:
        time_tmp = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
        news_time = time_tmp - timedelta(hours=1)
        msg += '\n' + str(news_time) + '\n' + news.news_title + '\n' + news.news_url + '\n'
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time_tw.yml')
    prev_time = news_list[0].news_time
    with open(current_dir, 'w', encoding="UTF-8") as f:
        f.write(str(prev_time))
    return msg

# 获取新闻更新
async def news_broadcast_tw():
    news_list = await sort_news()
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time_tw.yml')
    with open(current_dir, 'r', encoding="UTF-8") as f:
        init_time = str(f.read())
    init_time = datetime.datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S')
    msg = '◎◎ 台服马娘新闻更新 ◎◎\n'
    for news in news_list:
        prev_time = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
        if (init_time >= prev_time):
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
async def judge_tw() -> bool:
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time_tw.yml')
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