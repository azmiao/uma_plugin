from prettytable import PrettyTable
from PIL import Image, ImageDraw, ImageFont
import os

from hoshino import R, logger

# 获取限时任务列表
async def get_title(f_data):
    info_data = {
        'title': '限时任务列表',
        'info': {}
    }
    for task_id in list(f_data['tasks'].keys()):
        title = f_data['tasks'][task_id]['title']
        info_data['info'][task_id] = title
    img_dir = os.path.join(R.img('umamusume').path, 'uma_tasks/tasks_list.png')
    # 图片文件不存在就创建图片
    if not os.path.exists(img_dir):
        logger.info(f'检测到限时任务列表图片不存在正在开始生成')
        await create_img(True, info_data, 'tasks_list.png')
        logger.info(f'检测到限时任务列表图片生成完成，即将发送图片')
    else:
        logger.info(f'限时任务列表图片本地已存在，即将发送图片')
    msg = f'[CQ:image,file=file:///{os.path.abspath(img_dir)}]'
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
        info_data['info'][s_task_id]['race_time'] = f_data['tasks'][task_id]['task_list'][s_task_id]['比赛时间']
        info_data['info'][s_task_id]['race_env'] = f_data['tasks'][task_id]['task_list'][s_task_id]['比赛环境']
        info_data['info'][s_task_id]['suggest_uma'] = f_data['tasks'][task_id]['task_list'][s_task_id]['推荐赛马娘']
        info_data['info'][s_task_id]['reward'] = f_data['tasks'][task_id]['task_list'][s_task_id]['奖励']
    img_dir = os.path.join(R.img('umamusume').path, f'uma_tasks/task_id_{task_id}.png')
    # 图片文件不存在就创建图片
    if not os.path.exists(img_dir):
        logger.info(f'检测到{title}图片不存在正在开始生成')
        await create_img(False, info_data, f'task_id_{task_id}.png')
        logger.info(f'检测到{title}图片生成完成，即将发送图片')
    else:
        logger.info(f'{title}图片本地已存在，即将发送图片')
    msg = f'[CQ:image,file=file:///{os.path.abspath(img_dir)}]'
    return msg

# 生成图片
async def create_img(is_title, info_data, filename_tmp):
    if is_title:
        field_names = ('编号', '任务名')
    else:
        field_names = ('任务名', '达成条件', '比赛时间', '比赛环境', '推荐赛马娘', '奖励')
    titles = info_data['title']
    table = PrettyTable(field_names = field_names, title = titles)

    for id in list(info_data['info'].keys()):
        if is_title:
            task_name = info_data['info'][id]
            table.add_row([id, task_name])
        else:
            task_name = info_data['info'][id]['task_name']
            condition = info_data['info'][id]['condition']
            race_time = info_data['info'][id]['race_time']
            race_env = info_data['info'][id]['race_env']
            suggest_uma = info_data['info'][id]['suggest_uma']
            reward = info_data['info'][id]['reward']
            table.add_row([task_name, condition, race_time, race_env, suggest_uma, reward])

    table_info = str(table)
    space = 5
    current_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'simhei.ttf')
    font = ImageFont.truetype(current_dir, 20, encoding='utf-8')
    im = Image.new('RGB',(10, 10),(255, 255, 255, 0))
    draw = ImageDraw.Draw(im, 'RGB')
    img_size = draw.multiline_textsize(table_info, font=font)
    im_new = im.resize((img_size[0]+space*2, img_size[1]+space*2))
    del draw
    del im
    draw = ImageDraw.Draw(im_new, 'RGB')
    draw.multiline_text((space,space), table_info, fill=(0, 0, 0), font=font)
    save_dir = os.path.join(R.img('umamusume').path, 'uma_tasks/')
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    path_dir = os.path.join(save_dir, filename_tmp)
    im_new.save(path_dir, 'PNG')
    del draw