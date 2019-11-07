import json
from unittest.mock import patch
from flask import url_for, current_app

from trends.clients.google import get_trends
from trends.clients.prefs import cache


@patch('trends.handlers.trends.get_trends_cached')
def test_get_trends_mock_cache_good(mock_get, client, trends_json):
    mock_get.return_value = trends_json
    resp = client.get(url_for('trends.import_trends'))
    assert resp.status_code == 200
    assert json.loads(resp.data) == json.loads(trends_json)


@patch('trends.handlers.trends.get_trends_cached')
def test_get_trends_mock_cache_bad(mock_get, client):
    mock_get.return_value = None
    resp = client.get(url_for('trends.import_trends'))
    assert resp.status_code == 400


def test_get_trends_using_cache_good(client, trends_json):
    cache.init_app(current_app)
    with current_app.app_context():
        cache.set('trends', trends_json)
    resp = client.get(url_for('trends.import_trends'))
    assert resp.status_code == 200
    assert json.loads(resp.data) == json.loads(trends_json)


def test_get_trends_using_cache_bad(client):
    resp = client.get(url_for('trends.import_trends'))
    assert resp.status_code == 400


@patch('trends.clients.google.make_json_response')
def test_get_trends_from_google(mock_google_response, client, trends_json):
    cache.init_app(current_app)
    mock_google_response.return_value = trends_json
    get_trends(cache_=cache)
    cached_json = cache.get('trends')
    assert cached_json == trends_json






