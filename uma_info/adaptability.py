from typing import Dict, Tuple

from PIL import Image

from .detail_class import Uma
from ..plugin_utils.base_util import *

dir_name = os.path.dirname(__file__)


# 获取适应性图片
async def get_adaptability(en_name: str, f_data: Dict[str, Uma]) -> Image:
    uma = f_data.get(en_name, None)
    # 没有找到
    if not uma:
        raise UmaNotFoundException(f'Uma not found: [{en_name}]')

    adapt = uma.adapt
    # 没有适应性
    if not adapt:
        return False

    img: Image
    img = await generate_img(
        adapt.grass,
        adapt.mud,
        adapt.short,
        adapt.mile,
        adapt.middle,
        adapt.long,
        adapt.run_away,
        adapt.first,
        adapt.center,
        adapt.chase,
    )
    # img.show()
    return img


# 合成图片
async def generate_img(grass: str, mud: str, short: str, mile: str, middle: str, long: str, run_away: str,
                       first: str, center: str, chase: str) -> Image:
    # 底层
    img_path = os.path.join(dir_name, 'img_raw/adaptability.png')
    im = Image.open(img_path)
    await paste_img(im, await get_icon_image(grass), (298, 98))
    await paste_img(im, await get_icon_image(mud), (466, 98))
    await paste_img(im, await get_icon_image(short), (298, 159))
    await paste_img(im, await get_icon_image(mile), (466, 159))
    await paste_img(im, await get_icon_image(middle), (634, 159))
    await paste_img(im, await get_icon_image(long), (802, 159))
    await paste_img(im, await get_icon_image(run_away), (298, 220))
    await paste_img(im, await get_icon_image(first), (466, 220))
    await paste_img(im, await get_icon_image(center), (634, 220))
    await paste_img(im, await get_icon_image(chase), (802, 220))
    return im


async def get_icon_image(icon_type: str) -> Image:
    icon_path = os.path.join(dir_name, f'img_raw/{icon_type}.png')
    return Image.open(icon_path).convert("RGBA")


async def paste_img(base_image: Image, icon_image: Image, box: Tuple[int, int]):
    base_image.paste(icon_image, box, mask=icon_image)
