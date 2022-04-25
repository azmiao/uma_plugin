from PIL import Image
import os

# 获取适应性图片
async def get_adaptability(uma_name, f_data):
    grass = str(f_data[uma_name]['grass'])
    mud = str(f_data[uma_name]['mud'])
    short = str(f_data[uma_name]['short'])
    mile = str(f_data[uma_name]['mile'])
    middle = str(f_data[uma_name]['middle'])
    long = str(f_data[uma_name]['long'])
    run_away = str(f_data[uma_name]['run_away'])
    first = str(f_data[uma_name]['first'])
    center = str(f_data[uma_name]['center'])
    chase = str(f_data[uma_name]['chase'])
    if not grass:
        return False
    img = await generate_img(grass, mud, short, mile, middle, long, run_away, first, center, chase)
    return img

# 合成图片
async def generate_img(grass, mud, short, mile, middle, long, run_away, first, center, chase):
    img_path = os.path.join(os.path.dirname(__file__), 'img_raw/adaptability.png')
    grass_path = os.path.join(os.path.dirname(__file__), f'img_raw/{grass}.png')
    mud_path = os.path.join(os.path.dirname(__file__), f'img_raw/{mud}.png')
    short_path = os.path.join(os.path.dirname(__file__), f'img_raw/{short}.png')
    mile_path = os.path.join(os.path.dirname(__file__), f'img_raw/{mile}.png')
    middle_path = os.path.join(os.path.dirname(__file__), f'img_raw/{middle}.png')
    long_path = os.path.join(os.path.dirname(__file__), f'img_raw/{long}.png')
    run_away_path = os.path.join(os.path.dirname(__file__), f'img_raw/{run_away}.png')
    first_path = os.path.join(os.path.dirname(__file__), f'img_raw/{first}.png')
    center_path = os.path.join(os.path.dirname(__file__), f'img_raw/{center}.png')
    chase_path = os.path.join(os.path.dirname(__file__), f'img_raw/{chase}.png')
    im = Image.open(img_path)
    grass_img = Image.open(grass_path).convert("RGBA") 
    mud_img = Image.open(mud_path).convert("RGBA") 
    short_img = Image.open(short_path).convert("RGBA") 
    mile_img = Image.open(mile_path).convert("RGBA") 
    middle_img = Image.open(middle_path).convert("RGBA") 
    long_img = Image.open(long_path).convert("RGBA") 
    run_away_img = Image.open(run_away_path).convert("RGBA") 
    first_img = Image.open(first_path).convert("RGBA") 
    center_img = Image.open(center_path).convert("RGBA") 
    chase_img = Image.open(chase_path).convert("RGBA") 
    im.paste(grass_img, (298, 98), mask=grass_img)# 草地
    im.paste(mud_img, (466, 98), mask=mud_img)# 泥地
    im.paste(short_img, (298, 159), mask=short_img)# 短距离
    im.paste(mile_img, (466, 159), mask=mile_img)# 英里
    im.paste(middle_img, (634, 159), mask=middle_img)# 中距离
    im.paste(long_img, (802, 159), mask=long_img)# 长距离
    im.paste(run_away_img, (298, 220), mask=run_away_img)# 逃马
    im.paste(first_img, (466, 220), mask=first_img)# 先行
    im.paste(center_img, (634, 220), mask=center_img)# 差马
    im.paste(chase_img, (802, 220), mask=chase_img)# 追马
    # im.show()
    return im