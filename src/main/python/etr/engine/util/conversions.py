from .adapters import (
    AdapterTracker,
    get_distance_units,
)


def miles_to_km(value):
    if value == None:
        return None
    return value * 1.60934


def km_to_miles(value):
    if value == None:
        return None
    return value / 1.60934


@AdapterTracker.adapter('distance_conversion')
def convert_distance(frame, **kwargs):
    units = get_distance_units(frame)

    if units == 'km':
        return miles_to_km(kwargs['input'])
    else:
        return kwargs['input']


@AdapterTracker.adapter('to_string')
def string_conversion(frame, **kwargs):
    if kwargs['input'] != None:
        return str(kwargs['input'])
    else:
        return None
