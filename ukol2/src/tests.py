import pytest
import pandas as pd
from functions import parse_xml, find_xml_files
import json
import os
import shutil

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

    with open('./output.json', 'r', encoding='utf-16') as file:
        result_data = json.load(file)
    assert expected_data == result_data
    os.remove('test_file.xml')
    os.remove('output.json')


def test_find_xml_files(test_data):
    with open('./test_file2.xml', 'w', encoding='utf-16') as f:
        f.write(test_data)
    os.mkdir('.\\subdir')
    with open('./subdir/test_file3.xml', 'w', encoding='utf-16') as f:
        f.write(test_data)

    assert find_xml_files('.', search_sub=True, regex='^test.*') == ['.\\test_file2.xml', '.\\subdir\\test_file3.xml']
    assert find_xml_files('.', search_sub=False, regex='^test.*') == ['.\\test_file2.xml']
    os.remove('test_file2.xml')
    shutil.rmtree('subdir')
