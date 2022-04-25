import os

from hoshino import logger
from .update_type import update as com_update

# 首次启动函数
async def update():
    file_path = os.path.join(os.path.dirname(__file__), 'relation_type.json')
    if not os.path.exists(file_path):
        logger.info('====未检测到马娘相性信息，正在开始更新====')
        await com_update()
        logger.info('====马娘相性信息更新完成====')

# 自动更新
async def auto_update():
    await com_update()
    logger.info(f'已更新相性组文件')