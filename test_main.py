import pandas as pd
from pandas.testing import assert_frame_equal

from main import get_df_from_tuples, get_item_tuples


def get_single_item_example():
    return ('Primeiro Item\n\n'
            'SKU: 1234567\n'
            '	3 	R$4.242,42')


def get_single_item_example_as_dataframe():
    return pd.DataFrame({
        'description': ['Primeiro Item'],
        'code': ['1234567'],
        'amount': ['3'],
        'value': ['4.242,42']
    })


def get_multiple_items_example():
    return ('Texto antes\n\n'
            'Primeiro Item\n\n'
            'SKU: 1231234\n'
            '	10 	R$0,42\n\n'
            '2º produto\n\n'
            'SKU: 1233210\n'
            '	2 	R$24.242,42\n\n'
            'Texto depois\n\n'
            'Item 3\n\n'
            'SKU: 1212121\n'
            '	100 	R$2.424.242,42\n\n'
            'Texto depois\n')


def get_multiple_items_example_as_dataframe():
    return pd.DataFrame({
        'description': ['Primeiro Item', '2º produto', 'Item 3'],
        'code': ['1231234', '1233210', '1212121'],
        'amount': ['10', '2', '100'],
        'value': ['0,42', '24.242,42', '2.424.242,42']
    })


def test_regex_for_single_item():
    sample_text = get_single_item_example()
    actual = get_item_tuples(sample_text)
    expected = [('Primeiro Item', '1234567', '3', '4.242,42')]
    assert actual == expected


def test_regex_for_multiple_items():
    sample_text = get_multiple_items_example()
    actual = get_item_tuples(sample_text)
    expected = [('Primeiro Item', '1231234', '10', '0,42'),
                ('2º produto', '1233210', '2', '24.242,42'),
                ('Item 3', '1212121', '100', '2.424.242,42')]
    assert actual == expected


def test_get_df_from_tuple():
    sample_text = get_single_item_example()
    tuples = get_item_tuples(sample_text)
    actual = get_df_from_tuples(tuples)
    expected = get_single_item_example_as_dataframe()
    assert_frame_equal(actual, expected)


def test_get_df_from_tuples():
    sample_text = get_multiple_items_example()
    tuples = get_item_tuples(sample_text)
    actual = get_df_from_tuples(tuples)
    expected = get_multiple_items_example_as_dataframe()
    assert_frame_equal(actual, expected)
