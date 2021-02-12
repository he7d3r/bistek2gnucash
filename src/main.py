#!/usr/bin/env python3
"""
Process Bistek Notes
"""

__author__ = "Helder Geovane Gomes de Lima"
__version__ = "0.1.0"
__license__ = "MIT"

import sys
import re

import pandas as pd


def get_item_tuples(text):
    reg_item = r'(.+)\n\nSKU: (\d+)\n\s+(\d+)\s+R\$(\d+(?:\.\d{3})*,\d{2})$'
    result = [x.groups() for x in re.finditer(reg_item, text, re.M)]
    return result


def get_df_from_tuples(tuples):
    return pd.DataFrame(tuples,
                        columns=['description', 'code', 'amount', 'value'])


def clean_dataframe(df):
    df['code'] = df['code'].astype(int)
    df['amount'] = df['amount'].astype(int)
    df['value'] = df['value']\
        .str.replace('.', '')\
        .str.replace(',', '.')\
        .astype(float)
    return df


def get_text(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def main(file_name):
    """ Process the order data """
    text = get_text(file_name)
    tuples = get_item_tuples(text)
    df = get_df_from_tuples(tuples)
    clean_df = clean_dataframe(df)
    print(clean_df.tail())


if __name__ == "__main__":
    main(sys.argv[1])
