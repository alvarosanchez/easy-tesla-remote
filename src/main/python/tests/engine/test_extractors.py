"""
Tests for etr.engine.util.extractors
"""
import pytest
import etr.engine.util.extractors as extractors


@pytest.mark.parametrize('frame,result', [
    ({'gui_settings': {'gui_distance_units': 'km/hr'}}, 'km/hr'),
    ({'gui_settings': {'gui_distance_units': 'mi/hr'}}, 'mi/hr')
])
def test_get_speed_units(frame, result):
    value = extractors.get_speed_units(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'gui_settings': {'gui_distance_units': 'km/hr'}}, 'km'),
    ({'gui_settings': {'gui_distance_units': 'mi/hr'}}, 'mi')
])
def test_get_distance_units(frame, result):
    value = extractors.get_distance_units(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'gui_settings': {'gui_temperature_units': 'C'}}, 'C'),
    ({'gui_settings': {'gui_temperature_units': 'F'}}, 'F')
])
def test_get_temperature_units(frame, result):
    value = extractors.get_temperature_units(frame)
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
    value = extractors.is_charging(frame)
    assert value == result


@pytest.mark.parametrize('frame,result', [
    ({'charge_state': {'fast_charger_present': True}}, True),
    ({'charge_state': {'fast_charger_present': False}}, False),
    ({'charge_state': {'fast_charger_present': None}}, False)
])
def test_fast_charger_present(frame, result):
    value = extractors.fast_charger_present(frame)
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
    value = extractors.get_charger_phases(frame)
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
    value = extractors.get_charge_current(frame)
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
    value = extractors.get_charge_power(frame)
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
      'drive_state': { 'power': -100 }}, 500)
])
def test_get_charge_tension(frame, result):
    value = extractors.get_charge_tension(frame)
    assert value == result
