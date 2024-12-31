import os

from yuiChyan import logger, base_res_path
from yuiChyan.util.chart_generator import create_table, save_fig_as_image
from ..plugin_utils.base_util import get_img_cq

res_path = os.path.join(base_res_path, 'umamusume')


# 获取限时任务列表
async def get_title(f_data):
    info_data = {
        'title': '限时任务列表',
        'info': {}
    }
    for task_id in list(f_data['tasks'].keys()):
        title = f_data['tasks'][task_id]['title']
        info_data['info'][task_id] = title
    img_dir = os.path.join(res_path, 'uma_tasks', 'tasks_list.png')
    # 图片文件不存在就创建图片
    if not os.path.exists(img_dir):
        logger.info(f'检测到限时任务列表图片不存在正在开始生成')
        await create_img(True, info_data, 'tasks_list.png')
        logger.info(f'检测到限时任务列表图片生成完成，即将发送图片')
    else:
        logger.info(f'限时任务列表图片本地已存在，即将发送图片')
    msg = await get_img_cq(img_dir)
    return msg


# 获取限时任务内容
async def get_task_info(task_id, f_data):
    title = f_data['tasks'][task_id]['title']
    info_data = {
        'title': title,
        'info': {}
    }
    for s_task_id in list(f_data['tasks'][task_id]['task_list'].keys()):
        info_data['info'][s_task_id] = {}
        info_data['info'][s_task_id]['task_name'] = f_data['tasks'][task_id]['task_list'][s_task_id]['任务名']
        info_data['info'][s_task_id]['condition'] = f_data['tasks'][task_id]['task_list'][s_task_id]['达成条件']
        info_data['info'][s_task_id]['race_time'] = f_data['tasks'][task_id]['task_list'][s_task_id].get('比赛时间',
                                                                                                         '无')
        info_data['info'][s_task_id]['race_env'] = f_data['tasks'][task_id]['task_list'][s_task_id].get('比赛环境',
                                                                                                        '无')
        info_data['info'][s_task_id]['suggest_uma'] = f_data['tasks'][task_id]['task_list'][s_task_id]['推荐赛马娘']
        info_data['info'][s_task_id]['reward'] = f_data['tasks'][task_id]['task_list'][s_task_id]['奖励']
    img_dir = os.path.join(res_path, 'uma_tasks', f'task_id_{task_id}.png')
    # 图片文件不存在就创建图片
    if not os.path.exists(img_dir):
        logger.info(f'检测到{title}图片不存在正在开始生成')
        await create_img(False, info_data, f'task_id_{task_id}.png')
        logger.info(f'检测到{title}图片生成完成，即将发送图片')
    else:
        logger.info(f'{title}图片本地已存在，即将发送图片')
    msg = await get_img_cq(img_dir)
    return msg


# 生成图片
async def create_img(is_title, info_data, filename_tmp):
    if is_title:
        raw_data = {
            'title': info_data['title'],
            'index_column': 'task_id',
            'show_columns': {
                'task_id': '编号',
                'task_name': '任务名'
            }
        }
    else:
        raw_data = {
            'title': info_data['title'],
            'index_column': 'task_name',
            'show_columns': {
                'task_name': '任务名',
                'condition': '达成条件',
                'race_time': '比赛时间',
                'race_env': '比赛环境',
                'suggest_uma': '推荐赛马娘',
                'reward': '奖励'
            }
        }

    data_list = []
    for task_id in list(info_data['info'].keys()):
        if is_title:
            task_name = info_data['info'][task_id]
            data_list.append({
                'task_id': task_id,
                'task_name': task_name
            })
        else:
            task_name = info_data['info'][task_id]['task_name']
            condition = info_data['info'][task_id]['condition']
            race_time = info_data['info'][task_id]['race_time']
            race_env = info_data['info'][task_id]['race_env']
            suggest_uma = info_data['info'][task_id]['suggest_uma']
            reward = info_data['info'][task_id]['reward']
            data_list.append({
                'task_name': task_name,
                'condition': condition,
                'race_time': race_time,
                'race_env': race_env,
                'suggest_uma': suggest_uma,
                'reward': reward,
            })

    fig = await create_table(raw_data)
    save_dir = os.path.join(res_path, 'uma_tasks')
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    path_dir = os.path.join(save_dir, filename_tmp)
    await save_fig_as_image(fig, path_dir)
