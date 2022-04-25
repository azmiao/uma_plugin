from PIL import Image, ImageDraw, ImageFont, ImageColor
import httpx
import os

from .adaptability import get_adaptability
from hoshino import R

# 生成详细图片
async def get_detail(uma_name, f_data):
    im = Image.open(os.path.join(R.img('umamusume').path, f'base_data/background_data/{uma_name}.png'))
    # 制服图片就放在额外数据里
    current_dir = os.path.join(R.img('umamusume').path, f'extra_data/uma_uniform/{uma_name}_uniform.png')
    uniform = str(f_data[uma_name]['uniform_img'])
    # 创建文件夹
    if not os.path.exists(os.path.join(R.img('umamusume').path, f'extra_data/')):
        os.mkdir(os.path.join(R.img('umamusume').path, f'extra_data/'))
    if not os.path.exists(os.path.join(R.img('umamusume').path, f'extra_data/uma_uniform/')):
        os.mkdir(os.path.join(R.img('umamusume').path, f'extra_data/uma_uniform/'))
    # 图片不存在就下载
    if not os.path.exists(current_dir):
        await download_img(uniform, current_dir)
    # 合成图片
    uniform_img = Image.open(current_dir).convert("RGBA")
    uniform_img = uniform_img.resize((525, 924))
    im.paste(uniform_img, (70, -110), mask=uniform_img)
    # 获取适应性图片
    img_tmp = await get_adaptability(uma_name, f_data)
    if img_tmp:
        adaptability_img = img_tmp.convert("RGBA")
        adaptability_img = adaptability_img.resize((600, 200))
        im.paste(adaptability_img, (25, 620), mask=adaptability_img)
    # 增加详细查询的名字
    im = await add_text(im, uma_name, f_data)
    # im.show()
    return im

# 下载制服图片
async def download_img(uniform, current_dir):
    response = httpx.get(uniform, timeout=10)
    with open(current_dir, 'wb') as f:
        f.write(response.read())

# 撰写文字
async def add_text(im, uma_name, f_data):
    cn_name = f_data[uma_name]['cn_name'] if f_data[uma_name]['cn_name'] else f_data[uma_name]['jp_name']
    font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'simhei.ttf')
    img_font = ImageFont.truetype(font_path, 25, index=0) # 这个字体好像不带粗体，算了
    font_rgb = ImageColor.getrgb('#8B4513')
    im_draw = ImageDraw.Draw(im)
    im_draw.text(xy=(35, 35), text=str(cn_name), font=img_font, fill=font_rgb)
    return im