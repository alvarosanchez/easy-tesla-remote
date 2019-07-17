"""
Tests for etr.engine.tesla.api
"""
import json
import pytest
import requests_mock
from urllib.parse import urljoin
from etr.engine.tesla.api import(
    TeslaApiError,
    TeslaApi,
)
from etr.engine.tesla.endpoints import SupportedEndpoints


@pytest.fixture
def tesla_api():
    api = TeslaApi('auth_token')
    api.base_url = 'https://etr-test.test/'
    return api


@pytest.fixture
def basic_headers(tesla_api):
    return  {
        'User-Agent': tesla_api.user_agent,
        'Accept': 'application/json',
    }


@pytest.fixture
def authorization_headers(tesla_api, basic_headers):
    basic_headers['Authorization'] = f'Bearer {tesla_api.token}'
    return basic_headers


def test_send_get_request(tesla_api, authorization_headers):
    with requests_mock.Mocker() as m:
        endpoint_cfg = SupportedEndpoints.get_config(SupportedEndpoints.VEHICLE_LIST)
        url = urljoin(tesla_api.base_url, endpoint_cfg['URL'])

        m.get(
            url,
            request_headers=authorization_headers,
            text='{"response": {"a": "1"}}',
            status_code=200,
        )
        response = tesla_api.send_request(SupportedEndpoints.VEHICLE_LIST)

        assert response == { 'a': '1' }


def test_send_post_request(tesla_api, authorization_headers):
    with requests_mock.Mocker() as m:
        endpoint_cfg = SupportedEndpoints.get_config(SupportedEndpoints.HONK_HORN)
        url = urljoin(tesla_api.base_url, endpoint_cfg['URL'])
        url = url.format('9999')

        m.post(
            url,
            request_headers=authorization_headers,
            text='{"response": {"a": "1"}}',
            status_code=200,
        )
        response = tesla_api.send_request(SupportedEndpoints.HONK_HORN, '9999')

        assert response == { 'a': '1' }


def test_send_request_raises_wrong_status(tesla_api, authorization_headers):
    with requests_mock.Mocker() as m:
        endpoint_cfg = SupportedEndpoints.get_config(SupportedEndpoints.VEHICLE_LIST)
        url = urljoin(tesla_api.base_url, endpoint_cfg['URL'])

        m.get(
            url,
            request_headers=authorization_headers,
            text='{"response": {"a": "1"}}',
            status_code=404,
        )

        with pytest.raises(TeslaApiError):
            response = tesla_api.send_request(SupportedEndpoints.VEHICLE_LIST)


def test_send_request_unsupported_endpoint(tesla_api, authorization_headers):
    with requests_mock.Mocker() as m:
        endpoint_cfg = SupportedEndpoints.get_config('TIME_OF_USE_SETTINGS')
        url = urljoin(tesla_api.base_url, endpoint_cfg['URL'])

        m.post(
            url,
            request_headers=authorization_headers,
            text='{"response": {"a": "1"}}',
            status_code=200,
        )

        with pytest.raises(TeslaApiError):
            response = tesla_api.send_request('TIME_OF_USE_SETTINGS')


def test_send_request_raises_missing_resp_key(tesla_api, authorization_headers):
    with requests_mock.Mocker() as m:
        endpoint_cfg = SupportedEndpoints.get_config(SupportedEndpoints.VEHICLE_LIST)
        url = urljoin(tesla_api.base_url, endpoint_cfg['URL'])

        m.get(
            url,
            request_headers=authorization_headers,
            text='{"a": "1"}',
            status_code=200,
        )

        with pytest.raises(TeslaApiError):
            response = tesla_api.send_request(SupportedEndpoints.VEHICLE_LIST)


def test_get_token(tesla_api, basic_headers):
    with requests_mock.Mocker() as m:
        endpoint_cfg = SupportedEndpoints.get_config(SupportedEndpoints.AUTHENTICATE)
        url = urljoin(tesla_api.base_url, endpoint_cfg['URL'])
        url = url.format(
            'password',
            tesla_api.client_id,
            tesla_api.client_secret,
            'a@a.com',
            'aaaa'
        )

        m.post(
            url,
            request_headers=basic_headers,
            text='{"a": "1"}',
            status_code=200,
        )
        response = tesla_api.get_token('a@a.com', 'aaaa')

        assert response == { 'a': '1' }


def test_refresh_token(tesla_api, basic_headers):
    with requests_mock.Mocker() as m:
        endpoint_cfg = SupportedEndpoints.get_config(SupportedEndpoints.REFRESH_TOKEN)
        url = urljoin(tesla_api.base_url, endpoint_cfg['URL'])
        url = url.format(
            'refresh_token',
            tesla_api.client_id,
            tesla_api.client_secret,
            'FFFFFFFFFF'
        )

        m.post(
            url,
            request_headers=basic_headers,
            text='{"a": "1"}',
            status_code=200,
        )
        response = tesla_api.refresh_token('FFFFFFFFFF')

        assert response == { 'a': '1' }
