import pandas as pd
from exceptions import EmptyDataFrameError, ColumnDoesNotExist, FileTypeIsNotSupported
from bs4 import BeautifulSoup
import json
import os
import argparse

def delete_rows(df: pd.DataFrame, id_col: str, check_na_col: str) -> list:
    # check if the table is not empty
    if df.empty:
        raise EmptyDataFrameError("The DataFrame is empty")

    missing_cols = [col for col in [id_col, check_na_col] if col not in df.columns]
    if missing_cols:
        raise ColumnDoesNotExist(f"Missing columns: {', '.join(missing_cols)}")

    # get ObjectIDs for which all Name values are empty
    ids_all_na = df.groupby(id_col)[check_na_col].apply(lambda x: x.isnull().all()).reset_index()

    # get first occurrences for those IDs
    first_occurrence = df[
        df[id_col].isin(ids_all_na[id_col][ids_all_na[check_na_col] == True])].drop_duplicates(id_col)

    # delete all non empty values and combine it with first_occurrence df
    rows_to_keep = pd.concat([df.dropna(subset=[check_na_col]), first_occurrence])

    return df[~df.index.isin(rows_to_keep.index)].index.tolist()

def parse_xml(path: str, output_type: str, output_file: str):
    with open(path, 'r', encoding='utf-16') as f:
        soup = BeautifulSoup(f.read(), features="xml")

    # extract 'ObjectID', 'DirectoryID', 'TemplateName'
    om_object_data_dict = {k: soup.OM_OBJECT[k] for k in soup.OM_OBJECT.attrs if k in ['ObjectID', 'DirectoryID', 'TemplateName']}

    # extract field values and merge
    om_field_data = soup.find_all('OM_FIELD')
    om_field_data_dict = {field['FieldID']: field.text.replace('\n', '') for field in om_field_data}
    combined_data = {**om_object_data_dict, **om_field_data_dict}

    # export
    if output_type == 'json':
        with open(f'{output_file}.json', 'w', encoding='utf-16') as f:
            json.dump(combined_data, f)
    elif output_type in ('csv', 'tsv'):
        pd.DataFrame([combined_data]).to_csv(f'{output_file}.{output_type}', encoding='utf-16')


def parse_arguments():
    parser = argparse.ArgumentParser(description='XML file parsing')
    parser.add_argument("--source_file", help="source file", action="store", dest="source")
    parser.add_argument("--output_file", help="output file (optional)", action="store", dest="output", default=None)
    parser.add_argument("--otype", help="possible options: csv,tsv,json,db", action="store", dest="out_type")
    return parser.parse_args()

def validate_arguments(args):
    if not os.path.isfile(args.source):
        raise FileNotFoundError("Source file was not found")
    if args.out_type not in ('csv', 'json', 'tsv'):
        raise FileTypeIsNotSupported("Data can be parsed to json, csv or tsv.")
    if args.output is None:
        args.output = os.path.splitext(args.source)[0]