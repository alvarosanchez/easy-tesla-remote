import json
import random
import logging

from .api import TeslaApiError


logger = logging.getLogger(__name__)


class TeslaApiMock():

    token_response = {
        "access_token": "aaaaaaaaaaaaaaaa",
        "token_type": "bearer",
        "expires_in": 3888000,
        "refresh_token": "ffffffffffffff",
        "created_at": 1561913457
    }

    refresh_token_response = {
        "access_token": "bbbbbbbbbbbbbb",
        "token_type": "bearer",
        "expires_in": 3888000,
        "refresh_token": "ccccccccccccccc",
        "created_at": 1561913774
    }

    vehicles_response = [
        {
            "id": 90000000000000001,
            "vehicle_id": 900000001,
            "vin": "5Y000000000000001",
            "display_name": "Vehicle 01",
            "option_codes": "MDL3",
            "color": None,
            "tokens": [
                "aaaaaaaaaaaaaaa1",
                "bbbbbbbbbbbbbbb1"
            ],
            "state": "online",
            "in_service": False,
            "id_s": "90000000000000001",
            "calendar_enabled": True,
            "api_version": 6,
            "backseat_token": None,
            "backseat_token_updated_at": None
        },
        {
            "id": 90000000000000002,
            "vehicle_id": 900000002,
            "vin": "5Y000000000000002",
            "display_name": "Vehicle 02",
            "option_codes": "MDLS",
            "color": None,
            "tokens": [
                "aaaaaaaaaaaaaaa2",
                "bbbbbbbbbbbbbbb2"
            ],
            "state": "online",
            "in_service": False,
            "id_s": "90000000000000002",
            "calendar_enabled": True,
            "api_version": 6,
            "backseat_token": None,
            "backseat_token_updated_at": None
        },
        {
            "id": 90000000000000003,
            "vehicle_id": 900000003,
            "vin": "5Y000000000000003",
            "display_name": "Vehicle 03",
            "option_codes": "MDLX",
            "color": None,
            "tokens": [
                "aaaaaaaaaaaaaaa3",
                "bbbbbbbbbbbbbbb3"
            ],
            "state": "online",
            "in_service": False,
            "id_s": "90000000000000003",
            "calendar_enabled": True,
            "api_version": 6,
            "backseat_token": None,
            "backseat_token_updated_at": None
        },
        {
            "id": 90000000000000004,
            "vehicle_id": 900000004,
            "vin": "5Y000000000000004",
            "display_name": "Vehicle 04",
            "option_codes": "MDLS",
            "color": None,
            "tokens": [
                "aaaaaaaaaaaaaaa4",
                "bbbbbbbbbbbbbbb4"
            ],
            "state": "asleep",
            "in_service": False,
            "id_s": "90000000000000004",
            "calendar_enabled": True,
            "api_version": 6,
            "backseat_token": None,
            "backseat_token_updated_at": None
        }
    ]

    vehicle_data = {
        "90000000000000001": {
            "id": 90000000000000001,
            "user_id": 999999,
            "vehicle_id": 999999999,
            "vin": "5Y000000000000001",
            "display_name": "Vehicle 01",
            "option_codes": "MDL3",
            "color": None,
            "tokens": [
                "aaaaaaaaaaaaaaa1",
                "bbbbbbbbbbbbbbb1"
            ],
            "state": "online",
            "in_service": False,
            "id_s": "90000000000000001",
            "calendar_enabled": True,
            "api_version": 6,
            "backseat_token": None,
            "backseat_token_updated_at": None,
            "charge_state": {
                "battery_level": 82,
                "battery_range": 254.29
            },
            "gui_settings": {
                "gui_24_hour_time": True,
                "gui_charge_rate_units": "kW",
                "gui_distance_units": "km/hr",
                "gui_range_display": "Rated",
                "gui_temperature_units": "C",
                "show_range_units": False,
                "timestamp": 1561410259200
            },
            "vehicle_config": {
                "car_type": "model3",
                "charge_port_type": "CCS"
            },
            "vehicle_state": {
                "car_version": "2019.20.1 9973c22",
                "locked": True,
                "odometer": 4032.811076,
                "vehicle_name": "Vehicle 01"
            }
        },
        "90000000000000002": {
            "id": 90000000000000002,
            "user_id": 999999,
            "vehicle_id": 999999999,
            "vin": "5Y000000000000001",
            "display_name": "Vehicle 02",
            "option_codes": "MDL3",
            "color": None,
            "tokens": [
                "aaaaaaaaaaaaaaa1",
                "bbbbbbbbbbbbbbb1"
            ],
            "state": "online",
            "in_service": False,
            "id_s": "90000000000000001",
            "calendar_enabled": True,
            "api_version": 6,
            "backseat_token": None,
            "backseat_token_updated_at": None,
            "charge_state": {
                "battery_level": 82,
                "battery_range": 254.29
            },
            "gui_settings": {
                "gui_24_hour_time": True,
                "gui_charge_rate_units": "kW",
                "gui_distance_units": "km/hr",
                "gui_range_display": "Rated",
                "gui_temperature_units": "C",
                "show_range_units": False,
                "timestamp": 1561410259200
            },
            "vehicle_config": {
                "car_type": "model3",
                "charge_port_type": "CCS"
            },
            "vehicle_state": {
                "car_version": "2019.20.1 9973c22",
                "locked": True,
                "odometer": 4032.811076,
                "vehicle_name": "Vehicle 01"
            }
        },
        "90000000000000003": {
            "id": 90000000000000003,
            "user_id": 999999,
            "vehicle_id": 999999999,
            "vin": "5Y000000000000003",
            "display_name": "Vehicle 03",
            "option_codes": "MDL3",
            "color": None,
            "tokens": [
                "aaaaaaaaaaaaaaa1",
                "bbbbbbbbbbbbbbb1"
            ],
            "state": "online",
            "in_service": False,
            "id_s": "90000000000000001",
            "calendar_enabled": True,
            "api_version": 6,
            "backseat_token": None,
            "backseat_token_updated_at": None,
            "charge_state": {
                "battery_level": 82,
                "battery_range": 254.29
            },
            "gui_settings": {
                "gui_24_hour_time": True,
                "gui_charge_rate_units": "kW",
                "gui_distance_units": "km/hr",
                "gui_range_display": "Rated",
                "gui_temperature_units": "C",
                "show_range_units": False,
                "timestamp": 1561410259200
            },
            "vehicle_config": {
                "car_type": "model3",
                "charge_port_type": "CCS"
            },
            "vehicle_state": {
                "car_version": "2019.20.1 9973c22",
                "locked": True,
                "odometer": 4032.811076,
                "vehicle_name": "Vehicle 03"
            }
        }
    }

    def __init__(self, token='Demo Token'):
        self.token = token

    def get_token(self, email, password):
        if email == 'a' and password == 'b':
            return self.token_response
        else:
            raise TeslaApiError('User name or password not valid', 401, {})

    def refresh_token(self, refresh_token):
        return self.refresh_token_response

    def get_vehicles(self):
        logger.debug('getting vehicles from API')
        return self.vehicles_response

    def get_vehicle_data(self, id):
        logger.debug(f'getting vehicle data from API for {id}')
        if str(id) in self.vehicle_data:
            return self.vehicle_data[str(id)]
        else:
            raise TeslaApiError('not_found', 404, {})

    def wake_up(self, id):
        logger.debug(f'waking up {id}')
        responses = [x for x in self.vehicles_response if x['id'] == id]
        if len(responses) != 0:
            return responses[0]
        else:
            raise TeslaApiError('not_found', 404, {})

    def honk(self, id):
        logger.debug(f'honking {id}')
        responses = [x for x in self.vehicles_response if x['id'] == id]
        if len(responses) != 0:
            return {
                "response": {
                    "reason": "",
                    "result": True
                }
            }
        else:
            raise TeslaApiError('not_found', 404, {})

    def flash_lights(self, id):
        logger.debug(f'flashing lights {id}')
        responses = [x for x in self.vehicles_response if x['id'] == id]
        if len(responses) != 0:
            return {
                "response": {
                    "reason": "",
                    "result": True
                }
            }
        else:
            raise TeslaApiError('not_found', 404, {})
