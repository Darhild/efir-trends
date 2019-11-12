import logging

import requests

from trends.collectors.base import BaseCollector

REQUEST_INTERVAL = 1
REQUEST_JITTER = 1


class GoogleCollector(BaseCollector):
    def __init__(self, repo, url):
        logging.info("google collector link {0} interval {1} jitter {2}".
                     format(url, REQUEST_INTERVAL, REQUEST_JITTER))
        super().__init__(repo, REQUEST_INTERVAL, REQUEST_JITTER)
        self.source_link = url

    def collect(self):
        logging.info("google collect")
        try:
            response = requests.get(self.source_link)
            print("google collect response {0}".format(response.content))
            return self.insert_trend(response.content)
        except Exception as e:
            logging.error("failed to collect google {0}".format(str(e)))
