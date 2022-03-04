import httpx
import re
import os
from PIL import Image
from bs4 import BeautifulSoup

def generate_url(sup_type):
    # 先保留rank吧，防止跟以前的根卡界面一样
    rank = 'SSR'
    # 试了下，发现bwiki是可以自动跳转的，所以可以这样写，还减少了反爬虫的概率
    # 等啥时候不能自动跳转了再说吧
    if sup_type == '速卡':
        chart_url = 'https://wiki.biligame.com/umamusume/SSR速卡节奏榜（Ver.1.15.2）已更新成田路'
    elif sup_type == '耐卡':
        chart_url = 'https://wiki.biligame.com/umamusume/SSR耐卡节奏榜（Ver.1.16.0）已更新目白光明'
    elif sup_type == '力卡':
        chart_url = 'https://wiki.biligame.com/umamusume/SSR力卡节奏榜（Ver.1.13.2）已更新爱丽数码'
    elif sup_type == '根卡':
        chart_url = 'https://wiki.biligame.com/umamusume/SSR根卡节奏榜（Ver.1.15.2）已更新SR织姬'
    elif sup_type == '智卡':
        chart_url = 'https://wiki.biligame.com/umamusume/SSR智卡节奏榜（Ver.1.15.2）已更新周年光钻'
    img_dict = get_img(rank, sup_type, chart_url)
    return img_dict

def get_img(rank, sup_type, chart_url):
    res = httpx.get(chart_url, timeout=10)
    soup = BeautifulSoup(res.text, 'lxml')
    pattern = re.compile(f'{rank}{sup_type}节奏榜\S+')
    # 这里获取URL的真实名称
    true_id = soup.find(text=pattern)
    ver = re.search(r'(Ver\.)([0-9]*\.[0-9]*\.[0-9]*)', str(true_id))
    ver = ver.group(2)
    sup_type_tmp = sup_type.replace('卡', '')
    pattern_img = re.compile(f'{sup_type_tmp}{ver}\.\S+')
    img_id_list = soup.find_all(alt=pattern_img)
    img_dict = {}
    for img_id in img_id_list:
        img_name = img_id.get('alt')
        img_url = img_id.get('src')
        img_dict[img_name] = img_url
    return img_dict

def download_img(url, current_dir):
    if not os.path.exists(os.path.join(os.path.dirname(__file__), f'data/')):
        os.mkdir(os.path.join(os.path.dirname(__file__), f'data/'))
    response = httpx.get(url, timeout=10)
    with open(current_dir, 'wb') as f:
        f.write(response.read())

def generate_img(sup_type):
    img_dict = generate_url(sup_type)
    data_dict = {}
    for img_name in list(img_dict.keys()):
        current_dir = os.path.join(os.path.dirname(__file__), f'data/{img_name}')
        download_img(img_dict[img_name], current_dir)
        img = Image.open(current_dir)
        data_dict[img_name] = {}
        data_dict[img_name]['width'] = img.width
        data_dict[img_name]['height'] = img.height
        data_dict[img_name]['img'] = img
    all_height = 0
    for img_name in list(data_dict.keys()):
        all_height += data_dict[img_name]['height']
        all_width = data_dict[img_name]['width']
    end_img = Image.new('RGB', (all_width, all_height))
    all_height = 0
    for img_name in list(data_dict.keys()):
        img_tmp = data_dict[img_name]['img']
        end_img.paste(img_tmp, (0, all_height))
        all_height += data_dict[img_name]['height']
    return end_img