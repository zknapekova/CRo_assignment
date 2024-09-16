from exceptions_task1 import EmptyDataFrameError, ColumnDoesNotExist
from functions_task1 import delete_rows
import pandas as pd
import pytest

df_test = pd.DataFrame({
    'ObjectID': [1, 1, 2, 2, 3, 3, 4, 4, 5],
    'Name': [None, None, 'Alica', None, 'Beata', 'Cyril', None, 'Daniel', None],
    'RandomCol': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
})

@pytest.mark.parametrize("df, id_col, check_na_col, expected_result", [
    (df_test, 'ObjectID', 'Name', [1, 3, 6]),
    (pd.DataFrame(), 'ObjectID', 'Name', pytest.raises(EmptyDataFrameError)),
    (df_test, 'BSName1', 'BSName2', pytest.raises(ColumnDoesNotExist))
])
def test_delete_rows(df, id_col, check_na_col, expected_result):
    if type(expected_result) == list:
        assert delete_rows(df, id_col, check_na_col) == expected_result
    else:
        with expected_result:
            delete_rows(df, id_col, check_na_col)
