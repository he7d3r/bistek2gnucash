#!/usr/bin/env python3
"""
Process Bistek Notes
"""

__author__ = "Helder Geovane Gomes de Lima"
__version__ = "0.1.0"
__license__ = "MIT"

import re
import sys

import dateparser
import pandas as pd


def get_item_tuples(text):
    reg_item = r'(.+)\n\nSKU: (\d+)\n\s+(\d+)\s+R\$(\d+(?:\.\d{3})*,\d{2})$'
    result = [x.groups() for x in re.finditer(reg_item, text, re.M)]
    return result


def get_df_from_tuples(tuples):
    return pd.DataFrame(tuples,
                        columns=['description', 'code', 'amount', 'value'])


def parse_float(text):
    return float(text.replace('.', '').replace(',', '.'))


def clean_dataframe(df):
    df['code'] = df['code'].astype(int)
    df['amount'] = df['amount'].astype(int)
    df['value'] = df['value'].apply(parse_float)
    return df


def get_text(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def extract_date(text):
    regex_date = r'feito em (\d+ de .{0,9} de \d{4} \d{2}:\d{2}:\d{2}) foi'
    match = re.search(regex_date, text)
    date_time_string = match.group(1)
    return dateparser.parse(date_time_string).date()


def main(args):
    """ Process the order data """
    filename_in = args[1]
    filename_out = args[2]
    text = get_text(filename_in)
    tuples = get_item_tuples(text)
    df = get_df_from_tuples(tuples)
    clean_df = clean_dataframe(df)
    clean_df['date'] = extract_date(text)
    clean_df.to_csv(filename_out, index=False)


if __name__ == "__main__":
    main(sys.argv)
