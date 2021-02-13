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
import numpy as np
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


def extract_delivery_fee(text):
    regex_delivery_fee = r'Entrega & Manuseio 	R\$(\d+,\d{2})$'
    match = re.search(regex_delivery_fee, text, re.M)
    result = parse_float(match.group(1))
    return result


def extract_total(text):
    regex_total = r'Total 	R\$(\d+,\d{2})$'
    match = re.search(regex_total, text, re.M)
    result = parse_float(match.group(1))
    return result


def append_delivery_fee(df, fee):
    result = df.append(pd.Series(dtype=float), ignore_index=True)
    last_index = len(result)-1
    result.at[last_index, 'description'] = 'Entrega & Manuseio'
    result.at[last_index, 'amount'] = 1
    result.at[last_index, 'value'] = fee
    return result


def get_gnucash_dataframe(df,
                          col_names=None,
                          gnucash={'description': 'Bistek Supermercados',
                                   'expense': 'Expenses:Groceries',
                                   'payment': 'Liabilities:Credit Card',
                                   'currency': 'CURRENCY::BRL'}):
    if col_names:
        df = df.rename(columns=col_names)

    df.loc[1:, 'Date'] = np.nan
    df.at[0, 'Description'] = gnucash['description']
    df.at[0, 'Transaction Commodity'] = gnucash['currency']

    df = df.append(pd.Series(dtype=float), ignore_index=True)
    df.at[len(df)-1, 'Deposit'] = -df['Deposit'].sum()

    df['Account'] = gnucash['expense']
    df.at[len(df)-1, 'Account'] = gnucash['payment']
    # The price of one Real is... 1 BRL (no convension needed)
    df['Price'] = 1
    col_order = ['Date', 'Description', 'Transaction Commodity',
                 'Memo', 'Account', 'Deposit', 'Price']
    result = df[col_order]
    return result


def main(args):
    """ Process the order data """
    filename_in = args[1]
    filename_out = args[2]
    text = get_text(filename_in)
    tuples = get_item_tuples(text)
    df = get_df_from_tuples(tuples)
    clean_df = clean_dataframe(df)
    delivery_fee = extract_delivery_fee(text)
    clean_df = append_delivery_fee(clean_df, delivery_fee)
    clean_df['date'] = extract_date(text)
    clean_df = get_gnucash_dataframe(
        clean_df,
        col_names={
            'date': 'Date',
            'description': 'Memo',
            'value': 'Deposit'})
    # Sanity check
    assert clean_df['Deposit'].values[-1] == -extract_total(text)
    clean_df.to_csv(filename_out, index=False)


if __name__ == "__main__":
    main(sys.argv)
