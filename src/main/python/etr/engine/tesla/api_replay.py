from .api import TeslaApiError
from .endpoints import SupportedEndpoints


class TeslaApiReplay():
    """
    Replay a set of pre recorded API responses
    """

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
        """
        :param replayer: replayer object that will provide the data
        """
        self.token = 'Replay Token'
        self.replayer = replayer
        self.urls = SupportedEndpoints

    def get_token(self, email, password):
        return self.token_response

    def refresh_token(self, refresh_token):
        return self.refresh_token_response

    def send_request(self, endpoint, *args):
        """
        Return the next response from the replayer and the endpoint

        Only VEHICLE_LIST and VEHICLE_DATA endpoints are supported
        """
        if endpoint == self.urls.VEHICLE_LIST:
            return self.replayer.next_status()
        elif endpoint == self.urls.VEHICLE_DATA:
            return self.replayer.next_frame(args[0])
        else:
             raise TeslaApiError('not_found', 404, {})
