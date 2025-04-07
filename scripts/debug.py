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
import os
import sys
import json
import importlib
from scripts.helpers import get_folder_names, load_env, BASE_DIR
from everysk.sdk.base import handler_input_args
###############################################################################
# Scripts
###############################################################################
def main():
    """
    Executes a worker function based on the 'folder name' and the 'sample args key'
    dynamically loads and executes a specific worker's `main` function based on inputs specified through command-line arguments.
    It requires two arguments: a folder name that identifies the worker and a key that specifies which arguments to use from the worker's `sample_args.json` file.

    Usage:
        Command line example for running the script:
        >>> python script_name.py <folder_name> sample_args_key
    """
    # add workers path to the system path

    sys.path.append(f'{os.getcwd()}/{BASE_DIR}')

    # Get the arguments from the command line
    args_ = sys.argv[1].split(' ')

    # Check if the arguments are valid
    if len(args_) != 2:
        print('Enter the "folder_name" and "sample_args_key" of the worker.')
        sys.exit(1)

    # folder_name
    input_string = args_[0]

    # sample_args_key
    sample_args_key = args_[1]

    # Get the folder names
    folder_names = get_folder_names(input_string)

    # Check if the folder name is valid
    if len(folder_names) != 1:
        print('Invalid argument, write your "folder name" to select all folders')
        sys.exit(1)

    worker_path = os.path.join(BASE_DIR, folder_names[0])

    template_path = os.path.join(worker_path, 'config', 'sample_args.json')
    with open(template_path, 'r') as template_file:
        sample_args = json.load(template_file)

    main = importlib.import_module(f'{BASE_DIR}.{folder_names[0]}.main').main
    result = main(handler_input_args(sample_args[sample_args_key]))

    print(f'Worker: {folder_names[0]} - Sample Args Key: {sample_args_key} - Result:')
    print(result)

if __name__ == '__main__':
    load_env()
    main()
