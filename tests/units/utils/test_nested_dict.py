import pytest

from explicitdev.utils.nested_dict import get_nested_dict

dict_1levels = {
    'test': 'test0'
}
dict_2levels = {
    'test': dict_1levels
}

dict_3levels = {
    'test': dict_2levels
}


@pytest.mark.parametrize(
    'dict_,keys,result',
    [
        ({}, ('test', 'test'), None),
        (dict_3levels, ('test', 'test', 'test'), 'test0'),
        (dict_2levels, ('test', 'test', 'test'), None),
        (dict_1levels, ('test',), 'test0'),

    ],

)
def test_get_nested_values(dict_, keys, result):
    assert result == get_nested_dict(dict_, *keys)
