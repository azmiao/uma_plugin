import asyncio
from hoshino import logger
import os
from .pretty_handle import update_pretty_info, init_pretty_data
from .config import DRAW_PATH

async def async_update_game():
    tasks = []
    init_lst = [init_pretty_data]
    if not os.path.exists(f'{DRAW_PATH}/pretty.json') or not os.path.exists(f'{DRAW_PATH}/pretty_card.json'):
        tasks.append(asyncio.ensure_future(update_pretty_info()))
        init_lst.remove(init_pretty_data)
    try:
        await asyncio.gather(*tasks)
        for func in init_lst:
            await func()
    except asyncio.exceptions.CancelledError:
        logger.info('更新异常：CancelledError，再次更新...')
        await async_update_game()