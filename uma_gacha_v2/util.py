import datetime
import json
import os

from PIL import Image

from yuiChyan import base_res_path
from yuiChyan.util import pic2b64
from ..plugin_utils.base_util import get_server_default

# =====可调整数据=====

# 需要支持的服务器列表，添加时添加服务器名和开服时间即可，未开服的瞎写一个大点的时间就行
# 默认：日服jp，台服tw，韩服ko，B服bili
server_data = {
    'jp': '2021-02-24',
    'tw': '2022-06-29',
    'ko': '2022-06-20',
    'bili': '2023-08-29'
}

# ===================

gacha_path = os.path.join(os.path.join(base_res_path, 'umamusume'), 'uma_gacha')
server_list = list(server_data.keys())

# 梦开始的地方
init_data = {
    'other_uma': {
        '3': ['特别周', '无声铃鹿', '东海帝皇', '丸善斯基', '小栗帽', '大树快车', '目白麦昆', '鲁道夫象征', '米浴'],
        '2': ['黄金船', '伏特加', '大和赤骥', '草上飞', '神鹰', '气槽', '摩耶重炮', '超级小海湾'],
        '1': ['目白赖恩', '爱丽速子', '胜利奖券', '樱花进王', '春乌拉拉', '待兼福来', '优秀素质', '帝王光辉']
    },
    'other_chart': {
        'SSR': [
            '【輝く景色の、その先に】サイレンススズカ', '【夢は掲げるものなのだっ！】トウカイテイオー',
            '【Run(my)way】ゴールドシチー', '【はやい！うまい！はやい！】サクラバクシンオー',
            '【まだ小さな蕾でも】ニシノフラワー',
            '【必殺！Wキャロットパンチ！】ビコーペガサス', '【不沈艦の進撃】ゴールドシップ', '【待望の大謀】セイウンスカイ',
            '【天をも切り裂くイナズマ娘！】タマモクロス', '【一粒の安らぎ】スーパークリーク',
            '【千紫万紅にまぎれぬ一凛】グラスワンダー',
            '【飛び出せ、キラメケ】アイネスフウジン', '【B·N·Winner!!】ウイニングチケット',
            '【感謝は指先まで込めて】ファインモーション',
            '【7センチの先へ】エアシャカール', '【ロード·オブ·ウオッカ】ウオッカ', '【ようこそ、トレセン学園へ！】駿川たづな',
            '【パッションチャンピオーナ！】エルコンドルパサー', '【これが私のウマドル道☆】スマートファルコン',
            '【日本一のステージを】スペシャルウィーク'
        ],
        'SR': [
            '【やれやれ、お帰り】フジキセキ', '【努力は裏切らない！】ダイワスカーレット', '【テッペンに立て！】ヒシアマゾン',
            '【副会長の一刺し】エアグルーヴ', '【デジタル充電中+】アグネスデジタル', '【検証、開始】ビワハヤヒデ',
            '【カワイイ＋カワイイは～？】マヤノトップガン', '【雨の独奏、私の独創】マンハッタンカフェ',
            '【鍛えぬくトモ】ミホノブルボン', '【鍛えて、応えて！】メジロライアン', '【シチーガール入門＃】ユキノビジン',
            '【生体Aに関する実験的研究】アグネスタキオン', '【0500·定刻通り】エイシンフラッシュ',
            '【波立つキモチ】ナリタタイシン',
            '【マーベラス☆大作戦】マーベラスサンデー', '【運の行方】マチカネフクキタル',
            '【幸せと背中合わせ】メイショウドトウ',
            '【目線は気にせず】メジロドーベル', '【…ただの水滴ですって】ナイスネイチャ', '【一流プランニング】キングヘイロー',
            '【共に同じ道を！】桐生院葵', '【これがウチらのいか焼きや！】タマモクロス'
        ]
    }
}


# 计算开服时间差, 前面大后面小时返回为正数，反之则反
async def get_differ(server_a, server_b) -> int:
    server_A_time = datetime.datetime.strptime(server_data[server_a], '%Y-%m-%d')
    server_B_time = datetime.datetime.strptime(server_data[server_b], '%Y-%m-%d')
    differ = (server_A_time - server_B_time).days
    return differ


# 根据某个服的卡池ID计算其他池子对应的卡池ID
# 输入：服务器A 和 服务器B 和 服务器A的某个卡池ID
# 输出：服务器B的对应卡池ID
async def get_correspond(server_a, server_b, pool_id) -> str:
    if pool_id == '00000000':
        return pool_id
    if (server_a not in server_list) or (server_b not in server_list):
        raise 'input error: server_A or server_B not in server_list!'
    differ = await get_differ(server_a, server_b)
    year, month, day = pool_id[:4], pool_id[4:6], pool_id[6:8]
    A_time = datetime.datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')
    B_time = A_time - datetime.timedelta(days=differ)
    new_pool_id = str(B_time).replace('-', '')[:8]
    return new_pool_id


# 获取某个服务器的最新卡池ID
async def get_new_pool_id(server):
    pool_data_path = os.path.join(gacha_path, 'uma_pool.json')
    with open(pool_data_path, 'r', encoding='utf-8') as f:
        pool_data = json.load(f)
    pool_list = list(pool_data[server].keys())
    return pool_list[0]


# 创建服务器选择数据文件
# 文件已经存在的话会更新最新的池子ID，不会修改选择的服务器和默认服务器
async def update_select_data():
    select_data_path = os.path.join(gacha_path, 'select_data.json')
    default_server = await get_server_default()
    pool_id_default = await get_new_pool_id(default_server)
    # 文件存在
    if os.path.exists(select_data_path):
        with open(select_data_path, 'r', encoding='utf-8') as f:
            select_data = json.load(f)
        # 修改默认池子的ID
        old_pool_id = select_data['default']['pool_id']
        server_default = select_data['default']['server']
        pool_id_default = await get_new_pool_id(server_default)
        if old_pool_id != pool_id_default:
            # 新ID和旧ID不一致 | 需要重置目标选择
            await reset_all_target()
        select_data['default']['pool_id'] = pool_id_default
        # 修改分群的池子的ID
        group_list = list(select_data['group'].keys())
        for group_id in group_list:
            server = select_data['group'][group_id]['server']
            pool_id = await get_new_pool_id(server)
            select_data['group'][group_id]['pool_id'] = pool_id
    # 文件不存在，即首次使用
    else:
        select_data = {
            'default': {
                'server': default_server,
                'pool_id': pool_id_default
            },
            'group': {}
        }
        # 首次使用需要创建目标选择文件
        await reset_all_target()
    with open(select_data_path, 'w', encoding='utf-8') as f:
        # noinspection PyTypeChecker
        json.dump(select_data, f, ensure_ascii=False, indent=4)


# 重置所有目标选择
async def reset_all_target():
    target_path = os.path.join(os.path.dirname(__file__), 'gacha_target.json')
    with open(target_path, 'w', encoding='utf-8') as f:
        # noinspection PyTypeChecker
        json.dump({}, f, ensure_ascii=False, indent=4)


# 获取当前群使用的卡池
# 返回：服务器, 池子ID
async def get_pool(group_id: str):
    select_data_path = os.path.join(gacha_path, 'select_data.json')
    with open(select_data_path, 'r', encoding='utf-8') as f:
        select_data = json.load(f)
    group_list = list(select_data['group'].keys())
    if group_id not in group_list:
        return select_data['default']['server'], select_data['default']['pool_id']
    else:
        return select_data['group'][group_id]['server'], select_data['group'][group_id]['pool_id']


# 获取单个卡的图片路径
async def get_img_path(chara, gacha_type):
    res_data_path = os.path.join(gacha_path, 'uma_res.json')
    with open(res_data_path, 'r', encoding='utf-8') as f:
        res_data = json.load(f)
    filename = res_data[f'{gacha_type}_res'][chara]['filename']
    img_path = os.path.join(gacha_path, f'{gacha_type}_res', filename)
    img_path_abs = os.path.abspath(img_path)
    return img_path_abs


# 将支援卡名称和ID映射成字典
async def get_chart_name_dict():
    res_data_path = os.path.join(gacha_path, 'uma_res.json')
    with open(res_data_path, 'r', encoding='utf-8') as f:
        res_data = json.load(f)
    res_dict = res_data.get('chart_res', {})
    # 名称-ID
    chart_name_dict = {key: value.get('filename', '').replace('Support_thumb_', '').replace('.png', '')
                       for key, value in res_dict.items()}
    # ID-名称
    chart_id_dict = {value: key for key, value in chart_name_dict.items()}
    return chart_name_dict, chart_id_dict


# 生成多抽的图片
async def generate_img(result_list: list, gacha_type):
    # 图片压缩倍率，1为不压缩，越大压缩率越高，默认2节省带宽
    zoom = 2
    height_count = max((len(result_list) - 1) // 5 + 1, 2)
    w = 256 // zoom if gacha_type == 'uma' else 384 // zoom
    h = 280 // zoom if gacha_type == 'uma' else 512 // zoom
    full_wh = (w * 5, h * height_count)
    background = Image.new('RGBA', full_wh, 'white')
    for i in range(1, len(result_list) + 1, 1):
        column = i % 5 - 1
        if column == -1:
            column = 4
        row = (i - 1) // 5
        pos = (column * w, row * h)
        chara = result_list[i - 1]
        img_path = await get_img_path(chara, gacha_type)
        avatar = Image.open(img_path).convert("RGBA")
        avatar = avatar.resize((w, h))
        background.paste(avatar, pos)
    result_image = pic2b64(background)
    return result_image


# 生成评价
async def random_comment(result, gacha_type, first_up, gacha_select):
    s3_rank = '3★ × ' if gacha_type == 'uma' else 'SSR × '
    s2_rank = '2★ × ' if gacha_type == 'uma' else 'SR × '
    s1_rank = '1★ × ' if gacha_type == 'uma' else 'R × '
    msg = f'\n本次{gacha_select}抽卡获得:\n'
    msg += f'UP卡 × {len(result["up"])}\n{s3_rank}{len(result["s3"])} (UP外)\n'
    msg += f'{s2_rank}{len(result["s2"])}\n{s1_rank}{len(result["s1"])}'
    if gacha_select == '十连':
        if result['up']:
            msg += f'\nPS.十连出{len(result["up"])}张UP，兄弟姐妹们，有挂！'
        elif result['s3']:
            msg += f'\nPS.十连歪到{len(result["s3"])}张彩，这就是欧皇吗？'
    else:
        msg += f'\n其中第{first_up}抽首次出UP卡'
    return msg


# 切换服务器
async def switch_server(group_id, server):
    now_server, _ = await get_pool(group_id)
    if server == now_server:
        return f'本群已选择服务器{server}了，无需再次切换'
    select_data_path = os.path.join(gacha_path, 'select_data.json')
    with open(select_data_path, 'r', encoding='utf-8') as f:
        select_data = json.load(f)
    group_data = select_data['group'].get(group_id, {})
    group_data['server'] = server
    pool_id = await get_new_pool_id(server)
    group_data['pool_id'] = pool_id
    select_data['group'][group_id] = group_data
    with open(select_data_path, 'w', encoding='utf-8') as f:
        # noinspection PyTypeChecker
        json.dump(select_data, f, ensure_ascii=False, indent=4)
    await reset_all_target()
    msg = f'本群已成功切换到服务器{server}，并默认选取该服务器最新卡池'
    if server == 'bili':
        msg = f'本群已成功切换到服务器{server}，但由于目前暂未开服，仅提供开服卡池供娱乐，开服后会自动同步'
    return msg


# 切换卡池
async def switch_pool_id(group_id, pool_id):
    now_server, now_pool_id = await get_pool(group_id)
    if pool_id == now_pool_id:
        return f'本群已选择{now_server}服的卡池{pool_id}了，无需再次切换'
    # 获取卡池信息
    pool_data_path = os.path.join(gacha_path, 'uma_pool.json')
    with open(pool_data_path, 'r', encoding='utf-8') as f:
        pool_data = json.load(f)
    pool_list = list(pool_data[now_server].keys())
    if pool_id not in pool_list:
        msg = f'{now_server}中未找到该卡池！\n由于卡池ID过多，您可以去bwiki上查找需要的卡池\n'
        msg += f'注：卡池命名方式为卡池开始日期的前8位数字\n例如2022/07/29 12:00~2022/08/10 11:59对应的ID为：20220709'
        msg += f'\n另附bwiki的卡池链接：https://wiki.biligame.com/umamusume/%E5%8D%A1%E6%B1%A0'
        return msg
    # 修改
    select_data_path = os.path.join(gacha_path, 'select_data.json')
    with open(select_data_path, 'r', encoding='utf-8') as f:
        select_data = json.load(f)
    group_data = select_data['group'].get(group_id, {})
    group_data['server'] = now_server
    group_data['pool_id'] = pool_id
    select_data['group'][group_id] = group_data
    with open(select_data_path, 'w', encoding='utf-8') as f:
        # noinspection PyTypeChecker
        json.dump(select_data, f, ensure_ascii=False, indent=4)
    await reset_all_target()
    return f'本群已成功切换到{now_server}服的卡池{pool_id}'


# 获取当前卡池的信息详情
async def get_pool_detail(group_id):
    server, pool_id = await get_pool(group_id)
    pool_data_path = os.path.join(gacha_path, 'uma_pool.json')
    with open(pool_data_path, 'r', encoding='utf-8') as f:
        pool_data = json.load(f)
    pool_detail = pool_data[server][pool_id]
    msg = f'本群已选{server}服卡池:{pool_id}\n时间: {pool_detail["pool_time"]}\n'
    up_msg_uma = "\n".join(pool_detail["uma_up"]["3"])
    msg += f'[CQ:image,file={pool_detail["uma_title_img"]}]\n'
    msg += f'马娘池:{pool_detail["uma_title"]}\n3星UP:\n{up_msg_uma}\n'
    up_msg_chart = "\n".join(pool_detail["chart_up"]["SSR"])
    msg += f'[CQ:image,file={pool_detail["chart_title_img"]}]\n'
    msg += f'支援卡池:{pool_detail["chart_title"]}\nSSR UP:\n{up_msg_chart}'
    return msg
