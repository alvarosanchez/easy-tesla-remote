import json
import requests


class TeslaApiError(Exception):
    
    def __init__(self, message, status_code, full_response):
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
        self.client_id = '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
        self.client_secret = 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'
        self.token = token

    def _build_headers(self):
        return {
            'User-Agent': self.user_agent,
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

    def _validate_response(self, response, expected_code):
        if response.status_code != expected_code:
            message = f'Response status code is {response.status_code} '\
                      f'but expected {expected_code}'
            raise TeslaApiError(message, response.status_code, response)

        if 'response' not in response.json():
            message = f"Unsupported content. 'response' key is missing"
            raise TeslaApiError(message, response.status_code, response)

    def _send_request(self, url, method, expected_code):
        headers = self._build_headers()

        response = None
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers)
        else:
            raise TeslaApiError(f"Unsupported method '{method}'", None, None)

        self._validate_response(response, expected_code)

        return response.json()['response']

    def get_token(self, email, password):
        """
        Get new access and refresh tokens using the account's email and password

        See: https://tesla-api.timdorr.com/api-basics/authentication

        :param email: email address used to log into Tesla
        :param password: user password for the Tesla site
        :return: dictionary containing the API response
        """
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json'
        }

        parameters = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'email': email,
            'password': password
        }

        response = requests.post(f'{self.base_url}/oauth/token',
                                 headers=headers,
                                 params=parameters)

        return response.json()

    def refresh_token(self, refresh_token):
        """
        Get new access and refresh tokens using the refresh token

        See: https://tesla-api.timdorr.com/api-basics/authentication

        :param refresh_token: refresh token for the account
        :return: dictionary containing the API response
        """
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json'
        }

        parameters = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token
        }

        response = requests.post(f'{self.base_url}/oauth/token',
                                 headers=headers,
                                 params=parameters)

        return response.json()

    def get_vehicles(self):
        """
        Get a list of the owned vehicles with some basic information about them
        
        See: https://tesla-api.timdorr.com/api-basics/vehicles
        """
        url = f'{self.base_url}/api/1/vehicles/'
        return self._send_request(url, 'GET', 200)

    def get_vehicle_data(self, id):
        """
        Get all the availabe information about a vehicle
        
        See: https://tesla-api.timdorr.com/vehicle/state/data

        :param id: id of the car (not the vehicle_id)
        """
        url = f'{self.base_url}/api/1/vehicles/{id}/vehicle_data'
        return self._send_request(url, 'GET', 200)

    def wake_up(self, id):
        """
        Try to wake up a car

        See: https://tesla-api.timdorr.com/vehicle/commands/wake

        :param id: id of the car (not the vehicle_id)
        """
        url = f'{self.base_url}/api/1/vehicles/{id}/wake_up'
        return self._send_request(url, 'POST', 200)

    def honk(self, id):
        """
        Try to wake up a car

        See: https://tesla-api.timdorr.com/vehicle/commands/alerts

        :param id: id of the car (not the vehicle_id)
        """
        url = f'{self.base_url}/api/1/vehicles/{id}/command/honk_horn'
        return self._send_request(url, 'POST', 200)

    def flash_lights(self, id):
        """
        Try to flash the car lights

        See: https://tesla-api.timdorr.com/vehicle/commands/alerts

        :param id: id of the car (not the vehicle_id)
        """
        url = f'{self.base_url}/api/1/vehicles/{id}/command/flash_lights'
        return self._send_request(url, 'POST', 200)
