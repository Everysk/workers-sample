###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

################################################################################
# Imports
################################################################################
import os

from unittest import TestCase
from unittest.mock import patch, call

from scripts.helpers import get_folder_names, get_header, get_base_url, load_env

################################################################################
# Helpers Test Case Implementation
################################################################################
class HelpersTestCase(TestCase):

    def test_get_folder_names_returns_expected_data(self):
        base_dir = 'thefolder'
        folder_names = ['folder1', 'folder2', 'folder3', 'folder4', 'folder5']

        with patch('os.listdir') as mock_listdir, patch('os.path.isdir') as mock_isdir, patch('os.path.join') as mock_join:
            mock_listdir.return_value = folder_names
            mock_join.return_value = f'{base_dir}/folder2'
            mock_isdir.return_value = True
            result = get_folder_names('folder2')

        self.assertEqual(result, ['folder2'])

    def test_get_folder_names_returns_empty_list_when_folder_name_is_different_than_all(self):
        result = get_folder_names('folder_name_is_not_all')

        self.assertEqual(result, [])

    def test_get_folder_names_raises_type_error_when_more_than_one_argument_is_passed(self):
        with self.assertRaises(TypeError) as context:
            get_folder_names('ender', 'ender')

        self.assertEqual(str(context.exception), 'get_folder_names() takes 1 positional argument but 2 were given')

    def test_get_folder_names_raises_type_error_when_no_argument_is_provided(self):
        with self.assertRaises(TypeError) as context:
            get_folder_names()

        self.assertEqual(str(context.exception), "get_folder_names() missing 1 required positional argument: 'folder_name'")

    def test_get_header_returns_expected_data(self):
        expected_header = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer sid:token',
            'Everysk-Managed-Deploy': 'Potato'
        }

        with patch('os.getenv') as mock_getenv:
            mock_getenv.side_effect = ['sid', 'token', 'Potato']
            header = get_header()

        self.assertEqual(header, expected_header)
        self.assertEqual(mock_getenv.call_count, 3)
        mock_getenv.assert_has_calls([
            call('EVERYSK_API_SID'),
            call('EVERYSK_API_TOKEN'),
            call('EVERYSK_MANAGED_DEPLOY', 'None')
        ])

    def test_get_base_url_returns_expected_data(self):
        expected_base_url = 'http://localhost:8000/v2/worker_templates'

        with patch('os.getenv') as mock_getenv:
            mock_getenv.side_effect = ['http', 'localhost:8000', 'v2']
            base_url = get_base_url()

        self.assertEqual(base_url, expected_base_url)
        self.assertEqual(mock_getenv.call_count, 3)
        mock_getenv.assert_has_calls([
            call('EVERYSK_API_URL_SCHEME', 'https'),
            call('EVERYSK_API_URL_DOMAIN', 'api.everysk.com'),
            call('EVERYSK_API_VERSION', 'v2')
        ])

    def test_load_env_calls_load_dotenv(self):
        with patch('scripts.helpers.load_dotenv') as mock_load_dotenv:
            load_env()
        mock_load_dotenv.assert_called_once()
