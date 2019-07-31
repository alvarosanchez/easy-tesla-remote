"""
Functions to manipulate dictionaries.
"""


def get_dictionary_value(dictionary, key):
    """
    Get the value under certain dictionary key.

    Supports composite keys formed by multiple keys separated by dots (a.b.c).

    Args:
        - dictionary (dict): root dictionary.
        - key (str): key or composite key.

    Returns:
        value under the key or None if the key is not found.
    """
    names = key.split('.', 1)

    if names is None:
        return None

    value = dictionary.get(names[0], None)

    if len(names) == 1:
        return value
    elif issubclass(type(value), dict):
        return get_dictionary_value(value, names[1])
    else:
        return None


def dump_to_tupple_list(dictionary, prefix=None):
    """
    Dump a dictionary into a list of tupples

    The function will iterate through the dictionaries contained in the
    original dictionary and add their values to the result using composite
    keys (a.b.c).

    Args:
        - dictionary (dict): dictionary to be dumped.
        - prefix (str): prefix that will be added to the dictionary keys.

    Returns:
        list of tupples with the dictionary and subdictionaries key/value
        pairs.
    """
    result = []

    for key,value in dictionary.items():
        name = f'{prefix}.{key}' if prefix is not None else f'{key}'
        if issubclass(type(value), dict):
            result.extend(dump_to_tupple_list(value, prefix=name))
        else:
            result.append((name, value))

    return result
