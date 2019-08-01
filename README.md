# About

EasyTeslaRemote is a desktop application that interacts with your Tesla car through Tesla's API. Its main focus is privacy, your credentials will only be used to log in Tesla's servers and won't we send or stored anywhere else. Also the data obtained from Tesla won't leave your computer.

In this early stage the app functionality is pretty limited:
- Demo mode, so you can take a look at the app without using your Tesla credentials.
- Expose all the information about your car provided by Tesla's API.
- Keep your car awake without using Sentry Mode.
- Create an API token that can be used to allow other applications in your Tesla account.
- Option code translator.
- Wake up an asleep car. Honk its horn or flash its lights.

This application is possible thanks to the [unofficial Tesla API documentation](https://tesla-api.timdorr.com/).

# Installers

Soon

# Code setup

[Fman build system](https://build-system.fman.io/) is used as a build solution. Python 3.6 is required.

Create a virtual environment in the project's directory:

    # Windows
    python -m venv .venv
    # Linux / Mac
    python3 -m venv .venv

Activate the virtual environment:

    # Windows
    ./.venv/scripts/activate
    # Linux / Mac
    source .venv/bin/activate

Install the project's dependencies:

    pip install -r dev_requirements.txt

# Launch from code

In the virtual environment run:

    fbs run

# Building QT UI

QT UI is already built. But if you make any chages to the .ui files you will need to rebuild it. To do it launch the following script in the virtual environment:

    # Windows
    ./scripts/build_ui.ps1
    # Linux / Mac
    ./scripts/build_ui.sh

# Tests run

In the virtual environment run:

    # Windows
    ./scripts/run_tests.ps1
    # Linux / Mac
    ./scripts/run_tests.sh

# Freeze

In the virtual environment run:

    fbs freeze

# Build an installer

In the virtual environment run:

    fbs installer
