from PIL import Image, ImageDraw, ImageFont, ImageColor
import httpx
import os
from .adaptability import get_adaptability
from hoshino import R

async def get_detail(uma_name, f_data):
    im = Image.open(os.path.join(R.img('umamusume').path, f'uma_bir/{uma_name}.png'))
    current_dir = os.path.join(R.img('umamusume').path, f'uma_bir/uniform/{uma_name}_uniform.png')
    uniform = str(f_data[uma_name]['uniform_img'])
    if not os.path.exists(os.path.join(R.img('umamusume').path, f'uma_bir/uniform/')):
        os.mkdir(os.path.join(R.img('umamusume').path, f'uma_bir/uniform/'))
    if not os.path.exists(current_dir):
        await download_img(uniform, current_dir)
    uniform_img = Image.open(current_dir).convert("RGBA")
    uniform_img = uniform_img.resize((525, 924))
    im.paste(uniform_img, (70, -110), mask=uniform_img)
    
    img_tmp = await get_adaptability(uma_name, f_data)
    if img_tmp:
        adaptability_img = img_tmp.convert("RGBA")
        adaptability_img = adaptability_img.resize((600, 200))
        im.paste(adaptability_img, (25, 620), mask=adaptability_img)
    
    im = await add_text(im, uma_name, f_data)
    # im.show()
    return im

async def download_img(uniform, current_dir):
    response = httpx.get(uniform, timeout=10)
    with open(current_dir, 'wb') as f:
        f.write(response.read())

async def add_text(im, uma_name, f_data):
    cn_name = f_data[uma_name]['cn_name'] if f_data[uma_name]['cn_name'] else f_data[uma_name]['jp_name']
    font_path = os.path.join(os.path.dirname(__file__), f'simhei.ttf')
    img_font = ImageFont.truetype(font_path, 25, index=0) # 这个字体好像不带粗体，算了
    font_rgb = ImageColor.getrgb('#8B4513')
    im_draw = ImageDraw.Draw(im)
    im_draw.text(xy=(35, 35), text=str(cn_name), font=img_font, fill=font_rgb)
    return im