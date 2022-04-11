import random
import shutil
import time
from pathlib import Path

import requests

import config as cfg
from data_tools.utils.bunch import Bunch
from data_tools.utils.logger import Logger


class ProxyRequest:
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    ]

    def __init__(self,  ) -> None:
        """
        Initialize Kafka producer class
        Args:
            config: Get kafka config by file path or bunch object
        """
        self._producer = None
        self.log = Logger()
        self._proxies = {'https': cfg.PROXY_HTTPS,
                         'http': cfg.PROXY_HTTP}
        self.session = requests.session()
        self.session.proxies = self._proxies
        self.user_agent = self.random_user_agent()

    def get_request(self, url, params=None, headers=None):
        if headers is None:
            headers = {}
        headers['User-Agent'] = self.random_user_agent()
        if params is None:
            params = {}
        counter = 0
        while True:
            try:
                res = self.session.get(url, params=params, headers=headers, timeout=10, verify=False)
                # res = requests.get(url, params=params, headers=headers, proxies=self.proxies)
                return res
            except Exception as e:
                try:
                    counter += 1
                    if counter > 3:
                        raise ValueError
                    self.log.error(msg=f'try_count:{counter} , message: {e}')
                    time.sleep(3)
                    self.change_session()
                except:
                    self.log.error(msg='reject after 3 tries')
                    break

    def post_request(self, url, params=None, headers=None, data=None):
        if headers is None:
            headers = {}
        headers['User-Agent'] = self.random_user_agent()
        if params is None:
            params = {}
        res = self.session.post(url, params=params,
                                headers=headers,
                                data=data)
        return res

    def random_user_agent(self):
        return random.choice(self.user_agent_list)

    def change_session(self):
        self.session = requests.session()
        self.session.proxies = self._proxies

    def image_download(self, image_link: str = None, save: bool = True, image_path: str = None):
        Path(f"{cfg.root_path}/images").mkdir(parents=True, exist_ok=True)
        if save and image_path:
            res = self.session.get(image_link, stream=True)
            if res.status_code == 200:
                res.raw.decode_content = True
                with open(image_path, 'wb') as f:
                    shutil.copyfileobj(res.raw, f)
                self.log.info(msg=f'image downloaded at {image_path}')
        else:
            self.log.error(msg='image download failed')
