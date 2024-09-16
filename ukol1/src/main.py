import pandas as pd
from functions_task1 import delete_rows


def main():
    try:
        file_name = 'data_cleanup.tsv'
        df = pd.read_csv(file_name, sep='\t')
        print("Rows to delete: ", delete_rows(df, id_col='ObjectID', check_na_col='Name'))
    except FileNotFoundError as e:
        print(f"The file {file_name} was not found: {e}")
    except IOError as e:
        print(f"An IO error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
