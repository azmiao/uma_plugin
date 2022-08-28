import os
import httpx
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageColor

from hoshino import R, logger
from ..plugin_utils.base_util import get_img_cq

# 获取育成目标的数据
async def get_tar_data(uma_name):
    url = f'https://wiki.biligame.com/umamusume/{uma_name}'
    res = httpx.get(url, timeout=10)
    soup = BeautifulSoup(res.text, 'lxml')
    target_tmp = soup.find_all('table', {"style":"width:100%;margin:0px"})[-1]
    row_list = target_tmp.find_all('tr')
    data, i = {}, 0
    while (i <= 44 and row_list[i+1].find('td').text.strip()):
        race = row_list[i+3].find('td').text.strip().replace('\t', ' ').replace('&#160;', ' ').replace('\n', ' | ')\
            .replace('\xa0', ' ')
        data[row_list[i].text.strip()] = {
            row_list[i+1].find('th').text.strip(): row_list[i+1].find('td').text.strip(),
            row_list[i+2].find('th').text.strip(): row_list[i+2].find('td').text.strip(),
            row_list[i+3].find('th').text.strip(): race
        }
        i += 4
    return data

# 制作图片
async def generate_img(uma_name):
    data = await get_tar_data(uma_name)
    target_list = list(data.keys())
    end_img = Image.new('RGB', (1800, 136+309*len(target_list)))
    title_img = Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'title.png'))).convert("RGBA")
    target_img = Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'target.png'))).convert("RGBA")
    end_img.paste(title_img, (0, 0))
    all_height = 136
    font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'simhei.ttf')
    font_rgb = ImageColor.getrgb('#8B4513')
    for target in target_list:
        img_font = ImageFont.truetype(font_path, 50, index=0)
        end_img.paste(target_img, (0, all_height))
        draw_img = ImageDraw.Draw(end_img)
        # 调整居中
        img_size = draw_img.multiline_textsize(target, font=img_font)
        start_width = 900 - img_size[0] / 2
        if start_width < 0 : start_width = 15.45
        draw_img.text(xy=(start_width, all_height+15.45), text=target, font=img_font, fill=font_rgb)
        draw_img.text(xy=(135, all_height+92.7), text='时间', font=img_font, fill=font_rgb)
        draw_img.text(xy=(135, all_height+169.95), text='条件', font=img_font, fill=font_rgb)
        draw_img.text(xy=(80, all_height+247.2), text='比赛描述', font=img_font, fill=font_rgb)
        draw_img.text(xy=(380, all_height+92.7), text=data[target]['时间'], font=img_font, fill=font_rgb)
        draw_img.text(xy=(380, all_height+169.95), text=data[target]['条件'], font=img_font, fill=font_rgb)
        if uma_name == '大和赤骥' and target.startswith('目标4'):
            img_font = ImageFont.truetype(font_path, 32, index=0)
        draw_img.text(xy=(380, all_height+247.2), text=data[target]['比赛描述'], font=img_font, fill=font_rgb)
        all_height += 309
    return end_img

# 返回目标图片
async def get_tar(uma_name, is_force):
    if not os.path.exists(os.path.join(R.img('umamusume').path, f'uma_target/')):
        os.mkdir(os.path.join(R.img('umamusume').path, f'uma_target/'))
    img_path = os.path.join(R.img('umamusume').path, f'uma_target/target_{uma_name}.png')
    if not os.path.exists(img_path) or is_force:
        img = await generate_img(uma_name)
        img.save(img_path, 'PNG')
        logger.info(f'{uma_name}的育成目标图片不存在，现已成功生成！')
    logger.info(f'{uma_name}的育成目标图片已存在，即将发送图片！')
    img_ = await get_img_cq(img_path)
    return img_