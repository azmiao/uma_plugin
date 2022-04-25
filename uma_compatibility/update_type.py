import httpx
import os
from bs4 import BeautifulSoup

async def update():
    url = 'https://wiki.biligame.com/umamusume/相性计算器计算方法'
    res = httpx.get(url, timeout=15)
    soup = BeautifulSoup(res, 'lxml')
    type_text = soup.find('div', {'id': 'relation'}).text
    current_dir = os.path.join(os.path.dirname(__file__), 'relation_type.json')
    with open(current_dir, 'w', encoding='UTF-8') as f:
        f.write(type_text.strip())