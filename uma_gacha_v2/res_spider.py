import httpx
import json
import os
from bs4 import BeautifulSoup

from hoshino import R, logger

gacha_path = os.path.join(R.img('umamusume').path, 'uma_gacha')

# 下载图片资源
async def download_img(res_type_f, filename, img_url):
    img_path = os.path.join(gacha_path, res_type_f)
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    current_dir = os.path.join(img_path, filename)
    if not os.path.exists(current_dir):
        try:
            response = httpx.get(img_url, timeout=10)
            with open(current_dir, 'wb') as f:
                f.write(response.read())
            logger.info(f'未检测到马娘抽卡图片 {filename} ，现已下载成功')
        except Exception as e:
            logger.info(f'下载马娘抽卡图片 {filename} 时出现异常：{e}')

# 获取资源数据
async def get_res():
    res_data = {}
    for res_type in ['赛马娘', '支援卡']:
        res_type_f = 'uma_res' if res_type == '赛马娘' else 'chart_res'
        res_data[res_type_f] = {}
        pool_url = f'https://wiki.biligame.com/umamusume/{res_type}一览'
        res = httpx.get(pool_url, timeout=15)
        soup = BeautifulSoup(res.text, 'lxml')
        span_list = soup.find_all('span', {'class': 'popup'})
        for span in span_list:
            title = span.find('a').get('title')
            filename = span.find('img').get('alt').replace(' ', '_')
            img_url = span.find('img').get('src').replace('thumb/', '').replace('/100px-' + filename, '')
            res_data[res_type_f][title] = {
                'filename': filename,
                'img_url': img_url
            }
            await download_img(res_type_f, filename, img_url)
    with open(os.path.join(gacha_path, 'uma_res.json'), 'w', encoding='utf-8') as f:
        json.dump(res_data, f, ensure_ascii=False, indent=4)
