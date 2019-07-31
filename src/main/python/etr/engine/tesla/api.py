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
    Tesla API client.

    The token can be set when instancing the class using the constructor
    or later by setting the token attribute.

    For Tesla Api details see: https://tesla-api.timdorr.com/.
    """

    def __init__(self, token=''):
        self.base_url = 'https://owner-api.teslamotors.com'
        self.user_agent = 'etr'
        self.urls = SupportedEndpoints
        self.client_id = '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
        self.client_secret = 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'
        self.token = token

    def _build_headers(self, include_token):
        """
        Build the headers for a request.

        Args:
            - include_token (bool): Sets whether the authorization token will be
                included or not in the header.
        
        Returns:
            dict containing the headers for an API request.
        """
        result = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json'
        }
        if include_token:
            result['Authorization'] = f'Bearer {self.token}'
        return result

    def _validate_response(self, response, endpoint):
        """
        Validate an api response.

        Args:
            - response (requests response): api raw response.
            - endpoint (dict): dictionary containing the endpoint details.

        Raises:
            - TeslaApiError: if the response status code is not the expected
                one or if the RESULT_KEY is required and missing from the 
                response.
        """
        if response.status_code != endpoint['VALID_RESULT']:
            message = f'Response status code is {response.status_code} '\
                      f'but expected {endpoint["VALID_RESULT"]}'
            raise TeslaApiError(message, response.status_code, response)

        if 'RESULT_KEY' in endpoint and endpoint['RESULT_KEY'] not in response.json():
            message = f"Unsupported response. '{endpoint['RESULT_KEY']}' key is missing"
            raise TeslaApiError(message, response.status_code, response)

    def refresh_token(self, refresh_token):
        """
        Get new access and refresh tokens using the refresh token.

        Args:
            - refresh_token (str): refresh token for the account.
        
        Returns:
            dictionary containing the API response.
        """
        return self.send_request(
            self.urls.REFRESH_TOKEN,
            'refresh_token',
            self.client_id,
            self.client_secret,
            refresh_token)

    def get_token(self, email, password):
        """
        Get new access and refresh tokens using the account's email and
        password.

        Args:
            - email (str): email address used to log into Tesla.
            - password (str): user password for the Tesla site.

        Returns: 
            dictionary containing the API response.
        """
        return self.send_request(
            self.urls.AUTHENTICATE,
            'password',
            self.client_id,
            self.client_secret,
            email,
            password)

    def send_request(self, endpoint, *args):
        """
        Send a request to Tesla's API.

        Args:
            - endpoint: Name of the endpoint, this class urls attribute
                contains a list of accepted values.
        
        *Args:
            arguments required by the endpoint, usually they require only
            the car id. To check the required parameters of a particular
            endpoint check endpoints.py.
        """
        if endpoint not in self.urls.supported_endpoints:
            raise TeslaApiError(f'Endpoint {endpoint} not supported')

        config = self.urls.get_config(endpoint)
        url = urljoin(self.base_url, config['URL'])
        url = url.format(*args)

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
