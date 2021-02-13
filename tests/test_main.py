import datetime

import pandas as pd
from pandas.testing import assert_frame_equal
from src.main import (append_delivery_fee, clean_dataframe, extract_date,
                      extract_delivery_fee, extract_total, get_df_from_tuples,
                      get_item_tuples, get_text, parse_float)


def get_one_item_text():
    return ('Antes\nPrimeiro Item\n\n'
            'SKU: 1234567\n'
            '	3 	R$4.242,42\nDepois')


def get_one_item_list():
    return [('Primeiro Item', '1234567', '3', '4.242,42')]


def get_one_item_dataframe():
    return pd.DataFrame({
        'description': ['Primeiro Item'],
        'code': ['1234567'],
        'amount': ['3'],
        'value': ['4.242,42']
    })


def get_one_item_dataframe_clean():
    return pd.DataFrame({
        'description': ['Primeiro Item'],
        'code': [1234567],
        'amount': [3],
        'value': [4242.42]
    })


def get_many_items_text():
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


def get_many_items_list():
    return [('Primeiro Item', '1231234', '10', '0,42'),
            ('2º produto', '1233210', '2', '24.242,42'),
            ('Item 3', '1212121', '100', '2.424.242,42')]


def get_many_items_dataframe():
    return pd.DataFrame({
        'description': ['Primeiro Item', '2º produto', 'Item 3'],
        'code': ['1231234', '1233210', '1212121'],
        'amount': ['10', '2', '100'],
        'value': ['0,42', '24.242,42', '2.424.242,42']
    })


def get_many_items_dataframe_clean():
    return pd.DataFrame({
        'description': ['Primeiro Item', '2º produto', 'Item 3'],
        'code': [1231234, 1233210, 1212121],
        'amount': [10, 2, 100],
        'value': [0.42, 24242.42, 2424242.42]
    })


def get_summary_text():
    result = ('Subtotal 	R$432,10\n'
              'Entrega & Manuseio 	R$8,90\n'
              'Total 	R$441,00')
    return result


def test_regex_for_single_item():
    sample_text = get_one_item_text()
    actual = get_item_tuples(sample_text)
    expected = get_one_item_list()
    assert actual == expected


def test_regex_for_multiple_items():
    sample_text = get_many_items_text()
    actual = get_item_tuples(sample_text)
    expected = get_many_items_list()
    assert actual == expected


def test_get_df_from_tuple():
    tuples = get_one_item_list()
    actual = get_df_from_tuples(tuples)
    expected = get_one_item_dataframe()
    assert_frame_equal(actual, expected)


def test_get_df_from_tuples():
    tuples = get_many_items_list()
    actual = get_df_from_tuples(tuples)
    expected = get_many_items_dataframe()
    assert_frame_equal(actual, expected)


def test_clean_dataframe_single_item():
    df = get_one_item_dataframe()
    actual = clean_dataframe(df)
    expected = get_one_item_dataframe_clean()
    assert_frame_equal(actual, expected)


def test_clean_dataframe_multiple_items():
    df = get_many_items_dataframe()
    actual = clean_dataframe(df)
    expected = get_many_items_dataframe_clean()
    assert_frame_equal(actual, expected)


def test_get_text_contains_basic_text():
    text = get_text('tests/fake-text.txt')
    order_header_text = 'Detalhes do seu pedido'
    assert order_header_text in text
    table_header_text = 'Itens 	Quantidade 	Preço'
    assert table_header_text in text
    code_prefix_text = 'SKU'
    assert code_prefix_text in text
    total_text = 'Total'
    assert total_text in text


def test_extract_date():
    sample_text = 'pedido de nº 123 feito em 1 de fev de 2021 15:16:17 foi'
    actual = extract_date(sample_text)
    expected = datetime.date(2021, 2, 1)
    assert actual == expected


def test_parse_float():
    sample = '1,23'
    actual = parse_float(sample)
    expected = 1.23
    assert actual == expected

    sample = '5.432,10'
    actual = parse_float(sample)
    expected = 5432.10
    assert actual == expected

    sample = '98.765.432,10'
    actual = parse_float(sample)
    expected = 98765432.10
    assert actual == expected


def test_extract_total():
    sample_text = get_summary_text()
    actual = extract_total(sample_text)
    expected = 441.00
    assert actual == expected


def test_extract_delivery_fee():
    sample_text = get_summary_text()
    actual = extract_delivery_fee(sample_text)
    expected = 8.90
    assert actual == expected


def test_append_delivery_fee():
    sample_df = get_many_items_dataframe_clean()
    updated_df = append_delivery_fee(sample_df, 12.34)
    actual_len = len(updated_df)
    expected_len = len(sample_df) + 1
    assert actual_len == expected_len
    assert updated_df['value'].values[-1] == 12.34
