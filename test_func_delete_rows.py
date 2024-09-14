import pytest
import pandas as pd
from functions import delete_rows, parse_xml
from exceptions import EmptyDataFrameError, ColumnDoesNotExist
import json

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


test_xml = '''<?xml version="1.0" encoding="utf-16"?>
<OM_OBJECT DirectoryID="1234" ObjectID="5678" TemplateName="Contact Bin">
    <OM_HEADER>
        <OM_FIELD FieldID="1" FieldName="Čas vytvoření" FieldType="3" IsEmpty="no">
            <OM_DATETIME>20220207T134709,000</OM_DATETIME>
        </OM_FIELD>
        <OM_FIELD FieldID="2" FieldName="Aktualizováno kdy" FieldType="3" IsEmpty="no">
            <OM_DATETIME>20230312T135111,000</OM_DATETIME>
        </OM_FIELD>
    </OM_HEADER>
</OM_OBJECT>'''


@pytest.fixture
def test_data():
    return test_xml


def test_parse_xml(test_data):
    with open('test_file.xml', 'w', encoding='utf-16') as f:
        f.write(test_data)
    parse_xml('test_file.xml', 'json', 'output')

    expected_data = {
        'DirectoryID': '1234',
        'ObjectID': '5678',
        'TemplateName': 'Contact Bin',
        '1': '20220207T134709,000',
        '2': '20230312T135111,000'
    }

    with open('output.json', 'r', encoding='utf-16') as file:
        result_data = json.load(file)
    assert expected_data == result_data
