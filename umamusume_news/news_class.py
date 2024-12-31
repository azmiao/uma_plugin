import httpx
from bs4 import BeautifulSoup


class NewsClass:
    def __init__(self, server, news_id, news_time, news_url, news_title):
        self.server = server
        self.news_id = news_id
        self.news_time = news_time
        self.news_url = news_url
        self.news_title = news_title
        self.show_url = '▲' + self.news_url
        # 如不需要转短链请注释掉下面这一行 | 暂时只有日服需要吧
        if 'jp' == server:
            self.process_url()

    # 生成短链 | 防止被TX拦截
    def process_url(self):
        header = {'Content-Type': 'application/json'}
        res = httpx.post('https://osdb.link/', json={'url': self.news_url}, headers=header, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        show_url = ('▲[短链]' + soup.find('label', {"id": "surl"}).text
                    .replace('Your shortened URL is:', '').strip())
        self.show_url = show_url
