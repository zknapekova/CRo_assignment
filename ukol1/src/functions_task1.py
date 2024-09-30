import pandas as pd
from exceptions_task1 import EmptyDataFrameError, ColumnDoesNotExist

def delete_rows(df: pd.DataFrame, id_col: str, check_na_col: str) -> list:
    # check if the table is not empty
    if df.empty:
        raise EmptyDataFrameError("The DataFrame is empty")

    missing_cols = [col for col in [id_col, check_na_col] if col not in df.columns]
    if missing_cols:
        raise ColumnDoesNotExist(f"Missing columns: {', '.join(missing_cols)}")

    # get ObjectIDs for which all Name values are empty
    ids_all_na = df.groupby(id_col)[check_na_col] \
                    .apply(lambda x: x.isnull().all()) \
                    .reset_index()
    # find first occurrence of those Object IDs
    first_occurrence = df[
                        df[id_col].isin(ids_all_na[id_col][ids_all_na[check_na_col] == True])]\
                        .drop_duplicates(id_col)

    # keep first occurences and remove all other NA values
    rows_to_keep = pd.concat([df.dropna(subset=[check_na_col]), first_occurrence])

    # get list of row indexes that were deleted
    rows_to_delete = df[~df.index.isin(rows_to_keep.index)]\
                        .index.tolist()

    return rows_to_delete