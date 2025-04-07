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
#  Imports
###############################################################################s
from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock

from scripts.deploy import (
    find_substring,
    remove_comments,
    create_form_functions_dict,
    http_request,
    parse_template_files,
    update_template
)

###############################################################################
#  Deploy Functions Test Case Implementation
###############################################################################
class DeployTestCase(TestCase):

    ###############################################################################
    #  Find Substring Test Case Implementation
    ###############################################################################
    def test_find_substring_returns_expected_data(self):
        expected_index = 5
        result = find_substring('hello world', 1, 'world')

        self.assertEqual(result, expected_index)

    def test_find_substring_returns_minus_one_when_substring_is_not_found(self):
        expected_index = -1
        result = find_substring('hello world', 6, 'hello')

        self.assertEqual(result, expected_index)

    def test_find_substring_with_integer_raises_type_error(self):
        with self.assertRaises(TypeError) as context:
            find_substring(1, 1, 'hello')

        self.assertEqual(str(context.exception), "'int' object is not subscriptable")

    def test_find_substring_with_substring_as_integer_raises_type_error(self):
        with self.assertRaises(TypeError) as context:
            find_substring('hello world', 1, 1)

        self.assertEqual(str(context.exception), "must be str, not int")

    def test_find_substring_with_unicode_rich_string_returns_expected_data(self):
        expected_index = 4
        result = find_substring('こんにちは、世界!', 1, '、世界')

        self.assertEqual(result, expected_index)

    ###############################################################################
    #  Remove Comments Test Case Implementation
    ###############################################################################
    def test_remove_comments_returns_expected_data(self):
        input_data = ''''
            {
                "key": "value",// this is a single line comment
                "number": 1/* this is a block comment */
            }
        '''
        expected_output = ''''
            {
                "key": "value",
                "number": 1
            }
        '''
        result = remove_comments(input_data)

        self.assertEqual(result, expected_output)

    def test_remove_comments_with_no_comments_returns_expected_data(self):
        input_data = ''''
            {
                "key": "value",
                "number": 1
            }
        '''
        expected_output = ''''
            {
                "key": "value",
                "number": 1
            }
        '''
        result = remove_comments(input_data)

        self.assertEqual(result, expected_output)

    def test_remove_comments_with_integer_raises_type_error(self):
        with self.assertRaises(TypeError) as context:
            remove_comments(1)

        self.assertEqual(str(context.exception), "expected string or bytes-like object, got 'int'")

    ###############################################################################
    #  Create Form Functions Dict Test Case Implementation
    ###############################################################################
    def test_create_form_functions_dict_returns_expected_data(self):
        functions_code_input = '''
            def foo():
                return 'bar'
            def baz():
                return 'qux'
        '''
        expected_output = {'foo': "\n\n            def foo():\n                return 'bar'\n            def baz():\n                return 'qux'\n       "}
        result = create_form_functions_dict(functions_code_input)

        self.assertEqual(result, expected_output)

    def test_create_form_functions_dict_with_integer_input_raises_type_error(self):
        with self.assertRaises(TypeError) as context:
            create_form_functions_dict(1)

        self.assertEqual(str(context.exception), 'can only concatenate str (not "int") to str')

    def test_create_form_functions_dict_without_functions_returns_empty_dict(self):
        function_code_input = 'this will make the function return an empty dict'
        result = create_form_functions_dict(function_code_input)

        self.assertEqual(result, {})

    def test_create_form_functions_dict_without_input_raises_type_error(self):
        with self.assertRaises(TypeError) as context:
            create_form_functions_dict()

        self.assertEqual(str(context.exception), "create_form_functions_dict() missing 1 required positional argument: \'functions_text\'")

    ###############################################################################
    #  HTTP Request Test Case Implementation
    ###############################################################################
    def test_http_request_method_returns_expected_data_and_status_code(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Successful request operation"
        mock_response.json.return_value = {'worker_template': {'key': 'value'}}

        with patch('requests.request') as mock_request:
            mock_request.return_value = mock_response
            response = http_request({'key': 'value'}, 'GET', 'http://example.com')

        expected_response = (200, "Successful request operation.", {'key': 'value'})
        self.assertEqual(response, expected_response)

    def test_http_request_method_when_status_code_is_different_than_200_returns_error(self):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = 'Bad request error'
        mock_response.json.return_value = {}

        with patch('requests.request') as mock_request:
            mock_request.return_value = mock_response
            response = http_request({'key': 'value'}, 'GET', 'http://example.com')

        expected_response = (400, "Error on http_request: Bad request error", {})
        self.assertEqual(response, expected_response)

    def test_http_request_method_with_invalid_url_returns_error(self):
        with self.assertRaises(Exception) as context:
            http_request({'key': 'value'}, 'GET', 1)

        expected_error_message = "Invalid URL '1': No scheme supplied. Perhaps you meant https://1?"
        self.assertEqual(str(context.exception), expected_error_message)

    def test_http_request_method_with_invalid_method_returns_error(self):
        mock_response = MagicMock()
        mock_response.status_code = 501
        mock_response.text = 'Not Implemented'
        mock_response.json.return_value = {}

        with patch('requests.request') as mock_request:
            mock_request.return_value = mock_response
            response = http_request({'key': 'value'}, 'INVALID', 'http://example.com')

        expected_response = (501, "Error on http_request: Not Implemented", {})
        self.assertEqual(response, expected_response)

    def test_http_request_method_with_invalid_worker_template_data_returns_error(self):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_response.json.return_value = {}

        with patch('requests.request') as mock_request:
            mock_request.return_value = mock_response
            response = http_request({'key': 'value'}, 'GET', 'http://example.com')

        expected_response = (400, "Error on http_request: Bad request", {})
        self.assertEqual(response, expected_response)

    ###############################################################################
    #  Parse Template Files Test Case Implementation
    ###############################################################################
    @patch('scripts.deploy.zip_directory_to_str')
    @patch('builtins.open', new_callable=mock_open, read_data='{"name": "test_worker"}')
    def test_parse_template_files_returns_expected_data(self, mock_file, mock_zip):
        mock_zip.return_value = 'UEsFBgAAAAAAAAAAAAAAAAAAAAAAAA=='

        expected_result = {
            'name': 'test_worker',
            'form_inputs': {'name': 'test_worker'},
            'form_outputs': {'name': 'test_worker'},
            'form_functions': {},
            'description': '{"name": "test_worker"}',
            'script_source': 'UEsFBgAAAAAAAAAAAAAAAAAAAAAAAA==',
            'path_name': 'folder_name',
            'icon': None
        }
        with patch('os.listdir') as mocked_listdir:
            mocked_listdir.return_value = ['config.json']
            result = parse_template_files('workers/worker_path', 'folder_name')

        self.assertEqual(result, expected_result)

    @patch('scripts.deploy.zip_directory_to_str')
    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    def test_parse_template_files_with_no_worker_template_returns_error(self, mock_file, mock_zip):
        mock_zip.return_value = 'UEsFBgAAAAAAAAAAAAAAAAAAAAAAAA=='

        expected_error_result = {
            'description': '{}',
            'form_functions': {},
            'form_inputs': {},
            'form_outputs': {},
            'path_name': 'folder_name',
            'script_source': 'UEsFBgAAAAAAAAAAAAAAAAAAAAAAAA==',
            'icon': None
        }
        with patch('os.listdir') as mocked_listdir:
            mocked_listdir.return_value = ['config.json']
            result = parse_template_files('worker_path', 'folder_name')

        self.assertEqual(result, expected_error_result)

    def test_parse_template_files_with_invalid_directory_raises_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError) as context:
            parse_template_files('invalid_directory', 'folder_name')

        self.assertEqual(str(context.exception), "[Errno 2] No such file or directory: 'invalid_directory/config/config.json'")

    ###############################################################################
    #  Update Template Test Case Implementation
    ###############################################################################
    def test_update_template_function_returns_expected_data(self):
        mock_json_content = '{"key1": "old value 1", "key2": "old value 2", "key3": "value 3"}'
        new_values = {'key1': 'new value 1', 'key2': 'new value 2'}
        keys_to_update = ['key1', 'key2']

        with patch('builtins.open', mock_open(read_data=mock_json_content)) as mocked_file:
            update_template('config.json', new_values, keys_to_update)
            mocked_file.assert_called_once_with('config.json', 'r+')
            file_handle = mocked_file()

            file_handle.truncate.assert_called_once()

    def test_update_template_function_with_invalid_path_raises_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError) as context:
            update_template('invalid_path.json', {'key': 'value'}, ['key'])

        self.assertEqual(str(context.exception), "[Errno 2] No such file or directory: 'invalid_path.json'")

    def test_update_template_function_with_invalid_new_values_raises_type_error(self):
        mock_json_content = '{"key1": "value1", "key2": "value2"}'

        with patch('builtins.open', mock_open(read_data=mock_json_content)) as mocked_file:
            with self.assertRaises(TypeError) as context:
                update_template('config.json', 1, ['key1', 'key2'])
                mocked_file.assert_called_once_with('config.json', 'r+')
                file_handle = mocked_file()
                file_handle.truncate.assert_called_once()

        self.assertEqual(str(context.exception), "'int' object is not subscriptable")
