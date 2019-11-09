import requests
from pprint import pprint
from json import JSONDecodeError
import logging

feed_logger = logging.getLogger(__name__)


class FeedRequest:
    url = "https://frontend.vh.yandex.ru/v23/feed.json"

    headers = {
        'Origin': "https://yandex.ru",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                      " (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
    }

    query_params = {
        "filter": "carousels",
        "delete_filtered": "0",
        "synchronous_scheme": "1",
        "locale": "ru",
        "from": "efir",
        "service": "ya-main",
        "disable_trackings": "1"}

    @classmethod
    def get_response(cls, tag, offset, limit, num_docs):

        params = cls.query_params.copy()
        params.update({"offset": f"{offset}",
                       "num_docs": f"{num_docs}",
                       "limit": f"{limit}"})

        if tag:
            params["tag"] = tag

        response = requests.request("GET", cls.url, headers=cls.headers, params=params)
        return FeedData(response)


class FeedData:
    def __init__(self, response):
        self.response = response
        self.documents = dict()

    def _extract_documents_from_response(self):
        try:
            data = self.response.json()
        except JSONDecodeError as e:
            feed_logger.debug(type(e), ',', e)
            return {}

        for carousel in data['items']:
            for document in carousel['includes']:
                try:
                    content_id = document['content_id']
                except KeyError as e:
                    feed_logger.debug(type(e), ',', e)
                    continue

                self.documents[content_id] = document

        return self.documents

    def get_documents(self):
        if self.documents:
            return self.documents

        return self._extract_documents_from_response()


if __name__ == '__main__':
    fr = FeedRequest()
    result = fr.get_response(tag='', offset=0, limit=1, num_docs=2)
    pprint(result.get_documents())
