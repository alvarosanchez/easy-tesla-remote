"""
Custom frame adapters for QT and helper functions.
"""
import logging
import etr.engine.util.adapters as extractors
import etr.engine.util.conversions

from etr.engine.util.adapters import (
    AdapterTracker,
    is_charging,
    fast_charger_present,
)
from etr.engine.util.dictionaries import get_dictionary_value


logger = logging.getLogger(__name__)


def execute_adapter(adapter_name, frame, qwidget):
    """
    Execute the adapter for a frame and apply the result to a QT widget.

    All the exceptions raised from the adapters will be handled and
    logged by the function.

    Args:
        - adapter_name (str): name of the adapter that will be executed.
        - frame (dict): frame to adapt.
        - qwidget (QWidget): QT widget that will be updated with the result.
    """
    adapter = AdapterTracker.resolve_adapter(adapter_name)
    if adapter is not None:
        try:
            attribute = qwidget.property('jsonAttribute')
            units = qwidget.property('units')
            conversion = qwidget.property('conversion')
            round_to = qwidget.property('round')

            result = adapter(frame, json_attribute=attribute, widget=qwidget)

            if conversion is not None:
                converter = AdapterTracker.resolve_adapter(conversion)
                if converter is not None:
                    result = converter(frame, **{'input': result})

            if round_to is not None and result is not None:
                result = round(result, round_to)

            if units is not None and result is not None:
                unit_generator = AdapterTracker.resolve_adapter(units)
                if unit_generator is not None:
                    units = unit_generator(frame)
                result = f'{result} {units}'

            target_property = qwidget.property('targetProperty')                
            if target_property is None:
                target_property = 'text'
            qwidget.setProperty(target_property, result)
        except Exception as error:
            logger.error(error)


@AdapterTracker.adapter('qt_progress_bar')
def progress_bar(frame, **kwargs):
    """
    Adapt a frame key into a QT progress bar.

    Args:
        - frame (dict): frame to adapt.

    Kwargs:
        - json_attribute (string): Name of the dict key that has to be adapted in an a.b.c format.
        - widget (optional)(QWidget): Target widget. It will be hidden if the dict attribute
            doesn't exist or is None.

    Returns:
        int. The value of the dict key or 0 if the key doesn't exist or is None.
    """
    value = get_dictionary_value(frame, kwargs['json_attribute'])
    if kwargs['widget'] is not None:
        if value is not None:
            kwargs['widget'].setVisible(True)
        else:
            kwargs['widget'].setVisible(False)
    return value if value is not None else 0


@AdapterTracker.adapter('qt_max_range')
def string_estimated_max_range(frame, **kwargs):
    """
    Estimate car's max range.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        float. Estimated max range for the car or None if it can't be generated
        using the frame data.
    """
    current_level = get_dictionary_value(frame, 'charge_state.battery_level')
    current_range = get_dictionary_value(frame, 'charge_state.battery_range')

    value = None

    if current_level is not None and current_range is not None:
        value = current_range * 100 / current_level

    return value


@AdapterTracker.adapter('qt_json_attribute')
def json_attribute(frame, **kwargs):
    """
    Read a key from a frame.

    Args:
        - frame (dict): frame to adapt.

    Kwargs:
        - json_attribute (string): Name of the dict key that has to be read. In an a.b.c format.

    Returns:
        The value of the dict key or None if it doesn't exist.
    """
    return get_dictionary_value(frame, kwargs['json_attribute'])


@AdapterTracker.adapter('qt_current')
def current(frame, **kwargs):
    """
    Get the charge current value from a frame.

    Args:
        - frame (dict): frame to adapt.

    Kwargs:
        - json_attribute (string): Name of the dict key that contains the value. In an a.b.c format.

    Returns:
        float. Charge current value adjusted by charger phases or None if it can't be generated
        using the frame data.
    """
    if is_charging(frame) and not fast_charger_present(frame):
        return get_dictionary_value(frame, kwargs['json_attribute'])
    return None


@AdapterTracker.adapter('qt_location_link')
def location_link(frame, **kwargs):
    """
    Build an HTML Google Maps link using the car position.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        string. HTML link to the car's position in Google Maps.
    """
    latitude = get_dictionary_value(frame, 'drive_state.latitude')
    longitude = get_dictionary_value(frame, 'drive_state.longitude') 
    return f'<a href="http://maps.google.es/?q={latitude},{longitude}">View on map</a>'
