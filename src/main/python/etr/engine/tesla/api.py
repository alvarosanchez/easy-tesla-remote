import json
import requests

from urllib.parse import urljoin
from .endpoints import SupportedEndpoints


class TeslaApiError(Exception):
    
    def __init__(self, message, status_code=None, full_response=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.full_response = full_response


class TeslaApi():
    """
    Tesla API client

    The token can be set when instancing the class using the constructor
    or later by setting the token attribute
    """

    def __init__(self, token=''):
        self.base_url = 'https://owner-api.teslamotors.com'
        self.user_agent = 'etr'
        self.endpoints = SupportedEndpoints()
        self.client_id = '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
        self.client_secret = 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'
        self.token = token

    def refresh_token(self, refresh_token):
        """
        Get new access and refresh tokens using the refresh token

        See: https://tesla-api.timdorr.com/api-basics/authentication

        :param refresh_token: refresh token for the account
        :return: dictionary containing the API response
        """
        parameters = [
            'refresh_token',
            self.client_id,
            self.client_secret,
            refresh_token
        ]

        return self._send_request(self.endpoints.REFRESH_TOKEN, parameters)

    def get_token(self, email, password):
        """
        Get new access and refresh tokens using the account's email and password

        See: https://tesla-api.timdorr.com/api-basics/authentication

        :param email: email address used to log into Tesla
        :param password: user password for the Tesla site
        :return: dictionary containing the API response
        """
        parameters = [
            'password',
            self.client_id,
            self.client_secret,
            email,
            password
        ]

        return self._send_request(self.endpoints.AUTHENTICATE, parameters)

    def _send_request(self, endpoint, *args):
        if endpoint not in self.endpoints.supported_endpoints:
            raise TeslaApiError(f'Endpoint {endpoint} not supported')

        config = self.endpoints.get_config(endpoint)
        url = urljoin(self.base_url, config['URL'])
        url = url.format(args)

        headers = self._build_headers(config['AUTH'])

        response = None
        if config['METHOD'] == 'GET':
            response = requests.get(url, headers=headers)
        elif config['METHOD'] == 'POST':
            response = requests.post(url, headers=headers)
        else:
            raise TeslaApiError(f"Method {config['METHOD']} not supported")

        self._validate_response(response, config)

        if 'RESULT_KEY' in config:
            return response.json()[config['RESULT_KEY']]
        else:
            return response.json()

    def _build_headers(self, include_token):
        result = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json'
        }
        if include_token:
            result['Authorization'] = f'Bearer {self.token}'
        return result

    def _validate_response(self, response, endpoint):
        if response.status_code != endpoint['VALID_RESULT']:
            message = f'Response status code is {response.status_code} '\
                      f'but expected {expected_code}'
            raise TeslaApiError(message, response.status_code, response)

        if 'RESULT_KEY' in endpoint and endpoint['RESULT_KEY'] not in response.json():
            message = f"Unsupported response. '{endpoint['RESULT_KEY']}' key is missing"
            raise TeslaApiError(message, response.status_code, response)
