"""
Tests for etr.controllers.util.tesla_api
"""
import json
import pytest
import requests_mock
from etr.engine.tesla.api import(
    TeslaApiError,
    TeslaApi,
)


@pytest.fixture
def tesla_api():
    api = TeslaApi('auth_token')
    api.base_url = 'test://etr-test.test'
    return api


@pytest.fixture
def regular_headers(tesla_api):
    return {
        'User-Agent': tesla_api.user_agent,
        'Accept': 'application/json',
        'Authorization': f'Bearer {tesla_api.token}'
    }


def test_send_get_request(tesla_api, regular_headers):
    with requests_mock.Mocker() as m:
        m.get(
            f'{tesla_api.base_url}/testurl',
            request_headers=regular_headers,
            text='{"response": {"a": "1"}}',
            status_code=200,
        )
        response = tesla_api._send_request(
            f'{tesla_api.base_url}/testurl',
            'GET',
            200
        )

        assert response == { 'a': '1' }


def test_send_post_request(tesla_api, regular_headers):
    with requests_mock.Mocker() as m:
        m.post(
            f'{tesla_api.base_url}/testurl',
            request_headers=regular_headers,
            text='{"response": {"a": "1"}}',
            status_code=200,
        )
        response = tesla_api._send_request(
            f'{tesla_api.base_url}/testurl',
            'POST',
            200
        )

        assert response == { 'a': '1' }


def test_send_request_raises_wrong_status(tesla_api, regular_headers):
    with requests_mock.Mocker() as m:
        m.post(
            f'{tesla_api.base_url}/testurl',
            request_headers=regular_headers,
            text='{"response": {"a": "1"}}',
            status_code=404,
        )

        with pytest.raises(TeslaApiError):
            response = tesla_api._send_request(
                f'{tesla_api.base_url}/testurl',
                'POST',
                200
            )


def test_send_request_raises_missing_resp_key(tesla_api, regular_headers):
    with requests_mock.Mocker() as m:
        m.post(
            f'{tesla_api.base_url}/testurl',
            request_headers=regular_headers,
            text='{"a": "1"}',
            status_code=200,
        )

        with pytest.raises(TeslaApiError):
            response = tesla_api._send_request(
                f'{tesla_api.base_url}/testurl',
                'POST',
                200
            )


def test_get_vehicles(tesla_api, regular_headers):
    with requests_mock.Mocker() as m:
        m.get(
            f'{tesla_api.base_url}/api/1/vehicles/',
            request_headers=regular_headers,
            text='{"response": {"a": "1"}}',
            status_code=200,
        )
        response = tesla_api.get_vehicles()

        assert response == { 'a': '1' }


def test_get_vehicle_data(tesla_api, regular_headers):
    with requests_mock.Mocker() as m:
        m.get(
            f'{tesla_api.base_url}/api/1/vehicles/99999/vehicle_data',
            request_headers=regular_headers,
            text='{"response": {"a": "1"}}',
            status_code=200,
        )
        response = tesla_api.get_vehicle_data(99999)

        assert response == { 'a': '1' }


def test_wake_up(tesla_api, regular_headers):
    with requests_mock.Mocker() as m:
        m.post(
            f'{tesla_api.base_url}/api/1/vehicles/99999/wake_up',
            request_headers=regular_headers,
            text='{"response": {"a": "1"}}',
            status_code=200,
        )
        response = tesla_api.wake_up(99999)

        assert response == { 'a': '1' }


def test_honk(tesla_api, regular_headers):
    with requests_mock.Mocker() as m:
        m.post(
            f'{tesla_api.base_url}/api/1/vehicles/99999/command/honk_horn',
            request_headers=regular_headers,
            text='{"response": {"a": "1"}}',
            status_code=200,
        )
        response = tesla_api.honk(99999)

        assert response == { 'a': '1' }


def test_flash_lights(tesla_api, regular_headers):
    with requests_mock.Mocker() as m:
        m.post(
            f'{tesla_api.base_url}/api/1/vehicles/99999/command/flash_lights',
            request_headers=regular_headers,
            text='{"response": {"a": "1"}}',
            status_code=200,
        )
        response = tesla_api.flash_lights(99999)

        assert response == { 'a': '1' }


# get and refresh token


def test_get_token(tesla_api):
    # def parameter_matcher(request):
    #     # for var in vars(request._request):
    #     #     print(var)
    #     # print(', '.join("%s: %s" % item for item in vars(request._url_parts).items()))
    #     print(request._url_parts)
    #     return False
    #     # return len(request.headers) != 0

    with requests_mock.Mocker() as m:
        m.post(
            f'{tesla_api.base_url}/oauth/token',
            request_headers={
                'User-Agent': tesla_api.user_agent,
                'Accept': 'application/json'
            },
            # additional_matcher=parameter_matcher,
            text='{"a": "1"}',
            status_code=200,
        )
        response = tesla_api.get_token('user_name', 'user_password')

        assert response == { 'a': '1' }
