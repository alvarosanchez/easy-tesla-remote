from .api import TeslaApiError


class TeslaApiReplay():

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

    def __init__(self, replayer):
        self.token = 'Replay Token'
        self.replayer = replayer

    def get_token(self, email, password):
        return self.token_response

    def refresh_token(self, refresh_token):
        return self.refresh_token_response

    def get_vehicles(self):
        return self.replayer.next_status()

    def get_vehicle_data(self, id):
        return self.replayer.next_frame(id)

    def wake_up(self, id):
        raise TeslaApiError('not_found', 404, {})       

    def honk(self, id):
        raise TeslaApiError('not_found', 404, {})

    def flash_lights(self, id):
        raise TeslaApiError('not_found', 404, {})
