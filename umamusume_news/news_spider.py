# -*- coding: UTF-8 -*-
import requests
import os,base64
import re
import json
import datetime
from datetime import timedelta
import operator
from .translator_lite.apis import youdao
from io import BytesIO
import yaml
import random
import time
from hoshino import R

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    ]

class news_class:
    def __init__(self,news_time,news_url,news_title):
        self.news_time = news_time
        self.news_url = news_url
        self.news_title = news_title

def get_item():
    time.sleep(1)
    url = 'https://umamusume.jp/api/ajax/pr_info_index?format=json'
    data = {}
    data['announce_label'] = 0
    data['limit'] = 10
    data['offset'] = 0
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': random.choice(user_agent_list),
        'Connection': 'close',
        'origin': 'https://umamusume.jp',
        'referer': 'https://umamusume.jp/news',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/json;charset=UTF-8'
    }
    with requests.post(url=url,data=json.dumps(data),headers=headers, timeout=(5,10), stream = True) as res:
        res_dict = res.json()
        res.close()
    return res_dict

def sort_news():
    res_dict = get_item()
    news_list = []
    for n in range(0, 5):
        if (res_dict['information_list'][n]['update_at'] == None):
            news_time = res_dict['information_list'][n]['post_at']
        else :
            news_time = res_dict['information_list'][n]['update_at']

        news_id = res_dict['information_list'][n]['announce_id']
        news_url = '▲https://umamusume.jp/news/detail.php?id=' + str(news_id)
        news_title = res_dict['information_list'][n]['title']
        news_list.append(news_class(news_time, news_url ,news_title))

    news_key = operator.attrgetter('news_time')
    news_list.sort(key = news_key, reverse = True)
    return news_list

def get_news():
    news_list = sort_news()
    msg = '◎◎ 马娘官网新闻 ◎◎\n'
    for news in news_list:
        time_tmp = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
        news_time = time_tmp - timedelta(hours=1)
        msg = msg + '\n' + str(news_time) + '\n' + news.news_title + '\n' + news.news_url + '\n'
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
    prev_time = news_list[0].news_time
    file = open(current_dir, 'w', encoding="UTF-8")
    file.write(str(prev_time))
    file.close()
    return msg

def news_broadcast():
    news_list = sort_news()
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    init_time = str(file.read())
    file.close()
    init_time = datetime.datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S')
    msg = '◎◎ 马娘官网新闻更新 ◎◎\n'
    for news in news_list:
        prev_time = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
        if (init_time >= prev_time):
            break
        else:
            time_tmp = datetime.datetime.strptime(news.news_time, '%Y-%m-%d %H:%M:%S')
            news_time = time_tmp - timedelta(hours=1)
            msg = msg + '\n' + str(news_time) + '\n' + news.news_title + '\n' + news.news_url + '\n'

    for news in news_list:
        set_time = news.news_time
        break
    file = open(current_dir, 'w', encoding="UTF-8")
    file.write(str(set_time))
    file.close()
    return msg

# 判断一下是否有更新，为什么要单独写一个函数呢
# 函数单独写一个是怎么回事呢？函数相信大家都很熟悉，但是函数单独写一个是怎么回事呢，下面就让小编带大家一起了解吧。
# 函数单独写一个，其实就是我想单独写一个函数，大家可能会很惊讶函数怎么会单独写一个呢？但事实就是这样，小编也感到非常惊讶。
# 这就是关于函数单独写一个的事情了，大家有什么想法呢，欢迎在评论区告诉小编一起讨论哦！
def judge() -> bool:
    current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
    if (os.path.exists(current_dir) == True):
        file = open(current_dir, 'r', encoding="UTF-8")
        init_time = str(file.read())
        file.close()
    else:
        news_list = sort_news()
        for news in news_list:
            init_time = news.news_time
            break
        current_dir = os.path.join(os.path.dirname(__file__), 'prev_time.yml')
        file = open(current_dir, 'w', encoding="UTF-8")
        file.write(str(init_time))
        file.close()

    news_list = sort_news()
    for news in news_list:
        prev_time = news.news_time
        break
    
    if (init_time != prev_time):
        return True
    else:
        return False

# 替换不必要的文本
def replace_text(text_tmp):
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
    # 替换赛马娘游戏术语
    current_dir = os.path.join(os.path.dirname(__file__), 'replace_dict.json')
    file = open(current_dir, 'r', encoding = 'UTF-8')
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader = yaml.FullLoader)
    keys_list = list(config.keys())
    for key in keys_list:
        value = config[key]
        text = text.replace(f'{key}', f'{value}')
    return text

# 翻译完如果把中文又翻译一遍导致出问题可以在这里，再次替换一下？
def second_replace(news_text):
    # news_text = news_text.replace('', '') # 我先注释了
    return news_text

# 翻译新闻
def translate_news(news_id):
    time.sleep(1)
    url = 'https://umamusume.jp/api/ajax/pr_info_detail?format=json'
    data = {}
    data['announce_id'] = news_id
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': random.choice(user_agent_list),
        'Connection': 'close',
        'origin': 'https://umamusume.jp',
        'referer': 'https://umamusume.jp/news',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/json;charset=UTF-8'
    }
    flag = 0
    try:
        with requests.post(url=url,data=json.dumps(data),headers=headers, timeout=(5,10), stream = True) as res:
            res_dict = res.json()
            res.close()
        if res_dict['detail']['title'] == '現在確認している不具合について':
            news_msg = res_dict['detail']['message'][:500] + '...'
            flag = 1
        else:
            news_msg = res_dict['detail']['message']
        news_msg = replace_text(news_msg)
    except:
        news_text = '错误！马娘官网连接失败'
        return news_text
    try:
        news_text = youdao(news_msg, 'ja', 'zh')
        news_text = second_replace(news_text)
        if flag == 1:
            news_text = '(该新闻特别长，因此只显示前500个字符)\n\n' + news_text
        if res_dict['detail']['image_big'] != '':
            img_url = res_dict['detail']['image_big']
            response = requests.get(img_url)
            ls_f = base64.b64encode(BytesIO(response.content).read())
            imgdata = base64.b64decode(ls_f)
            save_dir = R.img('umamusume_news').path
            path_dir = os.path.join(save_dir,'news_img.jpg')
            file = open(path_dir,'wb')
            file.write(imgdata)
            file.close()
            news_img = ' '.join(map(str, [
                R.img(f'umamusume_news/news_img.jpg').cqcode,
            ]))
            news_text = f'{news_img}' + news_text
    except Exception as e:
        # 用于检查错误
        # print('error_check --> news_msg: ' + news_msg)
        e_msg = e
        if str(e) == 'The length of the text to be translated exceeds the limit.':
            e_msg = '详细原因：文章长度过长，禁止翻译！请移步马娘官网查看！'
        news_text = f'错误！翻译失败！{e_msg}'
    return news_text