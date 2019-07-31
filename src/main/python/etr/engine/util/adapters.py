"""
Frame adapters and tracker class.
"""
from datetime import timedelta
from math import sqrt
from .dictionaries import get_dictionary_value


class AdapterTracker:
    """
    Static class that tracks all the available adapters and indexes them by
    name.

    To register adapters in other modules import this class and use the
    decorator.
    """

    available_adapters = {}

    @classmethod
    def adapter(cls, name):
        """
        Register the decorated function as an adapter.

        Args:
            - name (str): Name for the function.
        """
        def decorator(f):
            cls.register_adapter(name, f)
            return f
        return decorator

    @classmethod
    def register_adapter(cls, name, function):
        """
        Register an adapter function.

        If another function with the same name exits it will be replaced with
        the new one.

        Args:
            - name (str): name for the function.
            - function (function): function that will be registered.
        """
        cls.available_adapters[name] = function

    @classmethod
    def resolve_adapter(cls, name):
        """
        Resolve an adapter function.

        Args:
            - name (str): name for the function.

        Returns:
            function. Function indexed to that name or None if the name hasn't
            been registered.
        """
        return cls.available_adapters.get(name, None)


@AdapterTracker.adapter('speed_units')
def get_speed_units(frame, **kwargs):
    """
    Get the car's speed units.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        string. Car's speed units, usually km/hr or mi/hr.
    """
    return get_dictionary_value(frame, 'gui_settings.gui_distance_units')


@AdapterTracker.adapter('distance_units')
def get_distance_units(frame, **kwargs):
    """
    Get the car's distance units.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        string. Car's distance units, km or mi.
    """
    unit = get_speed_units(frame)

    if unit is not None and unit == 'km/hr':
        return 'km'
    else:
        return 'mi'


@AdapterTracker.adapter('temperature_units')
def get_temperature_units(frame, **kwargs):
    """
    Get the car's temperature units.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        string. Car's distance units, C or F.
    """
    return get_dictionary_value(frame, 'gui_settings.gui_temperature_units')


@AdapterTracker.adapter('is_charging')
def is_charging(frame, **kwargs):
    """
    Get if the car is charging.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        bool.
    """
    charging = get_dictionary_value(frame, 'charge_state.charging_state')
    return charging == 'Charging'


@AdapterTracker.adapter('charger_present')
def fast_charger_present(frame, **kwargs):
    """
    Get if the car is using a fast charger.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        bool.
    """
    fast = get_dictionary_value(frame, 'charge_state.fast_charger_present')
    return fast == True


@AdapterTracker.adapter('charge_phases')
def get_charger_phases(frame, **kwargs):
    """
    Get the number of phases when using the onboard charger.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        int. Number of charger phases or None if the car isn't charging or the onboard
        charger is not beign used.
    """
    phases = get_dictionary_value(frame, 'charge_state.charger_phases')
    if is_charging(frame) and not fast_charger_present(frame) and phases is not None:
        if phases == 1:
            return 1
        else:
            return 3
    else:
        return None


@AdapterTracker.adapter('charge_current')
def get_charge_current(frame, **kwargs):
    """
    Get the charge current.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        float. Charge current or None if the car is not charging.
    """
    if is_charging(frame):
        return get_dictionary_value(frame, 'charge_state.charge_rate')
    else:
        return None


@AdapterTracker.adapter('charge_power')
def get_charge_power(frame, **kwargs):
    """
    Get the charge power.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        float. Car's charge power or None if the car is not charging.
    """
    if is_charging(frame):
        if fast_charger_present(frame):
            power = get_dictionary_value(frame, 'drive_state.power')
            if power is not None:
                return round(abs(power), 2)
        else:
            current = get_charge_current(frame)
            tension = get_dictionary_value(frame, 'charge_state.charger_voltage')
            if current is not None and tension is not None:
                return round(current * tension / 1000, 2)
    return None


@AdapterTracker.adapter('charge_tension')
def get_charge_tension(frame, **kwargs):
    """
    Get the charge tension.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        float. Car's charge tension or None if the car is not charging.
    """
    if is_charging(frame) and not fast_charger_present(frame):
        tension = get_dictionary_value(frame, 'charge_state.charger_voltage')
        phases = get_charger_phases(frame)
        if phases is None:
            phases = 1
        if tension is not None and tension > 2:
            return tension * sqrt(phases)
    return None


@AdapterTracker.adapter('charge_efficiency')
def get_charge_efficiency(frame, **kwargs):
    """
    Get the charge efficiency when using the onboard charger.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        float. Charge efficiency or None if the charge efficiency can not be
        calculated.
    """
    if is_charging(frame) and not fast_charger_present(frame):
        phases = get_charger_phases(frame)
        effective_current = get_charge_current(frame)
        drawn_current = get_dictionary_value(frame, 'charge_state.charger_actual_current')

        if phases is not None and drawn_current is not None and effective_current is not None:
            return (effective_current * 100) / (drawn_current * phases)

    return None


@AdapterTracker.adapter('charge_power_drawn')
def get_charge_power_drawn(frame, **kwargs):
    """
    Get the power drawn by the onboard charger.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        float. Power drawn or None if the car is not charging or if it can not be
        calculated.
    """
    if is_charging(frame) and not fast_charger_present(frame):
        tension = get_charge_tension(frame)
        drawn_current = get_dictionary_value(frame, 'charge_state.charger_actual_current')
        phases = get_charger_phases(frame)

        if tension is not None and phases is not None and drawn_current is not None:
            return (drawn_current * tension / 1000) * sqrt(phases)

    return None


@AdapterTracker.adapter('charge_time_left')
def get_charge_time_left(frame, **kwargs):
    """
    Get the time left to complete the charge.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        timedelta. Time left or None if the car is not charging.
    """
    if is_charging(frame):
        time_left = get_dictionary_value(frame, 'charge_state.time_to_full_charge')

        if time_left is not None:
            return timedelta(minutes=int(time_left * 60))

    return None


@AdapterTracker.adapter('charge_added')
def get_charge_added(frame, **kwargs):
    """
    Get the charge added in the charge session.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        float. Charge added or None if the car is not charging.
    """
    if is_charging(frame):
        return get_dictionary_value(frame, 'charge_state.charge_energy_added')

    return None


@AdapterTracker.adapter('engine_power')
def get_engine_power(frame, **kwargs):
    """
    Get the battery pack output.

    Args:
        - frame (dict): frame to adapt.

    Returns:
        float. Battery pack output or None if the car is charging.
    """
    if not is_charging(frame):
        return get_dictionary_value(frame, 'drive_state.power')

    return None
