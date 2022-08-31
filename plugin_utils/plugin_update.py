import re
import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from git.repo import Repo

from ..plugin_utils.base_util import get_proxy, get_update_type
from hoshino import logger, config, get_bot

version_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'version.json')
url = 'https://github.com/azmiao/uma_plugin'

# 初始化马娘插件版本
async def init_plugin():
    update_type = await get_update_type()
    if update_type == 'no': return
    if os.path.exists(version_path):
        return
    logger.info('【马娘插件】正在获取马娘插件版本...')
    data_list, version = await get_commits(url)
    commit_time = data_list[0]['time']
    version_data = {
        'version': version,
        'commit_time': str(commit_time)
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=4, ensure_ascii=False)
    logger.info('【马娘插件】马娘插件版本获取成功')

# 更新马娘插件
async def plugin_update_auto():
    update_type = await get_update_type()
    if update_type == 'no': return
    flag, msg = await judge_update(url)
    if not flag: return
    git_url = f'https://ghproxy.com/{url}'
    plugin_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uma_plugin')
    logger.info('【马娘插件】检测到插件更新，正在更新插件至最新...')
    repo = Repo(plugin_path)
    # 判断并更换镜像站
    origin_url = repo.remote('origin').url
    if origin_url != git_url:
        repo.remote('origin').set_url(git_url)
    repo.git.pull()
    logger.info('【马娘插件】已更新至最新！')
    superid = config.SUPERUSERS[0]
    bot = get_bot()
    await bot.send_private_msg(user_id=superid, message=msg)

# 检测马娘插件是否有更新
async def judge_update(url):
    with open(version_path, 'r', encoding="UTF-8") as f:
        version_data = json.load(f)
    old_time = datetime.strptime(version_data['commit_time'], "%Y-%m-%d %H:%M:%S")
    old_version = version_data['version']
    data_list, version = await get_commits(url)
    new_time = data_list[0]['time']
    if new_time <= old_time:
        logger.info('【马娘插件】未检测到更新！')
        return False, ''
    msg_header = '【该版本为强制更新版，请手动使用git pull -f更新】\n' if version.endswith('f') else '已成功自动更新，请手动重启bot！\n'
    msg = f'【马娘插件】\n版本：{old_version} -> {version}\n{msg_header}更新细节：'
    for data in data_list:
        data_time = data['time']
        if data_time > old_time:
            msg += f'\n▲{data["time"]} {data["author"]}提交了 "{data["title"]}"'
    # 替换监控信息的时间为最新commit时间
    version_data['commit_time'] = str(new_time)
    with open(version_path, 'w', encoding="UTF-8") as f:
        json.dump(version_data, f, indent=4, ensure_ascii=False)
    return True, msg

# 调整太平洋时间
async def change_time(raw_time):
    raw_time = str(raw_time).replace('Z', '')
    txtfmt = raw_time[:10]+ " " + raw_time[11:19]
    dt = datetime.strptime(txtfmt,"%Y-%m-%d %H:%M:%S")
    cur_time = dt + timedelta(hours=8)
    return cur_time

# 获取commits的信息和版本号 | 最近10条
async def get_commits(url):
    data_list = []
    # version
    res = requests.get(url, proxies = get_proxy(), timeout=20)
    version = re.search(r'release-([0-9]+\.[0-9]+\.[0-9]+f?)-orange\.svg', res.text)
    # commit
    resp = requests.get(url+"/commits", proxies = get_proxy(), timeout=20)
    soup = BeautifulSoup(resp.text, 'lxml')
    block_list = soup.find_all('li', {"class": "Box-row Box-row--focus-gray mt-0 d-flex js-commits-list-item js-navigation-item js-socket-channel js-updatable-content"})
    for block in block_list[:10]:
        if block.find('span', {"class": "hidden-text-expander inline"}):
            block.find('span', {"class": "hidden-text-expander inline"}).decompose()
        try:
            author = block.find('a', {"class": "commit-author user-mention"}).text
        except:
            author = block.find('span', {"class": "commit-author user-mention"}).text
        cur_time = await change_time(block.find('relative-time').get('datetime'))
        data_list.append({
            'title': block.find('p', {"class": "mb-1"}).text.strip(),
            'author': author,
            'time': cur_time
        })
    return data_list, version.group(1)