import json
import os
import logging


logger = logging.getLogger(__name__)


class FileReplayer:
    """
    Replay recorded engine frames
    """

    def __init__(self, source_path=None):
        self._sequence_positions = {}
        self._files = {}
        self._vin_id_mappings = {}

        if source_path != None:
            self.source_path = source_path
        else:
            self.source_path = os.path.join(os.path.expanduser('~'), 'etr_recordings')

    def _read_file(self, file_name):
        file_path = os.path.join(self.source_path, file_name)
        with open(file_path) as json_file:
            return json.load(json_file)

    def _convert_frame(self, frame):
        return frame

    def prepare_frames(self):
        self._sequence_positions.clear()
        self._files.clear()
        self._vin_id_mappings.clear()

        for json_file in os.listdir(self.source_path):
            file_path = os.path.join(self.source_path, json_file)

            if os.path.isfile(file_path) and json_file.endswith('.json'):
                try:
                    # index the file
                    vin = json_file.partition('-')[0]
                    
                    if vin not in self._vin_id_mappings:
                        frame = self._read_file(json_file)
                        self._vin_id_mappings[vin] = frame['id']

                    car_id = self._vin_id_mappings[vin]

                    if car_id not in self._files:
                        self._files[car_id] = []
                        self._sequence_positions[car_id] = 0
                    self._files[car_id].append(json_file)

                except Exception as error:
                    logger.error(error)
        
        for car_id in self._files:
            self._files[car_id].sort()

    def next_status(self):
        result = []

        for car_id in self._sequence_positions:
            position = self._sequence_positions[car_id]
            file_name = self._files[car_id][position]
            frame = self._read_file(file_name)
            result.append(self._convert_frame(frame))

        return result

    def next_frame(self, car_id):
        if car_id in self._sequence_positions:
            position = self._sequence_positions[car_id]

            file_name = self._files[car_id][position]
            frame = self._read_file(file_name)

            position += 1
            if position >= len(self._files[car_id]):
                position = 0
            self._sequence_positions[car_id] = position

            return frame

        else:
            return {}
