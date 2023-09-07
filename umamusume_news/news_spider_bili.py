import asyncio
import datetime
import operator
import os
import random

import requests

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
    url = 'https://api.biligame.com/news/list?gameExtensionId=1006&positionId=2&pageNum=1&pageSize=10'
    headers = {
        'User-Agent': random.choice(user_agent_list),
        'origin': 'https://game.bilibili.com',
        'referer': 'https://game.bilibili.com',
    }
    res_dict = requests.get(url=url, headers=headers, timeout=15).json()
    return res_dict


# 调整新闻列表
async def sort_news():
    res_dict = await get_item()
    news_list = []
    for n in range(0, 5):
        news_time = res_dict['data'][n]['modifyTime']
        news_id = res_dict['data'][n]['id']
        news_url = '▲https://game.bilibili.com/pd/news/#news_detail_id=' + str(news_id)
        news_title = res_dict['data'][n]['title']
        news_list.append(news_class(news_time, news_url, news_title))

    news_key = operator.attrgetter('news_time')
    news_list.sort(key=news_key, reverse=True)
    return news_list


# 获取新闻
async def get_news_bili():
    news_list = await sort_news()
    msg = '◎◎ B服马娘新闻 ◎◎\n'
    for news in news_list:
        news_time = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
        msg += '\n' + str(news_time) + '\n' + news.news_title + '\n' + news.news_url + '\n'
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time_bili.yml')
    prev_time = news_list[0].news_time
    with open(current_dir, 'w', encoding="UTF-8") as f:
        f.write(str(prev_time))
    return msg


# 获取新闻更新
async def news_broadcast_bili():
    news_list = await sort_news()
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time_tw.yml')
    with open(current_dir, 'r', encoding="UTF-8") as f:
        init_time = str(f.read())
    init_time = datetime.datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S')
    msg = '◎◎ B服马娘新闻更新 ◎◎\n'
    for news in news_list:
        prev_time = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
        if (init_time >= prev_time):
            break
        else:
            news_time = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
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
async def judge_bili() -> bool:
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time_bili.yml')
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
