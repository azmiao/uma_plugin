from hoshino import Service, R
import os
import shutil

sv_help = '''
马娘相关功能命令列表：

马娘签到
马娘数据帮助
支援卡节奏榜帮助
马娘新闻帮助
马娘抽卡帮助
马娘耐力帮助
马娘相性帮助
马娘表情包帮助
马娘漫画帮助
马娘限时任务帮助
马娘技能帮助

注：数据来自马娘官网和Bwiki
'''.strip()

sv = Service('uma_help', help_ = sv_help)

@sv.on_fullmatch('马娘帮助')
async def get_help(bot, ev):
    await bot.send(ev, sv_help)

# v1.5.2将图片文件夹合并至一个文件夹
root_path = R.img('umamusume').path
def move_dir(dir_name):
    if os.path.exists(R.img(dir_name).path):
        shutil.move(os.path.abspath(R.img(dir_name).path), os.path.abspath(root_path))

if not os.path.exists(root_path):
    os.mkdir(root_path)
    move_dir('uma_bir')
    move_dir('uma_comic')
    move_dir('uma_face')
    move_dir('uma_support_chart')
    move_dir('uma_voice')
    move_dir('umamusume_news')
# 这样独立版马娘抽卡删除后再装本整合版可以通用
move_dir('uma_gacha')