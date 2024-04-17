from typing import Dict, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageColor
from hoshino import R

from .adaptability import get_adaptability
from .detail_class import Uma
from ..plugin_utils.base_util import *

dir_name = os.path.dirname(__file__)


# 生成详细图片
async def get_detail(en_name: str, f_data: Dict[str, Uma]):
    uma = f_data.get(en_name, None)
    # 看板图片URL
    top_url = uma.top_thumb.url
    # 主题色
    color_main = uma.color_main
    color_sub = uma.color_sub

    # 背景&框架
    background = Image.open(os.path.join(dir_name, 'img_raw', 'background.png'))
    framework_1 = Image.open(os.path.join(dir_name, 'img_raw', 'framework_1.png'))
    framework_2 = Image.open(os.path.join(dir_name, 'img_raw', 'framework_2.png'))
    real_framework_1 = await fill_color(framework_1, color_main)
    real_framework_2 = await fill_color(framework_2, color_sub)
    background.paste(real_framework_1, (0, 0), mask=real_framework_1)
    background.paste(real_framework_2, (0, 0), mask=real_framework_2)

    # 角色看板图片就放在额外数据里
    top_path = os.path.join(R.img('umamusume').path, 'extra_data', 'top_thumb')
    # 创建文件夹
    if not os.path.exists(top_path):
        os.mkdir(top_path)
    # 图片路径
    top_thumb_path = os.path.join(top_path, f'{en_name}_top_thumb.png')
    # 图片不存在就下载
    if not os.path.exists(top_thumb_path):
        await download_file(top_url, top_path, f'{en_name}_uniform.png')

    # 贴上看板图片
    top_thumb = Image.open(top_thumb_path).convert("RGBA")
    top_thumb = top_thumb.resize((525, 924))
    background.paste(top_thumb, (70, -110), mask=top_thumb)

    # 贴上适应性图片
    adapt_image = await get_adaptability(en_name, f_data)
    if adapt_image:
        adaptability_img = adapt_image.convert("RGBA")
        adaptability_img = adaptability_img.resize((600, 200))
        background.paste(adaptability_img, (25, 620), mask=adaptability_img)

    # 补上文字
    await add_text(background, uma.name, (35, 35), 30)
    await add_text(background, uma.en, (35, 70), 15)
    await add_text(background, uma.cn_name, (35, 90), 25)
    await add_text(background, f'CV: {uma.cv}', (30, 120), 25)
    await add_text(background, f'生日: {uma.birthday}', (30, 150), 25)
    await add_text(background, f'身高: {uma.height}', (30, 180), 25)
    await add_text(background, f'体重: {uma.weight}', (30, 210), 25)
    await add_text(background, f'三围: {uma.size}', (30, 240), 25)

    # background.show()
    return background


# 撰写文字
async def add_text(image: Image, text: str, xy: Tuple[int, int], size: int):
    font_path = os.path.join(os.path.dirname(dir_name), f'simhei.ttf')
    img_font = ImageFont.truetype(font_path, size, index=0)
    font_rgb = ImageColor.getrgb('#8B4513')
    im_draw = ImageDraw.Draw(image)
    im_draw.text(xy=xy, text=text, font=img_font, fill=font_rgb)


async def fill_color(image: Image, hex_color: str) -> Image:
    # 十六进制值颜色转RGB
    rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    # 获取图像的透明通道信息
    alpha = image.split()[3]
    image = image.point(lambda p: rgb_color if p > 128 else p)
    # 将透明通道信息重新添加到图像中
    r, g, b = image.split()[:3]
    return Image.merge("RGBA", (r, g, b, alpha))
