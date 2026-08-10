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
# Imports
###############################################################################
from unittest import TestCase
from unittest.mock import patch, call

from scripts.create import create_folder_structure

###############################################################################
# Create Test Case Implementation
###############################################################################
class CreateTestCase(TestCase):

    @patch('shutil.copy2')
    @patch('os.path.isdir', return_value=False)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    @patch('os.listdir', return_value=['config.json', 'main.py'])
    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs')
    def test_create_folder_structure_with_template_copies_files(self, mock_makedirs, mock_exists, mock_listdir, mock_join, mock_isdir, mock_copy):
        with patch('builtins.print') as mock_print:
            create_folder_structure('my_worker')

        mock_makedirs.assert_called_once()
        self.assertEqual(mock_copy.call_count, 2)
        mock_print.assert_called_once()

    @patch('shutil.copytree')
    @patch('os.path.isdir', return_value=True)
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    @patch('os.listdir', return_value=['config'])
    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs')
    def test_create_folder_structure_with_template_copies_subdirs(self, mock_makedirs, mock_exists, mock_listdir, mock_join, mock_isdir, mock_copytree):
        with patch('builtins.print'):
            create_folder_structure('my_worker')

        mock_copytree.assert_called_once()

    @patch('os.path.exists', return_value=False)
    @patch('os.makedirs')
    def test_create_folder_structure_without_template_prints_error(self, mock_makedirs, mock_exists):
        with patch('builtins.print') as mock_print:
            create_folder_structure('my_worker')

        mock_print.assert_called_with("Error: Template directory does not exist.")
