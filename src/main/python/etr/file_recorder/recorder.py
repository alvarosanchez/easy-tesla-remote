import json
import logging
from datetime import datetime
from os import path
from queue import (
    Queue,
    Full,
    Empty,
)
from threading import (
    Thread,
    Event,
)


logger = logging.getLogger(__name__)


class FileRecorder:
    """
    Record engine frames into json files

    The class can be attached to an engine and will record the frames produced into disk
    """

    def __init__(self, engine, destination_path=None, daemon=False):
        """
        :param engine: engine to record from
        :param destination_path: directory where the resulting files will be stored
        :param daemon: sets whether a daemon thread will be used by the recorder
        """
        self._app_engine = engine
        self.destination_path = destination_path
        self.wire_events()
        self._stop_recording = Event()
        self._recording_stopped = Event()
        self._recording_stopped.set()
        self._frame_queue = Queue(maxsize=500)
        self._thread = Thread(target=self._worker_thread, daemon=daemon)

    def wire_events(self):
        """
        Attach the recorder to the engine
        """
        self._app_engine.register_handler(
            self._app_engine.events.NEW_FRAMES_READY,
            self._on_frames_available
        )

    def unwire_events(self):
        """
        Detach the recorder from the engine
        """
        self._app_engine.unregister_handler(
            self._app_engine.events.NEW_FRAMES_READY,
            self._on_frames_available
        )

    def start_recording(self):
        """
        Start to record engine events
        """
        if self._recording_stopped.is_set():
            logger.debug('Starting recording')
            self._stop_recording.clear()
            self._thread.start()
        else:
            logger.warning('Request to start recording received but recording is already ongoing')

    def stop_recording(self):
        """
        Stop recording engine events

        The stop may not be inmediate because the thread that does the actual recording
        may need a bit of time to stop
        """
        logger.debug('Stopping recording')
        self._stop_recording.set()

    def _on_frames_available(self, frames):
        if not self._recording_stopped.is_set():
            for frame in frames:
                try:
                    self._frame_queue.put_nowait(frame)
                except Full:
                    logger.warning('Queue is full a frame was dropped')

    def _worker_thread(self):
        self._recording_stopped.clear()
        while not self._stop_recording.is_set():
            try:
                frame = self._frame_queue.get(timeout=0.5)
                file_name = f'{frame["vin"]}-{datetime.now().timestamp()}.json'
                file_path = path.join(self.destination_path, file_name)

                with open(file_path, 'w') as recorded_frame:
                    json.dump(frame, recorded_frame, indent=3)

            except Empty:
                pass
            except Exception as error:
                logger.error(error)

        self._recording_stopped.set()

        while not self._frame_queue.empty():
            self._frame_queue.get()
