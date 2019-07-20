from .dictionaries import get_dictionary_value


def get_speed_units(frame):
    return get_dictionary_value(frame, 'gui_settings.gui_distance_units')


def get_distance_units(frame):
    unit = get_speed_units(frame)

    if unit != None and unit == 'km/hr':
        return 'km'
    else:
        return 'mi'


def get_temperature_units(frame):
    return get_dictionary_value(frame, 'gui_settings.gui_temperature_units')


def is_charging(frame):
    charging = get_dictionary_value(frame, 'charge_state.charging_state')
    return charging == 'Charging'


def fast_charger_present(frame):
    fast = get_dictionary_value(frame, 'charge_state.fast_charger_present')
    return fast == True


def get_charger_phases(frame):
    phases = get_dictionary_value(frame, 'charge_state.charger_phases')
    if is_charging(frame) and not fast_charger_present(frame) and phases != None:
        if phases == 1:
            return 1
        else:
            return 3
    else:
        return None


def get_charge_current(frame):
    if is_charging(frame):
        return get_dictionary_value(frame, 'charge_state.charge_rate')
    else:
        return None


def get_charge_power(frame):
    if is_charging(frame):
        if fast_charger_present(frame):
            power = get_dictionary_value(frame, 'drive_state.power')
            if power != None:
                return abs(power)
            else:
                return None
        else:
            current = get_charge_current(frame)
            tension = get_dictionary_value(frame, 'charge_state.charger_voltage')
            if current != None and tension != None:
                return current * tension / 1000
            else:
                return None
    else:
        return None


def get_charge_tension(frame):
    if is_charging(frame):
        if fast_charger_present(frame):
            power = get_dictionary_value(frame, 'drive_state.power')
            current = get_charge_current(frame)

            if power != None and current != None:
                power = abs(power)
                return (power * 1000) / current
            else:
                return None

        else:
            tension = get_dictionary_value(frame, 'charge_state.charger_voltage')
            return tension if tension != None and tension > 5 else None

    else: 
        return None


# def get_charge_efficiency(frame):
#     if is_charging(frame) and not fast_charger_present(frame):
#         phases = get_charger_phases(frame)
#         rate = get_dictionary_value(frame, 'charge_state.charge_rate')
#         current = get_dictionary_value(frame, 'charge_state.charger_actual_current')
# 
#     else:
#         return None