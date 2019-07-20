import logging

from datetime import timedelta

from etr.engine.util.dictionaries import get_dictionary_value
from etr.engine.util.extractors import (
    get_charge_tension,
    get_charge_power,
    get_charge_current,
)


logger = logging.getLogger(__name__)


class AdapterTracker:

    available_adapters = {}

    @classmethod
    def adapter(cls, name):
        def decorator(f):
            cls.available_adapters[name] = f
            return f
        return decorator

    @classmethod
    def resolve_adapter(cls, name):
        if name in cls.available_adapters:
            return cls.available_adapters[name]
        else:
            return None

    @classmethod
    def execute_adapter(cls, adapter_name, frame, key, qwidget=None, widget_property='text'):
        adapter = cls.resolve_adapter(adapter_name)
        if adapter != None:
            try:
                return adapter(frame, key, qwidget, widget_property)
            except Exception as ex:
                logger.error(ex)
        else:
            return None


@AdapterTracker.adapter('string')
def string(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    result = str(value) if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_temperature')
def string_temperature(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    temp_unit = get_dictionary_value(frame, 'gui_settings.gui_temperature_units')
    if temp_unit == None:
        temp_unit = ''
    result = f'{value} {temp_unit}' if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_distance')
def string_distance(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    distance_unit = get_dictionary_value(frame, 'gui_settings.gui_distance_units')

    if value != None and distance_unit == 'km/hr':
        value = value * 1.60934
        distance_unit = 'km'
    else:
        distance_unit = 'mi'

    result = f'{round(value, 2)} {distance_unit}' if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_speed')
def string_speed(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    distance_unit = get_dictionary_value(frame, 'gui_settings.gui_distance_units')

    if value != None and distance_unit == 'km/hr':
        value = value * 1.60934

    result = f'{round(value, 2)} {distance_unit}' if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_power')
def string_power(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)

    result = f'{value} kW' if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_energy')
def string_energy(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    result = f'{value} kWh' if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('current_to_battery')
def current_to_battery(frame, key, qwidget, widget_property):
    current = get_charge_current(frame)

    result = f'{current} A' if current != None else ''

    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_phases')
def string_current(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)

    result = ''

    if value != None:
        if value != 1:
            result = '3'
        else:
            result = '1'


    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_current_adjusted')
def string_current(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    phases = get_dictionary_value(frame, 'charge_state.charger_phases')

    result = ''

    if phases != None:
        if phases != 1:
            phases = 3
        
        result = f'{value * phases} A' if value != None else ''

    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_tension')
def string_tension(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    result = f'{value} V' if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_percentaje')
def string_percentaje(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    result = f'{value} %' if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('progress_bar')
def progress_bar(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    if qwidget != None:
        if value != None:
            qwidget.setProperty(widget_property, value)
            qwidget.setVisible(True)
        else:
            qwidget.setVisible(False)
    return value


@AdapterTracker.adapter('max_range')
def string_estimated_max_range(frame, key, qwidget, widget_property):
    current_level = get_dictionary_value(frame, 'charge_state.battery_level')
    current_range = get_dictionary_value(frame, 'charge_state.battery_range')
    distance_unit = get_dictionary_value(frame, 'gui_settings.gui_distance_units')

    value = None

    if current_level != None and current_range != None:
        value = current_range * 100 / current_level

    if value != None and distance_unit == 'km/hr':
        value = value * 1.60934
        distance_unit = 'km'
    else:
        distance_unit = 'mi'

    result = f'{round(value, 2)} {distance_unit}' if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('charge_power')
def string_charge_power(frame, key, qwidget, widget_property):
    power = get_charge_power(frame)

    value = f'{round(power, 2)} kW' if power != None else ''

    if qwidget != None:
        qwidget.setProperty(widget_property, value)
    return value


@AdapterTracker.adapter('charge_power_drawn')
def string_charge_power_drawn(frame, key, qwidget, widget_property):
    current = get_dictionary_value(frame, key)
    fast = get_dictionary_value(frame, 'charge_state.fast_charger_present')

    value = None

    if not fast:
        voltage = get_dictionary_value(frame, 'charge_state.charger_voltage')
        phases = get_dictionary_value(frame, 'charge_state.charger_phases')

        if current != None and voltage != None:
            value = current * voltage / 1000
            if phases != 1:
                value = value * 3
            value = f'{round(value, 2)} kW'

    if qwidget != None:
        qwidget.setProperty(widget_property, value)
    return value


@AdapterTracker.adapter('string_time')
def string_time(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    result = None

    if value != None:
        delta = timedelta(minutes=int(value * 60))
        result = str(delta)
    
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('charge_efficiency')
def charge_efficiency(frame, key, qwidget, widget_property):
    total_current = get_dictionary_value(frame, 'charge_state.charger_actual_current')
    phases = get_dictionary_value(frame, 'charge_state.charger_phases')
    rate = get_dictionary_value(frame, 'charge_state.charge_rate')

    result = ''

    if total_current != None and rate != None and phases != None and total_current != 0:
        if phases != 1:
            phases = 3
        result = f'{round(rate * 100 / (total_current * phases), 2)} %'

    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('location_link')
def location_link(frame, key, qwidget, widget_property):
    latitude = get_dictionary_value(frame, 'drive_state.latitude')
    longitude = get_dictionary_value(frame, 'drive_state.longitude')
    
    result = f'<a href="http://maps.google.es/?q={latitude},{longitude}">View on map</a>'
    
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('charge_tension')
def charge_tension(frame, key, qwidget, widget_property):
    tension = get_charge_tension(frame)

    result = f'{round(tension, 2)} V' if tension != None else ''

    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result
