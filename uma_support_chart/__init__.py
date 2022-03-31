import os
import json

from hoshino import Service, logger
from .get_url import generate_img

# 启动时不存在配置文件就生成一个
current_dir = os.path.join(os.path.dirname(__file__), 'sup_config.json')
if not os.path.exists(current_dir):
    img_dict = {}
    with open(current_dir, 'w', encoding='UTF-8') as f:
        json.dump(img_dict, f, indent=4, ensure_ascii=False)
    logger.info(f'节奏榜配置文件不存在，现已成功创建')

sv_help = '''
[速卡节奏榜] 对应速度卡
[耐卡节奏榜] 对应耐力卡
[力卡节奏榜] 对应力量卡
[根卡节奏榜] 对应根性卡
[智卡节奏榜] 对应智力卡
[友人卡节奏榜] 对应友人卡和团队卡
'''.strip()

sv = Service('uma_support_chart', help_=sv_help)

# 帮助界面
@sv.on_fullmatch("支援卡节奏榜帮助")
async def help(bot, ev):
    await bot.send(ev, sv_help)

@sv.on_rex(r'^(\S{1,2})卡节奏榜$')
async def SSR_speed_chart(bot, ev):
    sup_type = ev['match'].group(1)
    if sup_type not in ['速', '耐', '力', '根', '智', '友人']:
        return
    msg = await generate_img(sup_type)
    await bot.send(ev, msg)