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
from unittest.mock import patch

from scripts.venv import create_venv, install_requirements, print_activation_instructions

###############################################################################
# Venv Test Case Implementation
###############################################################################
class VenvTestCase(TestCase):

    @patch('subprocess.run')
    @patch('os.path.exists', return_value=False)
    def test_create_venv_when_not_exists_runs_subprocess(self, mock_exists, mock_subprocess):
        with patch('builtins.print'):
            create_venv()
        mock_subprocess.assert_called_once()

    @patch('os.path.exists', return_value=True)
    def test_create_venv_when_already_exists_prints_message(self, mock_exists):
        with patch('builtins.print') as mock_print:
            create_venv()
        mock_print.assert_called_with("⚡ Virtual environment already exists.")

    @patch('subprocess.run')
    @patch('os.path.exists', return_value=True)
    def test_install_requirements_when_file_exists_runs_pip(self, mock_exists, mock_subprocess):
        with patch('builtins.print'):
            install_requirements()
        mock_subprocess.assert_called_once()

    @patch('os.path.exists', return_value=False)
    def test_install_requirements_when_no_file_prints_warning(self, mock_exists):
        with patch('builtins.print') as mock_print:
            install_requirements()
        mock_print.assert_called_with("⚠️ No requirements.txt found, skipping dependency installation.")

    def test_print_activation_instructions_outputs_message(self):
        with patch('builtins.print') as mock_print:
            print_activation_instructions()
        mock_print.assert_called()
