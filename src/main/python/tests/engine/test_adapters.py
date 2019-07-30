"""
Tests for etr.engine.util.adapters
"""
import pytest
import etr.engine.util.adapters as adapters

from datetime import timedelta


@pytest.mark.parametrize('frame,result', [
    ({'gui_settings': {'gui_distance_units': 'km/hr'}}, 'km/hr'),
    ({'gui_settings': {'gui_distance_units': 'mi/hr'}}, 'mi/hr')
])
def test_get_speed_units(frame, result):
    value = adapters.get_speed_units(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'gui_settings': {'gui_distance_units': 'km/hr'}}, 'km'),
    ({'gui_settings': {'gui_distance_units': 'mi/hr'}}, 'mi')
])
def test_get_distance_units(frame, result):
    value = adapters.get_distance_units(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'gui_settings': {'gui_temperature_units': 'C'}}, 'C'),
    ({'gui_settings': {'gui_temperature_units': 'F'}}, 'F')
])
def test_get_temperature_units(frame, result):
    value = adapters.get_temperature_units(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {'charging_state': 'Charging'}}, True),
    ({'charge_state': {'charging_state': 'Starting'}}, False),
    ({'charge_state': {'charging_state': 'Disconnected'}}, False),
    ({'charge_state': {'charging_state': 'Stopped'}}, False),
    ({'charge_state': {'charging_state': 'Complete'}}, False),
    ({'charge_state': {'charging_state': None}}, False)
])
def test_is_charging(frame, result):
    value = adapters.is_charging(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {'fast_charger_present': True}}, True),
    ({'charge_state': {'fast_charger_present': False}}, False),
    ({'charge_state': {'fast_charger_present': None}}, False)
])
def test_fast_charger_present(frame, result):
    value = adapters.fast_charger_present(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charger_phases': 1 }}, 1),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charger_phases': 2 }}, 3),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charger_phases': 3 }}, 3),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charger_phases': None }}, None),
    ({'charge_state': {
        'charging_state': 'Stopped',
        'fast_charger_present': False,
        'charger_phases': 1 }}, None),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': True,
        'charger_phases': 1 }}, None)
])
def test_get_charger_phases(frame, result):
    value = adapters.get_charger_phases(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {
        'charging_state': 'Charging',
        'charge_rate': 0.1}}, 0.1),
    ({'charge_state': {
        'charging_state': 'Charging',
        'charge_rate': 15.99}}, 15.99),
    ({'charge_state': {
        'charging_state': 'Stopped',
        'charge_rate': 16}}, None)
])
def test_get_charge_current(frame, result):
    value = adapters.get_charge_current(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charge_rate': 5,
        'charger_voltage': 100},
      'drive_state': { 'power': -99 }}, 0.5),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': True,
        'charge_rate': 5,
        'charger_voltage': 100},
      'drive_state': { 'power': -99 }}, 99),
    ({'charge_state': {
        'charging_state': 'Stopped',
        'fast_charger_present': False,
        'charge_rate': 5,
        'charger_voltage': 100},
      'drive_state': { 'power': 99 }}, None),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charge_rate': None,
        'charger_voltage': None},
      'drive_state': { 'power': None }}, None),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': True,
        'charge_rate': None,
        'charger_voltage': None},
      'drive_state': { 'power': None }}, None)
])
def test_get_charge_power(frame, result):
    value = adapters.get_charge_power(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charge_rate': 5,
        'charger_voltage': 2},
      'drive_state': { 'power': -99 }}, None),
    ({'charge_state': {
        'charging_state': 'Stopped',
        'fast_charger_present': False,
        'charge_rate': 5,
        'charger_voltage': 2},
      'drive_state': { 'power': -99 }}, None),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charge_rate': None,
        'charger_voltage': None},
      'drive_state': { 'power': None }}, None),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': True,
        'charge_rate': None,
        'charger_voltage': None},
      'drive_state': { 'power': None }}, None),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charge_rate': 48,
        'charger_voltage': 240},
      'drive_state': { 'power': -100 }}, 240),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': True,
        'charge_rate': 200,
        'charger_voltage': 240},
      'drive_state': { 'power': -100 }}, None)
])
def test_get_charge_tension(frame, result):
    value = adapters.get_charge_tension(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': True}}, None),
    ({'charge_state': {
        'charging_state': 'Stopped',
        'fast_charger_present': False}}, None),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charger_actual_current': 16,
        'charge_rate': 16,
        'charger_phases': 1 }}, 100),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charger_actual_current': 16,
        'charge_rate': 48,
        'charger_phases': 3 }}, 100)
])
def test_get_charge_efficiency(frame, result):
    value = adapters.get_charge_efficiency(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': True}}, None),
    ({'charge_state': {
        'charging_state': 'Stopped',
        'fast_charger_present': False}}, None),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charger_actual_current': 16,
        'charge_rate': 16,
        'charger_voltage': 240,
        'charger_phases': 1 }}, 3.84),
    ({'charge_state': {
        'charging_state': 'Charging',
        'fast_charger_present': False,
        'charger_actual_current': 16,
        'charge_rate': 16,
        'charger_voltage': 240,
        'charger_phases': 3 }}, 11.519999999999998)
])
def test_get_charge_power_drawn(frame, result):
    value = adapters.get_charge_power_drawn(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {
        'charging_state': 'Stopped'}}, None),
    ({'charge_state': {
        'charging_state': 'Charging',
        'time_to_full_charge': 1}}, timedelta(hours=1)),
    ({'charge_state': {
        'charging_state': 'Charging',
        'time_to_full_charge': 0.6}}, timedelta(minutes=36))
])
def test_get_charge_time_left(frame, result):
    value = adapters.get_charge_time_left(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {
        'charging_state': 'Stopped'}}, None),
    ({'charge_state': {
        'charging_state': 'Charging',
        'charge_energy_added': 0.1}}, 0.1)
])
def test_get_charge_added(frame, result):
    value = adapters.get_charge_added(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {
        'charging_state': 'Charging'}}, None),
    ({'charge_state': {
        'charging_state': 'Disconnected'},
      'drive_state': {
          'power': 11}}, 11)
])
def test_get_engine_power(frame, result):
    value = adapters.get_engine_power(frame)
    assert value == result
