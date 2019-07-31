"""
Unit conversion functions and adapters.
"""
from .adapters import (
    AdapterTracker,
    get_distance_units,
    get_temperature_units,
)


def miles_to_km(value):
    """
    Convert miles to kilometers

    Args:
        value (float): miles value

    Returns:
        float. Value converted to kilometers
    """
    if value is None:
        return None
    return value * 1.60934


def km_to_miles(value):
    """
    Convert kilometers to miles

    Args:
        value (float): kilometers value

    Returns:
        float. Value converted to miles
    """
    if value is None:
        return None
    return value / 1.60934


def celsius_to_fahrenheit(value):
    """
    Convert celsius to fahrenheit

    Args:
        value (float): celsius value

    Returns:
        float. Value converted to fahrenheit
    """
    if value is None:
        return None
    return (value * 1.8) + 32


@AdapterTracker.adapter('distance_conversion')
def convert_distance(frame, **kwargs):
    """
    Convert distance if the frame requires it.

    Args:
        frame (dict): frame to adapt.

    Kwargs:
        input (float): value to convert.

    Returns:
        float. Converted input value.
    """
    units = get_distance_units(frame)

    if units == 'km':
        return miles_to_km(kwargs['input'])
    else:
        return kwargs['input']


@AdapterTracker.adapter('to_string')
def string_conversion(frame, **kwargs):
    """
    Cast input to string.

    Args:
        frame (dict): frame to adapt.

    Kwargs:
        input: value to cast.

    Returns:
        string. Casted input value.
    """
    if kwargs['input'] is not None:
        return str(kwargs['input'])
    else:
        return None


@AdapterTracker.adapter('temperature_conversion')
def convert_temperature(frame, **kwargs):
    """
    Convert temperature if the frame requires it.

    Args:
        frame (dict): frame to adapt.

    Kwargs:
        input (float): value to convert.

    Returns:
        float. Converted input value.
    """
    units = get_temperature_units(frame)

    if units == 'F':
        return celsius_to_fahrenheit(kwargs['input'])
    else:
        return kwargs['input']
