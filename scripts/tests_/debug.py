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
import asyncio
import json
from unittest import TestCase
from unittest.mock import patch, MagicMock, mock_open

from scripts.debug import run_maybe_async, main

###############################################################################
# Debug Test Case Implementation
###############################################################################
class DebugTestCase(TestCase):

    def test_run_maybe_async_with_sync_function_returns_result(self):
        def sync_func():
            return 'sync_result'
        result = run_maybe_async(sync_func)
        self.assertEqual(result, 'sync_result')

    def test_run_maybe_async_with_async_function_returns_result(self):
        async def async_func():
            return 'async_result'
        result = run_maybe_async(async_func)
        self.assertEqual(result, 'async_result')

    def test_run_maybe_async_handles_running_event_loop(self):
        async def async_func():
            return 'async_result'

        with patch('asyncio.run', side_effect=RuntimeError("asyncio.run() cannot be called from a running event loop")), \
             patch('asyncio.get_event_loop') as mock_get_loop:
            mock_loop = MagicMock()
            mock_loop.run_until_complete.return_value = 'async_result'
            mock_get_loop.return_value = mock_loop

            result = run_maybe_async(async_func)

        self.assertEqual(result, 'async_result')
        mock_loop.run_until_complete.assert_called_once()

    def test_run_maybe_async_reraises_other_runtime_errors(self):
        async def async_func():
            return 'result'

        with patch('asyncio.run', side_effect=RuntimeError("some other error")):
            with self.assertRaises(RuntimeError) as ctx:
                run_maybe_async(async_func)
        self.assertEqual(str(ctx.exception), "some other error")

    def test_main_exits_when_wrong_number_of_args(self):
        with patch('sys.argv', ['debug.py']):
            with self.assertRaises(SystemExit) as ctx:
                main()
        self.assertEqual(ctx.exception.code, 1)

    def test_main_exits_when_invalid_folder_name(self):
        with patch('sys.argv', ['debug.py', 'non_existent_folder', 'key']), \
             patch('scripts.debug.get_folder_names', return_value=[]), \
             patch('builtins.print'):
            with self.assertRaises(SystemExit) as ctx:
                main()
        self.assertEqual(ctx.exception.code, 1)

    def test_main_raises_when_no_main_function(self):
        mock_module = MagicMock()
        mock_module.main = None
        sample_args = json.dumps({'key': {}})
        with patch('sys.argv', ['debug.py', 'wk_foo', 'key']), \
             patch('scripts.debug.get_folder_names', return_value=['wk_foo']), \
             patch('os.path.join', return_value='workers/wk_foo/config/sample_args.json'), \
             patch('builtins.open', mock_open(read_data=sample_args)), \
             patch('importlib.import_module', return_value=mock_module), \
             patch('scripts.debug.handler_input_args', return_value={}):
            with self.assertRaises(RuntimeError):
                main()

    def test_main_executes_worker_and_prints_result(self):
        mock_module = MagicMock()
        mock_module.main.return_value = {'output': 'data'}
        sample_args = json.dumps({'key': {'field': 'value'}})
        with patch('sys.argv', ['debug.py', 'wk_foo', 'key']), \
             patch('scripts.debug.get_folder_names', return_value=['wk_foo']), \
             patch('os.path.join', return_value='workers/wk_foo/config/sample_args.json'), \
             patch('builtins.open', mock_open(read_data=sample_args)), \
             patch('importlib.import_module', return_value=mock_module), \
             patch('scripts.debug.handler_input_args', return_value={'field': 'value'}):
            main()
        mock_module.main.assert_called_once()
