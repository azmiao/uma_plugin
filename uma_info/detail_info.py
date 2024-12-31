from typing import Dict, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageColor

from yuiChyan import base_res_path, font_path
from .adaptability import get_adaptability
from .detail_class import Uma, uma_from_dict
from ..plugin_utils.base_util import *

dir_name = os.path.dirname(__file__)


# 生成详细图片
async def get_detail(en_name: str, f_data: Dict[str, Uma]):
    uma_raw = f_data.get(en_name, None)
    # 没有找到
    if not uma_raw:
        raise UmaNotFoundException(f'Uma not found: [{en_name}]')

    uma = uma_from_dict(uma_raw)
    # 看板图片URL
    visual_list = uma.visual
    image_dict = {visual.name.title: visual.image for visual in visual_list if visual.name.title}
    uniform_img = image_dict.get('制服', None)

    # 主题色
    color_main = uma.color_main
    color_sub = uma.color_sub

    # 背景&框架
    background = Image.open(os.path.join(dir_name, 'img_raw', 'background.png')).convert('RGBA')
    framework_1 = Image.open(os.path.join(dir_name, 'img_raw', 'framework_1.png')).convert('RGBA')
    framework_2 = Image.open(os.path.join(dir_name, 'img_raw', 'framework_2.png')).convert('RGBA')
    real_framework_1 = await fill_color(framework_1, color_main)
    real_framework_2 = await fill_color(framework_2, color_sub)
    background.paste(real_framework_1, (0, 0), mask=real_framework_1)
    background.paste(real_framework_2, (0, 0), mask=real_framework_2)

    # 角色看板图片就放在额外数据里
    if uniform_img.url:
        top_path = os.path.join(os.path.join(base_res_path, 'umamusume'), 'extra_data', 'top_thumb')
        # 创建文件夹
        if not os.path.exists(top_path):
            os.mkdir(top_path)
        # 图片路径
        top_thumb_path = os.path.join(top_path, f'{en_name}_top_thumb.png')
        # 图片不存在就下载
        if not os.path.exists(top_thumb_path):
            await download_file(uniform_img.url, top_path, f'{en_name}_top_thumb.png')

        # 贴上看板图片
        top_thumb = Image.open(top_thumb_path).convert('RGBA')
        top_thumb = top_thumb.resize((uniform_img.width * 900 // uniform_img.height, 900))
        background.paste(top_thumb, (70, -110), mask=top_thumb)

    # 贴上适应性图片
    adapt_image = await get_adaptability(en_name, f_data)
    if adapt_image:
        adaptability_img = adapt_image.convert('RGBA')
        adaptability_img = adaptability_img.resize((600, 200))
        background.paste(adaptability_img, (25, 620), mask=adaptability_img)

    # 补上文字
    await add_text(background, uma.name, (700, 100), 50)
    await add_text(background, uma.en, (700, 200), 30)
    await add_text(background, uma.cn_name, (700, 270), 30)
    await add_text(background, f'CV: {uma.cv}', (700, 350), 30)
    await add_text(background, f'生日: {uma.birthday}', (700, 430), 30)
    await add_text(background, f'身高: {uma.height}', (700, 510), 30)
    await add_text(background, f'体重: {uma.weight}', (700, 590), 30)
    await add_text(background, f'三围: {uma.size}', (700, 670), 30)

    # background.show()
    return background


# 撰写文字
async def add_text(image: Image, text: str, xy: Tuple[int, int], size: int):
    img_font = ImageFont.truetype(font_path, size, index=0)
    font_rgb = ImageColor.getrgb('#8B4513')
    im_draw = ImageDraw.Draw(image)
    im_draw.text(xy=xy, text=text, font=img_font, fill=font_rgb)


async def fill_color(image: Image, hex_color: str) -> Image:
    # 十六进制值颜色转RGB
    rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    # 获取图像的透明通道信息
    r, g, b, a = image.split()
    # 使用 point 方法将颜色应用到RGB三个通道上
    r = r.point(lambda p: rgb_color[0] if p > 128 else p)
    g = g.point(lambda p: rgb_color[1] if p > 128 else p)
    b = b.point(lambda p: rgb_color[2] if p > 128 else p)
    return Image.merge("RGBA", (r, g, b, a))
