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

from scripts.snippets import read_json_file, parse_json_file, create_snippet_dict

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
