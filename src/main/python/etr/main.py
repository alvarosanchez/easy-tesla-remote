import sys
import logging

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

engine.poll_rate = 0.25

@engine.handles(engine.events.REQUEST_DEMO_API)
def engine_demo_api():
    logger.debug('Engine requested a demo API')
    replayer = FileReplayer()
    replayer.prepare_frames()
    engine.switch_api(TeslaApiReplay(replayer), True)
    # engine.switch_api(TeslaApiMock(), True)


@engine.handles(engine.events.REQUEST_REAL_API)
def engine_real_api():
    logger.debug('Engine requested a real API')
    engine.switch_api(TeslaApi())


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s %(thread)d %(message)s'
    )

    ## Frame recorder
    # recorder = FileRecorder(engine)
    # recorder.start_recording()

    # QT UI with FBS context
    appctxt = ApplicationContext()
    main_window = MainWindow(engine)
    main_window.show()
    exit_code = appctxt.app.exec_()

    # AppEngine uses a long lived thread. This call
    # is required to ensure that the thread terminates
    engine.poll_stop()

    ## Stop frame recording
    # recorder.stop_recording()

    sys.exit(exit_code)
