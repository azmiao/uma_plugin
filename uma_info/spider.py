import json
import time
import os
import re
from .chinesefy import get_cn_name
import hoshino
from hoshino import R
from hoshino.typing import MessageSegment
from hoshino import aiorequests
import hoshino
import demjson

# 是否使用ocr_space接口，默认启用
ENABLE_OCR_SPACE = True
# ocr_space接口的apikey
APIKEY = ''

async def uma_spider():
    current_dir = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        uma_data = json.load(f)
        f.close()
    try:
        en_name = uma_data['current_chara']
    except:
        en_name = 'specialweek'
    next_en_name = ''
    while(1):
        time.sleep(0.5)
        if next_en_name == 'specialweek':
            uma_data['current_chara'] = 'specialweek'
            with open(current_dir, 'w', encoding = 'UTF-8') as af:
                json.dump(uma_data, af, indent=4, ensure_ascii=False)
                af.close()
            break
        try:
            data, next_en_name, en_name = await get_info(en_name)
        except aiorequests.exceptions.RequestException:
            return en_name
        uma_data['current_chara'] = en_name
        uma_data[en_name] = data
        hoshino.logger.info(f'成功处理{en_name}的数据！')
        en_name = next_en_name
        with open(current_dir, 'w', encoding = 'UTF-8') as af:
            json.dump(uma_data, af, indent=4, ensure_ascii=False)
            af.close()
    return ''

# 拿到中文名字
async def get_cn():
    current_dir = os.path.join(os.path.dirname(__file__), 'config.json')
    uma_dict = await get_cn_name()
    with open(current_dir, 'r', encoding = 'UTF-8') as f:
        f_data = json.load(f)
        f.close()
    name_list = list(f_data.keys())
    name_list.remove('current_chara')
    for en_name in name_list:
        jp_name = f_data[en_name]['jp_name']
        try:
            cn_name = uma_dict[jp_name]['cn_name']
        except:
            cn_name = ''
        if jp_name == 'ハルウララ':
            cn_name = '春乌拉拉'
        try:
            grass = uma_dict[jp_name]['grass']
            mud = uma_dict[jp_name]['mud']
            short = uma_dict[jp_name]['short']
            mile = uma_dict[jp_name]['mile']
            middle = uma_dict[jp_name]['middle']
            long = uma_dict[jp_name]['long']
            run_away = uma_dict[jp_name]['run_away']
            first = uma_dict[jp_name]['first']
            center = uma_dict[jp_name]['center']
            chase = uma_dict[jp_name]['chase']
        except:
            grass, mud, short, mile, middle, long, run_away, first, center, chase = '', '', '', '', '', '', '', '', '', ''
        f_data[en_name]['cn_name'] = cn_name
        f_data[en_name]['grass'] = grass
        f_data[en_name]['mud'] = mud
        f_data[en_name]['short'] = short
        f_data[en_name]['mile'] = mile
        f_data[en_name]['middle'] = middle
        f_data[en_name]['long'] = long
        f_data[en_name]['run_away'] = run_away
        f_data[en_name]['first'] = first
        f_data[en_name]['center'] = center
        f_data[en_name]['chase'] = chase

    with open(current_dir, 'w', encoding = 'UTF-8') as af:
        json.dump(f_data, af, indent=4, ensure_ascii=False)
        af.close()

async def get_info(en_name):
    url = f'https://umamusume.jp/app/wp-json/wp/v2/character?slug={en_name}'
    params = {
        'pragma': 'no-cache',
        'referer': f'https://umamusume.jp/character/detail/?name={en_name}'
    }
    uma_res = await aiorequests.get(url, params = params, timeout = 10)
    uma_json = await uma_res.json()
    uma_data = uma_json[0]
    detail_img = uma_data['acf']['detail_img']['pc']
    if ENABLE_OCR_SPACE:
        cv, bir, height, weight, measurements = await download_ocr(en_name, detail_img)
    else:
        cv, bir, height, weight, measurements = await send_ocr(en_name, detail_img)
    category = uma_data['acf']['category']['value']
    try:
        voice = uma_data['acf']['voice']
    except:
        voice = ''
    try:
        uniform_img = uma_data['acf']['chara_img'][0]['image']
    except:
        uniform_img =''
    try:
        winning_suit_img = uma_data['acf']['chara_img'][1]['image']
    except:
        winning_suit_img = ''
    try:
        original_img = uma_data['acf']['chara_img'][2]['image']
    except:
        original_img = ''
    data = {
        'id': uma_data['id'],
        'jp_name': uma_data['title']['rendered'],
        'category': category,
        'voice': voice,
        'uniform_img': uniform_img,
        'winning_suit_img': winning_suit_img,
        'original_img': original_img,
        'cv': cv,
        'bir': bir,
        'height': height,
        'weight': weight,
        'measurements': measurements,
        'sns_icon': uma_data['acf']['sns_icon'],
        'prev_en_name': uma_data['next']['slug'],
        'next_en_name': uma_data['prev']['slug']
    }
    return data, data['next_en_name'], en_name

# QQ接口，有毛病，有思路但好麻烦啊，先不改这个了，等gocq支持对发送的图片Ocr就不用这么麻烦了
async def send_ocr(en_name, url):
    bot = hoshino.get_bot()
    superid = hoshino.config.SUPERUSERS[0]
    msg = MessageSegment.image(file = url)
    msgback = await bot.send_private_msg(user_id = superid, message = msg)
    msg_id = msgback['message_id']
    message = await bot.get_msg(message_id=msg_id)
    img_text = message['message']
    img_id_tmp = re.findall(r'CQ:image,file=.+?\.image', img_text)
    img_id = img_id_tmp[0].replace('CQ:image,file=','')
    time.sleep(0.5)
    data = await bot.ocr_image(image = img_id)
    text_list = list(data['texts'])
    cv, bir, height, measurements = '', '', '', ''
    for text in text_list:
        text = str(text)
        cv_tmp = re.search(r'CV:(\S+)', text)
        cv = cv_tmp.group(1) if cv_tmp else cv
        bir_tmp = re.search(r'([0-9]+月[0-9]+日)', text)
        bir = bir_tmp.group(0) if bir_tmp else bir
        bir = bir.replace('月', '-').replace('日', '')
        height_tmp = re.search(r'([0-9]+)cm', text)
        height = height_tmp.group(1) if height_tmp else height
        weight = ''
        measurements_tmp = re.search(r'(B[0-9]+・W[0-9]+・H[0-9]+)', text)
        measurements = measurements_tmp.group(0) if measurements_tmp else measurements
    return cv, bir, height, weight, measurements

# ocr_space接口
async def download_ocr(en_name, url):
    if not os.path.exists(R.img('uma_bir').path):
        os.mkdir(R.img('uma_bir').path)
    response = await aiorequests.get(url, timeout=10)
    resp_data = await response.content
    current_dir = os.path.join(R.img('uma_bir').path, f'{en_name}.png')
    with open(current_dir, 'wb') as f:
        f.write(resp_data)

    api = 'https://api.ocr.space/parse/image'
    apikey = APIKEY
    data = {
        'apikey': apikey,
        'language': 'jpn',
        'filetype': 'PNG',
        'scale': True,
        'detectOrientation': False
    }
    with open(current_dir,'rb') as f:
        resp = await aiorequests.post(api, files = {f'{en_name}.png': f}, data = data, timeout = 60)
        resp.encodin = 'utf-8'
        res_json = await resp.json()
        json_obj = demjson.encode(res_json) # 解决解析json出错问题
    text = json.loads(json_obj)['ParsedResults'][0]['ParsedText'].replace('\r\n', '')
    cv, bir, height, weight, measurements = '', '', '', '', ''
    text = str(text)
    cv_tmp = re.search(r'CV:(\S+)([0-9]+月)', text)
    cv = cv_tmp.group(1) if cv_tmp else cv
    # 修正ocr识别问题
    cv = cv.replace('0', 'o').replace('、', '').replace('小自唯', '小仓唯')
    bir_tmp = re.search(r'([0-9]+月[0-9]+日)', text)
    if bir_tmp:
        bir = bir_tmp.group(0) if bir_tmp else bir
        bir = bir.replace('月', '-').replace('日', '')
        bir_list = bir.split('-', 1)
        bir = '-'.join(str(int(bir_num, 10)) for bir_num in bir_list)
    height_tmp = re.search(r'([0-9][0-9][0-9])5', text)
    height_tmp_2 = re.search(r'([0-9][0-9][0-9])cm', text)
    height_tmp_3 = re.search(r'([0-9][0-9][0-9])。m', text)
    height_tmp_4 = re.search(r'[0-9][0-9][0-9]', text)
    if height_tmp:
        height = height_tmp.group(1)
        weight_tmp = re.search(r'([0-9][0-9][0-9])5(\S*)(B[0-9][0-9])', text)
        weight = weight_tmp.group(2) if weight_tmp else weight
    elif height_tmp_2:
        height = height_tmp_2.group(1)
        weight_tmp = re.search(r'([0-9][0-9][0-9])cm(\S*)(B[0-9][0-9])', text)
        weight = weight_tmp.group(2) if weight_tmp else weight
    elif height_tmp_3:
        height = height_tmp_3.group(1)
        weight_tmp = re.search(r'([0-9][0-9][0-9])。m(\S*)(B[0-9][0-9])', text)
        weight = weight_tmp.group(2) if weight_tmp else weight
    elif height_tmp_4:
        height = height_tmp_4.group(0)
        weight_tmp = re.search(r'([0-9][0-9][0-9])(\S*)(B[0-9][0-9])', text)
        weight = weight_tmp.group(2) if weight_tmp else weight
    else:
        height = height
        weight = weight
    measurements_tmp = re.search(r'(B[0-9]+・W[0-9]+・H[0-9]+)', text)
    measurements = measurements_tmp.group(0) if measurements_tmp else measurements
    # 这写ocr顺序有问题，正则匹配结果异常
    if en_name == 'currenchan':
        cv, weight = '篠原侑', 'ひ・み・つ'
    if en_name == 'marveloussunday':
        cv, bir, height, weight, measurements = '三宅麻理恵', '5-31', '145', 'マーベラス!', 'B87・W52・H77'
    if en_name == 'bikopegasus':
        cv, weight = '田中あいみ', '体重微増（いっぱい食べて大きくなる！）'
    if en_name == "kitasanblack":
        cv, weight = '矢野妃菜喜', 'もりもり成長中!'
    return cv, bir, height, weight, measurements
