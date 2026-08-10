###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
import os
import json
from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock

from scripts.snippets import read_json_file, parse_json_file, create_snippet_dict, read_python_file, read_file, parse_python_file, parse_file, list_files, main

###############################################################################
#  Snippets Test Case Implementation
###############################################################################


class SnippetsTestCase(TestCase):

    def test_read_json_file(self):
        file_name = 'temp.json'
        test_dict = {"key": "value"}

        with open(file_name, '+w') as temp_json:
            temp_json.write(json.dumps(test_dict))

        try:
            result = read_json_file(file_name)
        finally:
            os.remove(file_name)
            restul = {}

        self.assertEqual(result, test_dict)

    def test_create_template(self):
        file_name = "example"
        json_dict = {
            "prefix": "example",
            "body": {
                "id": "__FIELD_ID__",
                "name": "__FIELD_NAME__"
            },
            "scope": "json,jsonl",
            "description": "An example snippet"
        }
        expected_body = [
            '{',
            '  "id": "__FIELD_ID__",',
            '  "name": "__FIELD_NAME__"',
            '}'
        ]
        expected = {
            "prefix": "example",
            "scope": "json,jsonl",
            "description": "An example snippet",
            "body": expected_body
        }
        result = parse_json_file(file_name, json_dict)
        self.assertEqual(result, expected)

    def test_parse_json_file_with_multiple_body_items_adds_trailing_comma(self):
        json_dict = {
            'body': [
                {'key1': 'value1'},
                {'key2': 'value2'}
            ]
        }
        result = parse_json_file('my_snippet', json_dict)
        # The last line of the first body item should have a trailing comma
        body = result['body']
        self.assertTrue(any(line.endswith(',') for line in body))

    def test_read_python_file_returns_content(self):
        with patch('builtins.open', mock_open(read_data='def hello(): pass')):
            result = read_python_file('test.py')
        self.assertEqual(result, 'def hello(): pass')

    def test_read_file_py_type_returns_string(self):
        with patch('builtins.open', mock_open(read_data='def hello(): pass')):
            result = read_file('test.py', 'py')
        self.assertEqual(result, 'def hello(): pass')

    def test_parse_python_file_returns_snippet_dict(self):
        result = parse_python_file('my_snippet', 'def hello():\n    pass')
        expected = {
            'prefix': 'my_snippet',
            'scope': 'python',
            'body': ['def hello():', '    pass']
        }
        self.assertEqual(result, expected)

    def test_parse_file_py_type_returns_snippet(self):
        result = parse_file('my_snippet', 'def hello(): pass', 'py')
        expected = {
            'prefix': 'my_snippet',
            'scope': 'python',
            'body': ['def hello(): pass']
        }
        self.assertEqual(result, expected)

    def test_list_files_recurses_into_subdirectories(self):
        with patch('os.listdir') as mock_listdir, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.join', side_effect=lambda *args: '/'.join(args)):
            mock_listdir.side_effect = lambda p: ['subdir'] if p == 'base' else ['file.py']
            mock_isdir.side_effect = lambda p: p == 'base/subdir'

            result = list_files('base')

        self.assertEqual(result, ['base/subdir/file.py'])

    def test_main_writes_snippets_file(self):
        with patch('scripts.snippets.list_files', return_value=['snippets/test.json']), \
             patch('scripts.snippets.create_snippet_dict', return_value={'test': {}}), \
             patch('os.path.join', return_value='.vscode/everysk.code-snippets'), \
             patch('builtins.open', mock_open()) as mock_file:
            main()
        mock_file.assert_called_with('.vscode/everysk.code-snippets', 'w')

    @patch("scripts.snippets.read_json_file", side_effect=[
        {
            "body": {
                "id": "__FIELD_ID_1__",
                "name": "__FIELD_NAME_1__"
            },
            "scope": "json"
        },
        {
            "prefix": "field_two",
            "body": {
                "id": "__FIELD_ID_2__",
                "name": "__FIELD_NAME_2__"
            },
            "description": "New Field."
        }
    ])
    def test_create_snippet_dict(self, mock_read_json):
        expected = {
            "field_one": {
                "prefix": "field_one",
                "scope": "json",
                "description": "",
                "body": [
                    '{',
                    '  "id": "__FIELD_ID_1__",',
                    '  "name": "__FIELD_NAME_1__"',
                    '}'
                ]
            },
            "field_two": {
                "prefix": "field_two",
                "scope": "json,jsonl,jsonc",
                "description": "New Field.",
                "body": [
                    '{',
                    '  "id": "__FIELD_ID_2__",',
                    '  "name": "__FIELD_NAME_2__"',
                    '}'
                ]
            }
        }
        result = create_snippet_dict(["field_one.json", "field_two.json"])
        self.assertEqual(result, expected)
