import json
import os
import shutil
from git.repo import Repo

from hoshino import R, logger

# 由于数据量不小，因此采用clone形式下载数据，预计用时1分钟
async def download_info_data():
    data_url = 'https://ghproxy.com/https://github.com/azmiao/uma_info_data.git'
    download_path = os.path.join(R.img('umamusume').path, f'base_data/')
    logger.info('正在更新数据至最新，请耐心等待，预计用时1分钟')
    # 没有就下载
    if not os.path.exists(download_path):
        os.mkdir(download_path)
        Repo.clone_from(data_url, to_path = download_path, branch = 'main')
    # 有就更新
    else:
        repo = Repo(download_path)
        # 判断并更换镜像站
        origin_url = repo.remote('origin').url
        if origin_url != data_url:
            repo.remote('origin').set_url(data_url)
        repo.git.pull()
    logger.info('数据更新完成')

# 删除旧版文件
async def del_dir():
    config_tmp_path = os.path.join(os.path.dirname(__file__), f'config_tmp.json')
    bir_path = os.path.join(R.img('umamusume').path, f'uma_bir/')
    voice_path = os.path.join(R.img('umamusume').path, f'uma_voice/')
    if os.path.exists(bir_path):
        shutil.rmtree(bir_path)
    if os.path.exists(voice_path):
        shutil.rmtree(voice_path)
    if os.path.exists(config_tmp_path):
        os.remove(config_tmp_path)

# 复制配置文件
async def copy_config(config_name, data_path):
    with open(data_path, 'r', encoding='UTF-8') as af:
        data = json.load(af)
    with open(config_name, 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# 更新数据
async def uma_update(current_dir):
    # 首先下载/更新配置文件和数据
    await download_info_data()
    # 删除旧版文件
    await del_dir()
    # 复制配置文件
    data_path = os.path.join(R.img('umamusume').path, f'base_data/config.json')
    await copy_config(current_dir, data_path)