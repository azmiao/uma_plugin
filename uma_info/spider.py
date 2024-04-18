import os

from git.repo import Repo
from hoshino import R, logger

from ..plugin_utils.base_util import delete_dir, delete_file, copy_file

# 基础数据源
data_url = 'https://github.com/azmiao/uma_info_data.git'


# 由于数据量不小，因此采用clone形式下载数据，预计用时1分钟
async def download_info_data() -> bool:
    download_path = os.path.join(R.img('umamusume').path, f'base_data/')
    logger.info('> Updating base uma data...')
    try:
        if not os.path.exists(download_path):
            # 没有就下载
            logger.info('Base uma data is not existed, then we will download it, please be waiting...')
            os.mkdir(download_path)
            Repo.clone_from(data_url, to_path=download_path, branch='main')
        else:
            # 有就更新
            repo = Repo(download_path)
            # 判断并更换数据源站
            origin_url = repo.remote('origin').url
            if origin_url != data_url:
                repo.remote('origin').set_url(data_url)
            repo.git.pull()
        logger.info('> Base uma data update success!')
        return True
    except Exception as e:
        logger.error(f'> Base uma data update failed: {e}')
        return False


# 删除旧版文件
async def del_all_dir():
    # 需要删除的路径
    delete_path_list = [
        os.path.join(R.img('umamusume').path, f'uma_bir'),
        os.path.join(R.img('umamusume').path, f'uma_voice')
    ]
    # 需要删除的文件
    delete_file_list = [
        os.path.join(os.path.dirname(__file__), f'config_tmp.json'),
        os.path.join(os.path.dirname(__file__), f'config.json')
    ]
    for delete_path in delete_path_list:
        await delete_dir(delete_path)
    for file in delete_file_list:
        await delete_file(file)


# 更新数据
async def uma_update(current_dir):
    # 首先下载/更新配置文件和数据
    success = await download_info_data()
    if not success:
        return
    # 删除旧版文件
    await del_all_dir()
    # 复制配置文件
    data_path = os.path.join(R.img('umamusume').path, f'base_data', 'config_v2.json')
    await copy_file(data_path, current_dir)
