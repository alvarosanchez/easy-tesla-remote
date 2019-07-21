from datetime import timedelta
from .dictionaries import get_dictionary_value


class AdapterTracker:

    available_adapters = {}

    @classmethod
    def adapter(cls, name):
        def decorator(f):
            cls.register_adapter(name, f)
            return f
        return decorator

    @classmethod
    def register_adapter(cls, name, function):
        cls.available_adapters[name] = function

    @classmethod
    def resolve_adapter(cls, name):
        if name in cls.available_adapters:
            return cls.available_adapters[name]
        else:
            return None


@AdapterTracker.adapter('speed_units')
def get_speed_units(frame, **kwargs):
    return get_dictionary_value(frame, 'gui_settings.gui_distance_units')


@AdapterTracker.adapter('distance_units')
def get_distance_units(frame, **kwargs):
    unit = get_speed_units(frame)

    if unit != None and unit == 'km/hr':
        return 'km'
    else:
        return 'mi'


@AdapterTracker.adapter('temperature_units')
def get_temperature_units(frame, **kwargs):
    return get_dictionary_value(frame, 'gui_settings.gui_temperature_units')


@AdapterTracker.adapter('is_charging')
def is_charging(frame, **kwargs):
    charging = get_dictionary_value(frame, 'charge_state.charging_state')
    return charging == 'Charging'


@AdapterTracker.adapter('charger_present')
def fast_charger_present(frame, **kwargs):
    fast = get_dictionary_value(frame, 'charge_state.fast_charger_present')
    return fast == True


@AdapterTracker.adapter('charge_phases')
def get_charger_phases(frame, **kwargs):
    phases = get_dictionary_value(frame, 'charge_state.charger_phases')
    if is_charging(frame) and not fast_charger_present(frame) and phases != None:
        if phases == 1:
            return 1
        else:
            return 3
    else:
        return None


@AdapterTracker.adapter('charge_current')
def get_charge_current(frame, **kwargs):
    if is_charging(frame):
        return get_dictionary_value(frame, 'charge_state.charge_rate')
    else:
        return None


@AdapterTracker.adapter('charge_power')
def get_charge_power(frame, **kwargs):
    if is_charging(frame):
        if fast_charger_present(frame):
            power = get_dictionary_value(frame, 'drive_state.power')
            if power != None:
                return round(abs(power), 2)
            else:
                return None
        else:
            current = get_charge_current(frame)
            tension = get_dictionary_value(frame, 'charge_state.charger_voltage')
            if current != None and tension != None:
                return round(current * tension / 1000, 2)
            else:
                return None
    else:
        return None


@AdapterTracker.adapter('charge_tension')
def get_charge_tension(frame, **kwargs):
    if is_charging(frame):
        if fast_charger_present(frame):
            power = get_dictionary_value(frame, 'drive_state.power')
            current = get_charge_current(frame)

            if power != None and current != None:
                power = abs(power)
                return round((power * 1000) / current, 2)
            else:
                return None

        else:
            tension = get_dictionary_value(frame, 'charge_state.charger_voltage')
            return tension if tension != None and tension > 2 else None

    else: 
        return None


#--------------------------------------


@AdapterTracker.adapter('charge_efficiency')
def get_charge_efficiency(frame, **kwargs):
    if is_charging(frame) and not fast_charger_present(frame):
        phases = get_charger_phases(frame)
        effective_current = get_charge_current(frame)
        drawn_current = get_dictionary_value(frame, 'charge_state.charger_actual_current')

        if phases != None and drawn_current != None and effective_current != None:
            return round((effective_current * 100) / (drawn_current * phases), 2)

    return None


@AdapterTracker.adapter('charge_power_drawn')
def get_charge_power_drawn(frame, **kwargs):
    if is_charging(frame) and not fast_charger_present(frame):
        tension = get_charge_tension(frame)
        drawn_current = get_dictionary_value(frame, 'charge_state.charger_actual_current')
        phases = get_charger_phases(frame)

        if tension != None and phases != None and drawn_current != None:
            return round((drawn_current * tension / 1000) * phases, 2)

    return None


@AdapterTracker.adapter('charge_time_left')
def get_charge_time_left(frame, **kwargs):
    if is_charging(frame):
        time_left = get_dictionary_value(frame, 'charge_state.time_to_full_charge')

        if time_left != None:
            return timedelta(minutes=int(time_left * 60))

    return None


@AdapterTracker.adapter('charge_added')
def get_charge_added(frame, **kwargs):
    if is_charging(frame):
        return get_dictionary_value(frame, 'charge_state.charge_energy_added')

    return None


@AdapterTracker.adapter('engine_power')
def get_engine_power(frame, **kwargs):
    if not is_charging(frame):
        return get_dictionary_value(frame, 'drive_state.power')

    return None
