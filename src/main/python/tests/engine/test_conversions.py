"""
Tests for etr.engine.util.conversions
"""
import pytest
import etr.engine.util.conversions as conversions


@pytest.mark.parametrize('value,result', [
    (1, 1.60934),
    (-1, -1.60934),
    (0, 0),
    (10.5, 16.89807),
    (None, None)
])
def test_miles_to_km(value, result):
    x = conversions.miles_to_km(value)
    assert x == result


@pytest.mark.parametrize('value,result', [
    (1.60934, 1),
    (-1.60934, -1),
    (0, 0),
    (16.89807, 10.5),
    (None, None)
])
def test_km_to_miles(value, result):
    x = conversions.km_to_miles(value)
    assert x == result


@pytest.mark.parametrize('frame,value,result', [
    ({'gui_settings': {'gui_distance_units': 'km/hr'}}, 1, 1.60934),
    ({'gui_settings': {'gui_distance_units': 'mi/hr'}}, 1, 1)
])
def test_convert_distance(frame, value, result):
    x = conversions.convert_distance(frame, **{'input': value})
    assert x == result


@pytest.mark.parametrize('value,result', [
    ('1', '1'),
    (1, '1'),
    (None, None)
])
def test_convert_distance(value, result):
    x = conversions.string_conversion({}, **{'input': value})
    assert x == result
