from datetime import timedelta

from .dictionaries import get_dictionary_value


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
            return adapter(frame, key, qwidget, widget_property)
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

    if value != None and distance_unit == 'km\hr':
        value = value * 1.60934

    result = f'{round(value, 2)} {distance_unit}' if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_power')
def string_power(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    power_unit = get_dictionary_value(frame, 'gui_settings.gui_charge_rate_units')
    if power_unit == None:
        power_unit = ''
    result = f'{value} {power_unit}' if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_energy')
def string_energy(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    power_unit = get_dictionary_value(frame, 'gui_settings.gui_charge_rate_units')
    power_unit = f'{power_unit}h' if power_unit != None else ''
    result = f'{value} {power_unit}' if value != None else ''
    if qwidget != None:
        qwidget.setProperty(widget_property, result)
    return result


@AdapterTracker.adapter('string_current')
def string_current(frame, key, qwidget, widget_property):
    value = get_dictionary_value(frame, key)
    result = f'{value} A' if value != None else ''
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
    current = get_dictionary_value(frame, key)
    voltage = get_dictionary_value(frame, 'charge_state.charger_voltage')
    phases = get_dictionary_value(frame, 'charge_state.charger_phases')

    value = None

    if current != None and voltage != None:
        value = current * voltage / 1000
        if phases == 3:
            value = value * 1.732
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
