class SupportedEndpoints():

    AUTHENTICATE = 'AUTHENTICATE'
    REFRESH_TOKEN = 'REFRESH_TOKEN'
    VEHICLE_LIST = 'VEHICLE_LIST'
    VEHICLE_DATA = 'VEHICLE_DATA'
    WAKE_UP = 'WAKE_UP'
    HONK_HORN = 'HONK_HORN'
    FLASH_LIGHTS = 'FLASH_LIGHTS'

    def __init__(self):
        self.supported_endpoints = [
            self.AUTHENTICATE,
            self.VEHICLE_LIST,
            self.VEHICLE_DATA,
            self.WAKE_UP,
            self.HONK_HORN,
            self.FLASH_LIGHTS
        ]

    def get_config(self, endpoint):
        return tesla_endpoints[endpoint]


tesla_endpoints = {
    'AUTHENTICATE': {
      'METHOD': 'POST',
      'URL': 'oauth/token?grant_type={0}&client_id={1}&client_secret={2}&email={3}&password={4}',
      'AUTH': False,
      'VALID_RESULT': 200
    },
    'REFRESH_TOKEN': {
      'METHOD': 'POST',
      'URL': 'oauth/token?grant_type={0}&client_id={1}&client_secret={2}&refresh_token={3}',
      'AUTH': False,
      'VALID_RESULT': 200
    },
    'REVOKE_AUTH_TOKEN': {
      'METHOD': 'POST',
      'URL': 'oauth/revoke',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'PRODUCT_LIST': {
      'METHOD': 'GET',
      'URL': 'api/1/products',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'VEHICLE_LIST': {
      'METHOD': 'GET',
      'URL': 'api/1/vehicles',
      'AUTH': True,
      'VALID_RESULT': 200,
      'RESULT_KEY': 'response'
    },
    'VEHICLE_SUMMARY': {
      'METHOD': 'GET',
      'URL': 'api/1/vehicles/{0}',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'VEHICLE_DATA_LEGACY': {
      'METHOD': 'GET',
      'URL': 'api/1/vehicles/{0}/data',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'VEHICLE_DATA': {
      'METHOD': 'GET',
      'URL': 'api/1/vehicles/{0}/vehicle_data',
      'AUTH': True,
      'VALID_RESULT': 200,
      'RESULT_KEY': 'response'
    },
    'VEHICLE_SERVICE_DATA': {
      'METHOD': 'GET',
      'URL': 'api/1/vehicles/{0}/service_data',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'NEARBY_CHARGING_SITES': {
      'METHOD': 'GET',
      'URL': 'api/1/vehicles/{0}/nearby_charging_sites',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'WAKE_UP': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/wake_up',
      'AUTH': True,
      'VALID_RESULT': 200,
      'RESULT_KEY': 'response'
    },
    'UNLOCK': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/door_unlock',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'LOCK': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/door_lock',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'HONK_HORN': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/honk_horn',
      'AUTH': True,
      'VALID_RESULT': 200,
      'RESULT_KEY': 'response'
    },
    'FLASH_LIGHTS': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/flash_lights',
      'AUTH': True,
      'VALID_RESULT': 200,
      'RESULT_KEY': 'response'
    },
    'CLIMATE_ON': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/auto_conditioning_start',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'CLIMATE_OFF': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/auto_conditioning_stop',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'CHANGE_CLIMATE_TEMPERATURE_SETTING': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/set_temps',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'CHANGE_CHARGE_LIMIT': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/set_charge_limit',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'CHANGE_SUNROOF_STATE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/sun_roof_control',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'ACTUATE_TRUNK': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/actuate_trunk',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'REMOTE_START': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/remote_start_drive',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'CHARGE_PORT_DOOR_OPEN': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/charge_port_door_open',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'CHARGE_PORT_DOOR_CLOSE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/charge_port_door_close',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'START_CHARGE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/charge_start',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'STOP_CHARGE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/charge_stop',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'MEDIA_TOGGLE_PLAYBACK': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/media_toggle_playback',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'MEDIA_NEXT_TRACK': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/media_next_track',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'MEDIA_PREVIOUS_TRACK': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/media_prev_track',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'MEDIA_NEXT_FAVORITE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/media_next_fav',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'MEDIA_PREVIOUS_FAVORITE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/media_prev_fav',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'MEDIA_VOLUME_UP': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/media_volume_up',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'MEDIA_VOLUME_DOWN': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/media_volume_down',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SEND_LOG': {
      'METHOD': 'POST',
      'URL': 'api/1/logs',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SEND_REPORT': {
      'METHOD': 'POST',
      'URL': 'api/1/reports',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'RETRIEVE_NOTIFICATION_PREFERENCES': {
      'METHOD': 'GET',
      'URL': 'api/1/notification_preferences',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SEND_NOTIFICATION_PREFERENCES': {
      'METHOD': 'POST',
      'URL': 'api/1/notification_preferences',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'RETRIEVE_NOTIFICATION_SUBSCRIPTION_PREFERENCES': {
      'METHOD': 'GET',
      'URL': 'api/1/vehicle_subscriptions',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SEND_NOTIFICATION_SUBSCRIPTION_PREFERENCES': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicle_subscriptions',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'CALENDAR_SYNC': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/upcoming_calendar_entries',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SET_VALET_MODE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/set_valet_mode',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'RESET_VALET_PIN': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/reset_valet_pin',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SPEED_LIMIT_ACTIVATE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/speed_limit_activate',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SPEED_LIMIT_DEACTIVATE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/speed_limit_deactivate',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SPEED_LIMIT_SET_LIMIT': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/speed_limit_set_limit',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SPEED_LIMIT_CLEAR_PIN': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/speed_limit_clear_pin',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SCHEDULE_SOFTWARE_UPDATE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/schedule_software_update',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'CANCEL_SOFTWARE_UPDATE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/cancel_software_update',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SET_SENTRY_MODE': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/set_sentry_mode',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SITE_SUMMARY': {
      'METHOD': 'GET',
      'URL': 'api/1/energy_sites/{0}/status',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SITE_DATA': {
      'METHOD': 'GET',
      'URL': 'api/1/energy_sites/{0}/live_status',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SITE_CONFIG': {
      'METHOD': 'GET',
      'URL': 'api/1/energy_sites/{0}/site_info',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'HISTORY_DATA': {
      'METHOD': 'GET',
      'URL': 'api/1/energy_sites/{0}/history',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'BACKUP_RESERVE': {
      'METHOD': 'POST',
      'URL': 'api/1/energy_sites/{0}/backup',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'SITE_NAME': {
      'METHOD': 'POST',
      'URL': 'api/1/energy_sites/{0}/site_name',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'OPERATION_MODE': {
      'METHOD': 'POST',
      'URL': 'api/1/energy_sites/{0}/operation',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'TIME_OF_USE_SETTINGS': {
      'METHOD': 'POST',
      'URL': 'api/1/energy_sites/{0}/time_of_use_settings',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'STORM_MODE_SETTINGS': {
      'METHOD': 'POST',
      'URL': 'api/1/energy_sites/{0}/storm_mode',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'NAVIGATION_REQUEST': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/navigation_request',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'REMOTE_SEAT_HEATER_REQUEST': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/remote_seat_heater_request',
      'AUTH': True,
      'VALID_RESULT': 200
    },
    'REMOTE_STEERING_WHEEL_HEATER_REQUEST': {
      'METHOD': 'POST',
      'URL': 'api/1/vehicles/{0}/command/remote_steering_wheel_heater_request',
      'AUTH': True,
      'VALID_RESULT': 200
    }
}
