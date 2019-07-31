"""
Functions to manipulate dictionaries
"""


def get_dictionary_value(dictionary, key):
    """
    Get the value under certain dictionary key

    Supports composite keys formed by multiple keys separated by dots (a.b.c)
    
    :param dictionary: root dictionary.
    :param key: key or composite key.
    :return: value under the key or None if the key is not found.
    """
    names = key.split('.', 1)

    if names is None or names[0] not in dictionary:
        return None
    
    if len(names) == 1:
        return dictionary[names[0]]
    elif issubclass(type(dictionary[names[0]]), dict):
        return get_dictionary_value(dictionary[names[0]], names[1])
    else:
        return None


def dump_to_tupple_list(dictionary, prefix=None):
    """
    Dump a dictionary into a list of tupples

    The function will iterate through the dictionaries contained in the original
    dictionary and add their values to the result using composite keys (a.b.c)

    :param dictionary: dictionary to be dumped
    :param prefix: prefix that will be added to the dictionary keys
    :return: list of tupples with the dictionary and subdictionaries key/value pairs
    """
    result = []

    for key in dictionary:
        if issubclass(type(dictionary[key]), dict):
            new_prefix = f'{prefix}.{key}' if prefix is not None else f'{key}'
            result.extend(dump_to_tupple_list(dictionary[key], prefix=new_prefix))
        else:
            name = f'{prefix}.{key}' if prefix is not None else f'{key}'
            result.append((name, dictionary[key]))

    return result
