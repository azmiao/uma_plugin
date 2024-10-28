import os
import shutil

from hoshino import R, logger

from .res_spider import get_res
from .uma_pool import get_pool_data
from .util import update_select_data

gacha_path = os.path.join(R.img('umamusume').path, 'uma_gacha/')


# 首次启动函数
async def update():
    if not os.path.exists(gacha_path):
        os.mkdir(gacha_path)
    if not os.path.exists(os.path.join(gacha_path, 'select_data.json')):
        logger.info('马娘卡池信息不存在，正在重新生成...')
        try:
            # 获取卡池信息
            logger.info(f'正在获取马娘卡池数据...')
            await get_pool_data()
            logger.info(f'马娘卡池数据获取完成！')
            # 下载图片
            logger.info(f'正在开始下载马娘抽卡图片...')
            await get_res()
            logger.info(f'马娘抽卡图片下载完成！')
            # 初始化卡池选择
            logger.info(f'正在初始化马娘卡池选择...')
            await update_select_data()
            logger.info(f'马娘卡池选择文件初始化完成！[默认日服的最新卡池]')
            logger.info(f'正在删除旧版马娘卡池资源...')
            await delete_old_folder()
            logger.info('====马娘抽卡信息更新完成====')
        except Exception as e:
            logger.error(f'马娘卡池信息初始化失败：{e}')


# 自动更新
async def auto_update():
    try:
        # 获取卡池信息
        logger.info(f'正在更新马娘卡池数据...')
        await get_pool_data()
        logger.info(f'马娘卡池数据更新完成！')
        # 下载图片
        logger.info(f'正在更新马娘抽卡图片...')
        await get_res()
        logger.info(f'马娘抽卡图片更新完成！')
        # 初始化卡池选择
        logger.info(f'正在更新马娘卡池选择...')
        await update_select_data()
        logger.info(f'马娘卡池选择文件更新完成！')
        logger.info('====马娘抽卡信息更新完成====')
        return '马娘抽卡信息更新完成'
    except Exception as e:
        logger.error(f'马娘卡池信息更新失败：{e}')
        return f'马娘卡池信息更新失败：{e}'


# 删除旧版文件
async def delete_old_folder():
    await del_files('draw_card')
    await del_files('draw_card_config')
    await del_files('draw_card_up')
    await del_files('pretty_card.json')
    await del_files('pretty.json')


# 删除文件夹内的文件或本身的文件
async def del_files(filename):
    file_path = os.path.abspath(os.path.join(gacha_path, filename))
    if not os.path.exists(file_path):
        return
    if os.path.isfile(file_path):
        os.remove(file_path)
        logger.info(f'文件{filename}已删除')
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
        logger.info(f'文件夹{filename}已删除')
