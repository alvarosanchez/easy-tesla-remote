#! /bin/sh
cd ui &&
find -name "*.ui" -exec sh -c 'pyuic5 "$0" -o "../src/main/python/etr/qt_interface/auto_generated/${0%.ui}_auto.py"' {} \; &&
cd ..
