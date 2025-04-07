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
from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock

from scripts.delete import get_template_id, http_request

###############################################################################
#  Delete Test Case Implementation
###############################################################################
class DeleteTestCase(TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"id": "1234"}')
    @patch('os.path.join')
    def test_get_template_id_returns_expected_data(self, mock_os_join, mock_file):
        mock_os_join.return_value = 'test_worker/config.json'
        expected_template_id = '1234'
        template_id = get_template_id('test_worker')

        mock_os_join.assert_called_with('test_worker', 'config', 'config.json')
        mock_file.assert_called_with('test_worker/config.json', 'r')
        self.assertEqual(template_id, expected_template_id)

    @patch('builtins.open', new_callable=mock_open, read_data='{"id": "1234"}')
    @patch('os.path.join')
    def test_get_template_id_with_wrong_id_returns_error(self, mock_os_join, mock_file):
        mock_os_join.return_value = 'test_worker/config.json'
        expected_template_id = '12345'
        template_id = get_template_id('test_worker')

        mock_os_join.assert_called_with('test_worker', 'config', 'config.json')
        mock_file.assert_called_with('test_worker/config.json', 'r')
        self.assertNotEqual(template_id, expected_template_id)

    def test_get_template_id_raises_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError):
            get_template_id('test_worker')

    def test_get_template_id_with_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            get_template_id(1234)

    ###############################################################################
    #  HTTP Request Test Case Implementation
    ###############################################################################
    @patch('requests.delete')
    def test_delete_http_request_returns_expected_data(self, mock_delete):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'worker_template': '12345_worker_template'}
        mock_delete.return_value = mock_response
        expected_output = 'Successfuly deleted worker template 12345_worker_template'

        with patch('builtins.print') as mocked_print:
            http_request('12345_worker_template')
            mocked_print.assert_called_with(expected_output)

    @patch('requests.delete')
    def test_delete_http_request_method_when_status_code_is_different_than_200(self, mock_delete):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.template_id = '12345_worker_template'
        mock_response.text = f'Failed to delete {mock_response.template_id}'
        mock_delete.return_value = mock_response
        expected_output_error = 'Failed to delete 12345_worker_template'

        with patch('builtins.print') as mocked_print:
            http_request('12345_worker_template')
            mocked_print.assert_called_with(expected_output_error)
