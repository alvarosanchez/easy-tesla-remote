import sys
import logging
import time

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from etr.qt_interface.main_window import MainWindow
from etr.engine.app_engine import AppEngine
from etr.engine.tesla.api import TeslaApi
from etr.engine.tesla.api_replay import TeslaApiReplay
from etr.file_recorder.recorder import FileRecorder
from etr.file_recorder.replayer import FileReplayer


logger = logging.getLogger(__name__)
engine = AppEngine(TeslaApi())
demo_data_path = ''

# Frame recorder
recorder = FileRecorder(engine)


@engine.handles(engine.events.REQUEST_DEMO_API)
def engine_demo_api():
    logger.debug('Engine requested a demo API')
    recorder.stop_recording()
    time.sleep(0.5)
    replayer = FileReplayer(demo_data_path)
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
    demo_data_path = appctxt.get_resource('demo_data.zip')

    main_window = MainWindow(engine)
    main_window.show()
    exit_code = appctxt.app.exec_()

    # AppEngine uses a long lived thread. This call
    # is required to ensure that the thread terminates
    engine.poll_stop()

    # Stop frame recording
    recorder.stop_recording()

    sys.exit(exit_code)
