
import json
import requests
import traceback
import concurrent
from data_tools.utils.bunch import Bunch
from data_tools.utils.logger import Logger
from concurrent.futures import ProcessPoolExecutor
import config as cfg 

class SiteBanChecker(object):
    """
    Check ban site with send lots of fetch request
    """
    def __init__(self,  ) -> None:
        """
        Initialize Kafka producer class
        Args:
            config: Get ban checker config by file path or bunch object
        """
        self._logger = Logger()

    def _get_tor_session(self):
        """
        Create tor session
            - Tor uses the 9050 port as the default socks port
        """
        session = requests.session()
        session.proxies = {
            'http': cfg.PROXY_HTTP,
            'https': cfg.PROXY_HTTPS
        }
        return session


    def _get_data_by_crawl(self):
        """
        Get data from url by tor session
        """
        session = self._get_tor_session()
        params = self._config.params if self._config.params is not None else {}
        payload = self._config.payload if self._config.payload is not None else {}
        headers = dict(self._config.headers)
        response = session.get(url=self._config.url, headers=headers, params=params, data=payload)
        if response.status_code == 200:
            return json.loads(response.text)
        return response

    def _get_data(self):
        """
        Get data until loop break
        """
        count = 0
        while True:
            try:
                names = []
                response = self._get_data_by_crawl()
                if 'data' in response:
                    data = response['data']
                    for symbol in data:
                        names.append(symbol['name'])
                    self._logger.info(f'Current number of execution {count}')
                    count += 1
                else:
                    assert 'data' in response, f'count : {count} \nerror :{response}'
            except Exception as e:
                self._logger.error(str(e))
                break

    def check(self, max_workers: int = 1):
        """
        Check ban based on url
        Args:
            max_workers: Number of worker for running parallel
        Returns: Show log results for checking ban url based on requests
        """
        while True:
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                i = 0
                while i < 300:
                    futures.append(executor.submit(self._get_data()))
                    self._logger.info(f'Current worker number {i}')
                    i += 1
                for future in concurrent.futures.as_completed(futures):
                    try:
                        message = future.result()
                        if message is not None:
                            self._logger.info(msg=str(message))
                    except Exception as e:
                        self._logger.error(msg=str(e))
                        trace_back = traceback.TracebackException.from_exception(e)
                        self._logger.error(msg=''.join(trace_back.format()))
