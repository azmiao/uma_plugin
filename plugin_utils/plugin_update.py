import json
import os
import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from git.repo import Repo
from hoshino import logger, config, get_bot

from ..plugin_utils.base_util import get_proxy, get_update_type

version_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'version.json')
url = 'https://github.com/azmiao/uma_plugin'


# 初始化马娘插件版本
async def init_plugin(is_force):
    update_type = await get_update_type()
    if not is_force and os.path.exists(version_path):
        return
    if update_type == 'no':
        logger.info('【马娘插件】正在从本地获取马娘插件版本...')
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md'), 'r', encoding='utf-8') as f:
            text = f.read()
        version = re.search(r'release-([0-9]+\.[0-9]+\.[0-9]+f?)-orange\.svg', text).group(1)
        commit_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    else:
        logger.info('【马娘插件】正在在线获取马娘插件版本...')
        data_list, version = await get_commits(url)
        commit_time = data_list[0]['time']
    version_data = {
        'version': version,
        'commit_time': str(commit_time)
    }
    with open(version_path, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=4, ensure_ascii=False)
    logger.info(f'【马娘插件】马娘插件版本获取成功，当前版本[{version}]')


# 更新马娘插件
async def plugin_update_auto():
    update_type = await get_update_type()
    if update_type == 'no':
        return
    flag, is_sup, msg = await judge_update(url)
    if not flag:
        return
    # 如果不是强制更新的版本
    if not is_sup:
        plugin_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uma_plugin')
        logger.info('【马娘插件】检测到插件更新，正在更新插件至最新...')
        repo = Repo(plugin_path)
        # 判断并更换镜像站
        origin_url = repo.remote('origin').url
        if origin_url != url:
            repo.remote('origin').set_url(url)
        repo.git.pull()
        logger.info('【马娘插件】已更新至最新！')
    super_id = config.SUPERUSERS[0]
    bot = get_bot()
    await bot.send_private_msg(user_id=super_id, message=msg)


# 检测马娘插件是否有更新
async def judge_update(rep_url):
    with open(version_path, 'r', encoding="UTF-8") as f:
        version_data = json.load(f)
    old_time = datetime.strptime(version_data['commit_time'], "%Y-%m-%d %H:%M:%S")
    old_version = version_data['version']
    data_list, version = await get_commits(rep_url)
    new_time = data_list[0]['time']
    if new_time <= old_time:
        logger.info('【马娘插件】未检测到更新！')
        return False, False, ''
    msg_header = '【该版本为强制更新版，将不会自动更新，请手动使用git pull -f更新】\n' if version.endswith(
        'f') and old_version != version else '已成功自动更新，请手动重启bot！\n'
    msg = f'【马娘插件】\n版本：{old_version} -> {version}\n{msg_header}更新细节：'
    for data in data_list:
        data_time = data['time']
        if data_time > old_time:
            msg += f'\n▲{data["time"]} {data["author"]}提交了 "{data["title"]}"'
    # 替换监控信息的时间为最新commit时间
    version_data['commit_time'] = str(new_time)
    version_data['version'] = version
    with open(version_path, 'w', encoding="UTF-8") as f:
        json.dump(version_data, f, indent=4, ensure_ascii=False)
    return True, version.endswith('f') and old_version != version, msg


# 调整太平洋时间
async def change_time(raw_time):
    raw_time = str(raw_time).replace('Z', '')
    txt_fmt = raw_time[:10] + " " + raw_time[11:19]
    dt = datetime.strptime(txt_fmt, "%Y-%m-%d %H:%M:%S")
    cur_time = dt + timedelta(hours=8)
    return cur_time


# 获取commits的信息和版本号 | 最近10条
async def get_commits(rep_url):
    data_list = []
    # version
    res = requests.get(rep_url, proxies=get_proxy(), timeout=20)
    version = re.search(r'release-([0-9]+\.[0-9]+\.[0-9]+f?)-orange\.svg', res.text)
    logger.info(f'version=[{version.group(1)}]')
    # commit
    resp = requests.get(rep_url + "/commits", proxies=get_proxy(), timeout=20)
    soup = BeautifulSoup(resp.text, 'lxml')
    soup_find = soup.find('script', {"data-target": "react-app.embeddedData"})
    raw_info = json.loads(soup_find.text.strip())
    commit_info_list = raw_info['payload']['commitGroups']
    for commit_info_by_date in commit_info_list:
        for commit_info in commit_info_by_date['commits']:
            commit_message = commit_info['shortMessage']
            authors_name = ','.join([info['displayName'] for info in commit_info['authors']])
            time = await change_time(commit_info['committedDate'])
            data_list.append({'title': commit_message, 'author': authors_name, 'time': time})
            if len(data_list) >= 10:  # 如果要只取最近10次commit
                break
    return data_list, version.group(1)
