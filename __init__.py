from hoshino import Service

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
'''.strip()

sv = Service('uma_help', help_ = sv_help)

@sv.on_fullmatch('马娘帮助')
async def get_help(bot, ev):
    await bot.send(ev, sv_help)