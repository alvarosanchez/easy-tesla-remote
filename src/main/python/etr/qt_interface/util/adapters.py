import logging
import etr.engine.util.adapters as extractors
import etr.engine.util.conversions

from etr.engine.util.adapters import AdapterTracker
from etr.engine.util.dictionaries import get_dictionary_value


logger = logging.getLogger(__name__)


def execute_adapter(adapter_name, frame, qwidget):
    adapter = AdapterTracker.resolve_adapter(adapter_name)
    if adapter != None:
        try:
            attribute = qwidget.property('jsonAttribute')
            units = qwidget.property('units')
            conversion = qwidget.property('conversion')
            round_to = qwidget.property('round')

            result = adapter(frame, json_attribute=attribute, widget=qwidget)

            if conversion != None:
                converter = AdapterTracker.resolve_adapter(conversion)
                if converter != None:
                    result = converter(frame, **{'input': result})

            if round_to != None and result != None:
                result = round(result, round_to)

            if units != None and result != None:
                unit_generator = AdapterTracker.resolve_adapter(units)
                if unit_generator != None:
                    units = unit_generator(frame)
                result = f'{result} {units}'

            target_property = qwidget.property('targetProperty')                
            if target_property == None:
                target_property = 'text'
            qwidget.setProperty(target_property, result)
        except Exception as error:
            logger.error(error)


@AdapterTracker.adapter('qt_progress_bar')
def progress_bar(frame, **kwargs):
    value = get_dictionary_value(frame, kwargs['json_attribute'])
    if kwargs['widget'] != None:
        if value != None:
            kwargs['widget'].setVisible(True)
        else:
            kwargs['widget'].setVisible(False)
    return value if value != None else 0


@AdapterTracker.adapter('qt_max_range')
def string_estimated_max_range(frame, **kwargs):
    current_level = get_dictionary_value(frame, 'charge_state.battery_level')
    current_range = get_dictionary_value(frame, 'charge_state.battery_range')
    distance_unit = extractors.get_distance_units(frame)

    value = None

    if current_level != None and current_range != None:
        value = current_range * 100 / current_level

    return value


@AdapterTracker.adapter('qt_json_attribute')
def json_attribute(frame, **kwargs):
    return get_dictionary_value(frame, kwargs['json_attribute'])


@AdapterTracker.adapter('qt_current')
def current(frame, **kwargs):
    value = get_dictionary_value(frame, kwargs['json_attribute'])
    phases = extractors.get_charger_phases(frame)
    return value * phases if value != None and phases != None else None


@AdapterTracker.adapter('qt_location_link')
def location_link(frame, **kwargs):
    latitude = get_dictionary_value(frame, 'drive_state.latitude')
    longitude = get_dictionary_value(frame, 'drive_state.longitude') 
    return f'<a href="http://maps.google.es/?q={latitude},{longitude}">View on map</a>'
