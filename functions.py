import pandas as pd
from exceptions import EmptyDataFrameError, ColumnDoesNotExist, FileTypeIsNotSupported
from bs4 import BeautifulSoup
import json
import os
import argparse
import re
from setup_logging import setup_logger

processed_success_logger = setup_logger('proccessed_success', 'proccessed_success.log')
processed_error_logger = setup_logger('processed_error', 'processed_error.log')


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


def set_output_file(path, output_file=None, output_dir=None):
    if output_file is not None:
        return output_file

    file_name, _ = os.path.splitext(os.path.basename(path))

    if output_dir is not None:
        return os.path.join(output_dir, file_name)

    return os.path.splitext(path)[0]


def parse_xml(path: str, output_type: str, output_file: str = None, output_dir: str = None):
    try:
        with open(path, 'r', encoding='utf-16') as f:
            soup = BeautifulSoup(f.read(), features="xml")

        # extract 'ObjectID', 'DirectoryID', 'TemplateName'
        om_object_data_dict = {k: soup.OM_OBJECT[k] for k in soup.OM_OBJECT.attrs if
                               k in ['ObjectID', 'DirectoryID', 'TemplateName']}

        # extract field values and merge
        om_field_data = soup.find_all('OM_FIELD')
        om_field_data_dict = {field['FieldID']: field.text.replace('\n', '') for field in om_field_data}
        combined_data = {**om_object_data_dict, **om_field_data_dict}

        # export
        output_path = set_output_file(path, output_file, output_dir)
        if output_type == 'json':
            with open(f'{output_path}.json', 'w', encoding='utf-16') as f:
                json.dump(combined_data, f)
        elif output_type in ('csv', 'tsv'):
            pd.DataFrame([combined_data]).to_csv(f'{output_path}.{output_type}', encoding='utf-16')
        processed_success_logger.info(f'{output_path}.{output_type} created successfully')
    except Exception as e:
        processed_error_logger.error(f'Parsing {path} failed due to error: {str(e)}.')


def dir_path(path: str) -> str:
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError(f"{path} is not a valid directory path.")


def parse_arguments():
    parser = argparse.ArgumentParser(description='XML file parsing')
    subparsers = parser.add_subparsers(dest='command')

    parse_file = subparsers.add_parser('parse_file', help='Parsing single XML file')
    parse_file.add_argument("--source_file", help="source file", action="store", dest="source")
    parse_file.add_argument("--output_file", help="output file (optional)", action="store", dest="output", default=None)
    parse_file.add_argument("--otype", help="possible options: csv,tsv,json,db", action="store", dest="out_type")

    search_and_parse = subparsers.add_parser('search_and_parse',
                                             help='Searching a directory and process all XML files within it.')
    search_and_parse.add_argument("--source_dir", help="source directory", action="store", dest="source_dir",
                                  type=dir_path)
    search_and_parse.add_argument("--source_dir_recurse",
                                  help="boolean value that indicates if program should search the subdirectories",
                                  action="store", dest="search_sub", type=bool)
    search_and_parse.add_argument("--source_file_regexp",
                                  help="Regular expression for file name. Kindly use double quotes.",
                                  action="store", dest="regex")
    search_and_parse.add_argument("--output_dir", help="output directory", action="store", dest="output_dir",
                                  default='.',
                                  type=dir_path)
    search_and_parse.add_argument("--otype", help="possible options: csv,tsv,json,db", action="store", dest="out_type")

    return parser.parse_args()


def validate_arguments_parse_file(args):
    if not os.path.isfile(args.source):
        raise FileNotFoundError("Source file was not found")
    if args.out_type not in ('csv', 'json', 'tsv'):
        raise FileTypeIsNotSupported("Data can be parsed to json, csv or tsv.")


def match_file(file, pattern):
    return file.endswith(".xml") and (pattern.match(file) if pattern else True)


def find_xml_files(directory: str, search_sub: bool, regex=None) -> list:
    pattern = re.compile(regex) if regex else None

    if search_sub:
        return [os.path.join(root, file) for root, subdir, files in os.walk(directory)
                for file in files if match_file(file, pattern)]
    return [os.path.join(directory, file) for file in os.listdir(directory) if match_file(file, pattern)]
