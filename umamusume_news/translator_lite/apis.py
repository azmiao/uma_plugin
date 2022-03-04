# coding=utf-8
# author=UlionTse

"""MIT License

Copyright (c) 2022 UlionTse

Warning: Prohibition of commercial use!
This module is designed to help students and individuals with translation services.
For commercial use, please purchase API services from translation suppliers.

Don't make high frequency requests!
Enterprises provide free services, we should be grateful instead of making trouble.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. You may obtain a copy of the
License at

    https://github.com/uliontse/translators/blob/master/LICENSE

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import re
import time
import random
import urllib.parse
import hashlib
import functools
import warnings
from typing import Union, Callable

import pathos.multiprocessing
import lxml.etree
import requests

class Tse:
    def __init__(self):
        self.author = 'Ulion.Tse'
    
    @staticmethod
    def time_stat(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            t1 = time.time()
            r = func(*args, **kwargs)
            t2 = time.time()
            return r
        return _wrapper

    @staticmethod
    def get_headers(host_url, if_api=False, if_referer_for_host=True, if_ajax_for_api=True, if_json_for_api=False):
        url_path = urllib.parse.urlparse(host_url).path
        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/55.0.2883.87 Safari/537.36"
        host_headers = {
            'Referer' if if_referer_for_host else 'Host': host_url,
            "User-Agent": user_agent,
        }
        api_headers = {
            'Origin': host_url.split(url_path)[0] if url_path else host_url,
            'Referer': host_url,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": user_agent,
        }
        if if_api and not if_ajax_for_api:
            api_headers.pop('X-Requested-With')
            api_headers.update({'Content-Type': 'text/plain'})
        if if_api and if_json_for_api:
            api_headers.update({'Content-Type': 'application/json'})
        return host_headers if not if_api else api_headers

    @staticmethod
    def check_language(from_language, to_language, language_map, output_zh=None, output_auto='auto'):
        auto_pool = ('auto', 'auto-detect')
        zh_pool = ('zh', 'zh-CN', 'zh-CHS', 'zh-Hans')
        from_language = output_auto if from_language in auto_pool else from_language
        from_language = output_zh if output_zh and from_language in zh_pool else from_language
        to_language = output_zh if output_zh and to_language in zh_pool else to_language
        
        if from_language != output_auto and from_language not in language_map:
            raise TranslatorError('Unsupported from_language[{}] in {}.'.format(from_language, sorted(language_map.keys())))
        elif to_language not in language_map:
            raise TranslatorError('Unsupported to_language[{}] in {}.'.format(to_language, sorted(language_map.keys())))
        elif from_language != output_auto and to_language not in language_map[from_language]:
            raise TranslatorError('Unsupported translation: from [{0}] to [{1}]!'.format(from_language, to_language))
        return from_language, to_language

    @staticmethod
    def make_temp_language_map(from_language, to_language):
        warnings.warn('Did not get a complete language map. And do not use `from_language="auto"`.')
        assert from_language != 'auto' and to_language != 'auto' and from_language != to_language
        lang_list = [from_language, to_language]
        return {}.fromkeys(lang_list, lang_list)

    @staticmethod
    def check_query_text(query_text, if_ignore_limit_of_length=False, limit_of_length=5000):
        if not isinstance(query_text, str):
            raise TranslatorError('query_text is not string.')
        query_text = query_text.strip()
        if not query_text:
            return ''
        length = len(query_text)
        if length > limit_of_length and not if_ignore_limit_of_length:
            raise TranslatorError('The length of the text to be translated exceeds the limit.')
        else:
            if length > limit_of_length:
                warnings.warn(f'The translation ignored the excess[above 5000]. Length of `query_text` is {length}.')
                return query_text[:limit_of_length]
        return query_text

class TranslatorError(Exception):
    pass

class Youdao(Tse):
    def __init__(self):
        super().__init__()
        self.host_url = 'https://fanyi.youdao.com'
        self.api_url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.get_old_sign_url = 'https://shared.ydstatic.com/fanyi/newweb/v1.0.29/scripts/newweb/fanyi.min.js'
        self.get_new_sign_url = None
        self.get_sign_pattern = 'https://shared.ydstatic.com/fanyi/newweb/(.*?)/scripts/newweb/fanyi.min.js'
        self.host_headers = self.get_headers(self.host_url, if_api=False)
        self.api_headers = self.get_headers(self.host_url, if_api=True)
        self.language_map = None
        self.query_count = 0
        self.output_zh = 'zh-CHS'
    
    def get_language_map(self, host_html):
        et = lxml.etree.HTML(host_html)
        lang_list = et.xpath('//*[@id="languageSelect"]/li/@data-value')
        lang_list = [(x.split('2')[0], [x.split('2')[1]]) for x in lang_list if '2' in x]
        lang_map = dict(map(lambda x: x, lang_list))
        lang_map.pop('zh-CHS')
        lang_map.update({'zh-CHS': list(lang_map.keys())})
        return lang_map

    def get_sign_key(self, ss, host_html, timeout, proxies):
        try:
            if not self.get_new_sign_url:
                self.get_new_sign_url = re.compile(self.get_sign_pattern).search(host_html).group(0)
            r = ss.get(self.get_new_sign_url, headers=self.host_headers, timeout=timeout, proxies=proxies)
            r.raise_for_status()
        except:
            r = ss.get(self.get_old_sign_url, headers=self.host_headers, timeout=timeout, proxies=proxies)
            r.raise_for_status()
        sign = re.compile('n.md5\("fanyideskweb"\+e\+i\+"(.*?)"\)').findall(r.text)
        return sign[0] if sign and sign != [''] else "Tbh5E8=q6U3EXe+&L[4c@" #v1.0.31

    def get_form(self, query_text, from_language, to_language, sign_key):
        ts = str(int(time.time()*1000))
        salt = str(ts) + str(random.randrange(0, 10))
        sign_text = ''.join(['fanyideskweb', query_text, salt, sign_key])
        sign = hashlib.md5(sign_text.encode()).hexdigest()
        bv = hashlib.md5(self.api_headers['User-Agent'][8:].encode()).hexdigest()
        form = {
            'i': query_text,
            'from': from_language,
            'to': to_language,
            'lts': ts,                  # r = "" + (new Date).getTime()
            'salt': salt,               # i = r + parseInt(10 * Math.random(), 10)
            'sign': sign,               # n.md5("fanyideskweb" + e + i + "n%A-rKaT5fb[Gy?;N5@Tj"),e=text
            'bv': bv,                   # n.md5(navigator.appVersion)
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_DEFAULT',  # not time.["FY_BY_REALTlME","FY_BY_DEFAULT"]
            # 'typoResult': 'false'
        }
        return form

    # @Tse.time_stat
    def youdao_api(self, query_text:str, from_language:str='auto', to_language:str='en', **kwargs) -> Union[str,dict]:
        """
        https://fanyi.youdao.com
        :param query_text: str, must.
        :param from_language: str, default 'auto'.
        :param to_language: str, default 'en'.
        :param **kwargs:
                :param if_ignore_limit_of_length: boolean, default False.
                :param is_detail_result: boolean, default False.
                :param timeout: float, default None.
                :param proxies: dict, default None.
                :param sleep_seconds: float, default `random.random()`.
        :return: str or dict
        """
        is_detail_result = kwargs.get('is_detail_result', False)
        timeout = kwargs.get('timeout', None)
        proxies = kwargs.get('proxies', None)
        sleep_seconds = kwargs.get('sleep_seconds', random.random())
        if_ignore_limit_of_length = kwargs.get('if_ignore_limit_of_length', False)
        query_text = self.check_query_text(query_text, if_ignore_limit_of_length)

        with requests.Session() as ss:
            host_html = ss.get(self.host_url, headers=self.host_headers, timeout=timeout, proxies=proxies).text
            if not self.language_map:
                 self.language_map = self.get_language_map(host_html)
            sign_key = self.get_sign_key(ss, host_html, timeout, proxies)
            from_language, to_language = self.check_language(from_language, to_language, self.language_map,output_zh=self.output_zh)
            from_language, to_language = ('auto', 'auto') if from_language == 'auto' else (from_language, to_language)

            form = self.get_form(query_text, from_language, to_language, sign_key)
            r = ss.post(self.api_url, data=form, headers=self.api_headers, timeout=timeout, proxies=proxies)
            r.raise_for_status()
            data = r.json()
            if data['errorCode'] == 40:
                raise TranslatorError('Invalid translation of `from_language[auto]`, '
                                'please specify parameters of `from_language` or `to_language`.')
        time.sleep(sleep_seconds)
        self.query_count += 1
        return data if is_detail_result else ' '.join(item['tgt'] if item['tgt'] else '\n' for result in data['translateResult'] for item in result)

_youdao = Youdao()
youdao = _youdao.youdao_api

@Tse.time_stat
def translate_html(html_text:str, to_language:str='en', translator:Callable='auto', n_jobs:int=-1, **kwargs) -> str:
    """
    Translate the displayed content of html without changing the html structure.
    :param html_text: str, html format.
    :param to_language: str, default: 'en'.
    :param translator: translator, default 'auto', means ts.bing
    :param n_jobs: int, default -1, means os.cpu_cnt().
    :param **kwargs:
        :param if_ignore_limit_of_length: boolean, default False.
        :param timeout: float, default None.
        :param proxies: dict, default None.
    :return: str, html format.
    """
    if kwargs:
        for param in ('query_text', 'to_language', 'is_detail_result'):
            assert param not in kwargs, f'{param} should not be in `**kwargs`.'
    kwargs.update({'sleep_seconds': 0})

    n_jobs = os.cpu_count() if n_jobs <= 0 else n_jobs

    pattern = re.compile(r"(?:^|(?<=>))([\s\S]*?)(?:(?=<)|$)") #TODO: <code></code> <div class="codetext notranslate">
    sentence_list = set(pattern.findall(html_text))
    _map_translate_func = lambda sentence: (sentence,translator(query_text=sentence, to_language=to_language, **kwargs))
    result_list = pathos.multiprocessing.ProcessPool(n_jobs).map(_map_translate_func, sentence_list)
    result_dict = {text: ts_text for text,ts_text in result_list}
    _get_result_func = lambda k: result_dict.get(k.group(1), '')
    return pattern.sub(repl=_get_result_func, string=html_text)