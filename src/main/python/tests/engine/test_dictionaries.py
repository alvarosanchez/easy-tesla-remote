"""
Tests for etr.engine.util.dictionaries
"""
import pytest

from etr.engine.util.dictionaries import (
    get_dictionary_value,
    dump_to_tupple_list,
)


@pytest.fixture
def dictionary():
    return {
        'a': 1,
        'b': 2,
        'c': None,
        'd': {
            'd1': 3,
            'd2': 4,
            'd5': {
                'd5a': '5'
            }
        }
    }


def test_get_dictionary_value(dictionary):
    val1 = get_dictionary_value(dictionary, 'a')
    val2 = get_dictionary_value(dictionary, 'c')
    val3 = get_dictionary_value(dictionary, 'd.d2')
    val4 = get_dictionary_value(dictionary, 'd.d5.d5a')

    assert val1 == 1
    assert val2 == None
    assert val3 == 4
    assert val4 == '5'


def test_get_dictionary_value_key_doesnt_exist(dictionary):
    val1 = get_dictionary_value(dictionary, 'z')
    val2 = get_dictionary_value(dictionary, 'z.z1.z1a')

    assert val1 == None
    assert val2 == None


def test_dump_to_tupple_list(dictionary):
    result = dump_to_tupple_list(dictionary)

    assert len(result) == 6
    assert result[0] == ('a', 1)
    assert result[1] == ('b', 2)
    assert result[2] == ('c', None)
    assert result[3] == ('d.d1', 3)
    assert result[4] == ('d.d2', 4)
    assert result[5] == ('d.d5.d5a', '5')
