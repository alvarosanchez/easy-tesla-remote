import sys
import logging
import time

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from qt_interface.main_window import MainWindow
from engine.app_engine import AppEngine
from engine.tesla.api import TeslaApi
from engine.tesla.api_mock import TeslaApiMock
from engine.tesla.api_replay import TeslaApiReplay
from file_recorder.recorder import FileRecorder
from file_recorder.replayer import FileReplayer


logger = logging.getLogger(__name__)
engine = AppEngine(TeslaApi())

# Frame recorder
recorder = FileRecorder(engine)

@engine.handles(engine.events.REQUEST_DEMO_API)
def engine_demo_api():
    logger.debug('Engine requested a demo API')
    recorder.stop_recording()
    time.sleep(0.5)
    replayer = FileReplayer()
    replayer.prepare_frames()
    engine.poll_rate = 1
    engine.switch_api(TeslaApiReplay(replayer), True)


@engine.handles(engine.events.REQUEST_REAL_API)
def engine_real_api():
    logger.debug('Engine requested a real API')
    engine.poll_rate = 3
    recorder.start_recording()
    engine.switch_api(TeslaApi())


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s %(thread)d %(message)s'
    )

    # Enable recorder
    recorder.start_recording()

    # QT UI with FBS context
    appctxt = ApplicationContext()
    main_window = MainWindow(engine)
    main_window.show()
    exit_code = appctxt.app.exec_()

    # AppEngine uses a long lived thread. This call
    # is required to ensure that the thread terminates
    engine.poll_stop()

    # Stop frame recording
    recorder.stop_recording()

    sys.exit(exit_code)
