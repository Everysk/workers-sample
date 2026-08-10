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
import sys
import os
import json
import re
import requests
import base64

from everysk.core.compress import zip_directory_to_str
from scripts.helpers import get_folder_names, load_env, get_header, get_base_url, BASE_DIR

###############################################################################
# Functions
###############################################################################
def find_substring(string: str, start_index: int, substring: str) -> int:
    """
    The function is designed to find the position of a specified substring within a string, starting the search from a given index.
    Then, it returns the position of the substring.

    Args:
        string (str):
            The string where the search will be perfomed.

        start_index (int):
            The index from which the search should start.

        substring (str):
            The string segment to search for based on the `string` argument.

    Usage:
        >>> from scripts.deploy import find_substring
        >>> find_substring('hello world', 1, 'world')
        5

        Since the starting index is after the substring `hello` it will return -1
        >>> find_substring('hello world', 6, 'hello)
        -1

    Returns:
        int: The index of the first occurance that matches the substring. If the substring is not found, returns -1
    """
    try:
        return string[start_index:].index(substring)
    except ValueError:
        return -1

def remove_comments(json_str: str) -> str:
    """
    Removes single line comment and block comments

    Args:
        json_str (str): A string containing the JSON data with or without single line or block comments.

    Usage:
        >>> from deploy import remove_comments
        >>> example_json = '''
        ... {
        ...    "key": "value", // This is a single line comment
        ...    "number": 1 /* This is a block comment */
        ... }
        ... '''

        >>> print(remove_comments(example_json))
        {
            "key": "value",
            "number": 1
        }

    Returns:
        str: The JSON string with all comments removed.
    """
    json_str = re.sub(r'//.*?\n', '\n', json_str)
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
    return json_str

def get_icon(worker_template: dict, worker_path: str) -> str:
    """
    Retrieves an icon for a worker.

    This function searches for an SVG icon in the specified `worker_path` directory.
    If an SVG file is found, it encodes the file in Base64 and returns it as a string
    prefixed with "data:image/svg+xml;base64," for rendering in the front end.
    If no SVG file is found, it falls back to the `icon` key from the provided
    `worker_template` dictionary.

    Args:
        worker_template (dict): A dictionary containing worker attributes, including a fallback icon under the 'icon' key.
        worker_path (str): The file path to the directory where the worker's icon file is expected to reside.

    Returns:
        str: A Base64-encoded string of the SVG icon prefixed for rendering, or the fallback icon from the `worker_template`.

    """
    icon_str = ''
    base_path = os.path.join(worker_path, 'config')

    if 'icon.svg' in os.listdir(base_path):
        icon_path = os.path.join(base_path, 'icon.svg')
        with open(icon_path, 'rb') as icon_file:
            icon_data = icon_file.read()
            icon_str = base64.b64encode(icon_data).decode('utf-8')

    return icon_str or worker_template.get('icon')


def read_file(worker_path: str, is_remove_comments: bool = False, is_json: bool = True) -> str:
    data = ''
    with open(worker_path, 'r') as template_file:
        data = remove_comments(template_file.read()) if is_remove_comments else template_file.read()
    return json.loads(data) if is_json else data

def parse_template_files(worker_path: str, folder_name: str) -> dict:
    """
    Parses configuration and code files related to a worker located in a specified dictionary,
    constructing a comprehensive dictionary that represents the worker template.

    It processes a main config file (`config.json`), input/output specifications (`form_inputs.json` and `form_outputs.json`), and additional Python and Markdown files.
    It takes all the data from these files and puts into a structured dictionary. If a Python file named `form_functions.py` exists it creates the dictionary.

    Args:
        worker_path (str):
            The file path to the directory containing the worker's files.

    Returns:
        dict: A dictionary containing:
            - 'status': 'OK' if processing is successful, 'ERROR' otherwise.
            - 'message': saying if the worker template was created or if the file `config.json` is empty
            - 'worker_template': The dictionary containing the parsed data from all the files.
    """
    config_path = os.path.join(worker_path, 'config')
    worker_template = {}
    worker_template.update(read_file(os.path.join(config_path, 'config.json'), is_remove_comments=True))

    worker_template.update({
        'form_inputs': read_file(os.path.join(config_path, 'form_inputs.json'), is_remove_comments=True),
        'form_outputs': read_file(os.path.join(config_path, 'form_outputs.json'), is_remove_comments=True),
        'form_functions': {'source_code': read_file(os.path.join(config_path, 'form_functions.py'), is_json=False)},
        'description': read_file(os.path.join(worker_path, 'README.md'), is_remove_comments=False, is_json=False),
        'script_source': zip_directory_to_str([worker_path, 'workers/libs'], path_name_list=[folder_name, 'libs'], ignore_files=['config.json'], ignore_roots=['**/tests*']),
        'icon': get_icon(worker_template, worker_path),
        'path_name': folder_name
    })
    return worker_template

def update_template(template_path: str, template: str, keys: list) -> None:
    """
    Updates specific keys in a JSON file located at a given path.
    This functions opens a JSON File in read+write mode

    Args:
        template_path (str):
            The file path to the JSON template that needs updating

        template (str):
            A dictionary containing the new values for the keys

        keys (list):
            A list of keys present in the template dictionary whose value should be updated in the JSON file.

    Usage:
        >>> from scripts.deploy import update_template
        >>> template_path = '/path/to/config.json'
        >>> new_values = {'key1': 'new value 1', 'key2': 'new value 2'}
        >>> keys_to_update = ['key1', 'key2']
        >>> update_template(template_path, new_values, keys_to_update)
    """
    with open(template_path, 'r+') as template_file:
        json_str = remove_comments(template_file.read())
        worker_template = json.loads(json_str)
        for key in keys:
            worker_template[key] = template[key]
        template_file.seek(0)
        json.dump(worker_template, template_file, indent=2)
        template_file.truncate()

def http_request(worker_template: dict, method: str, url: str) -> tuple:
    """
    Send an HTTP request for a worker template with specified HTTP method and URL.
    The function handles the request with authorization headers using API credentials from settings.

    Args:
        worker_template (dict):
            The data of the worker template to be sent as the request payload.
            It should contain necessary worker template details as a dictionary.

        method (str):
            The HTTP method to be used for the request.

        url (str):
            The endpoint URL where the HTTP request will be sent.

    Usage:
        >>> from scripts.deploy import http_request
        >>> worker_template = {"id": 123, "name": "Sample Worker"}
        >>> method = 'POST'
        >>> url = 'https://api.everysk.com/v2/worker_templates'
        >>> http_request(worker_template, method, url)

    Returns:
        tuple: Tuple containg 'status_code', 'message', and 'new_worker_template' once the request is completed.
    """
    headers = get_header()
    answer = requests.request(method, url, headers=headers, json=worker_template)
    status_code = answer.status_code

    if status_code == 200:
        message = 'Successful request operation.'
        new_worker_template = answer.json()['worker_template']
    else:
        message = f'Error on http_request: {answer.text}'
        new_worker_template = {}

    return (status_code, message, new_worker_template)

################################################################################
# Scripts
################################################################################
def main():
    """
    Deploy worker templates to a specified location.

    The following scripts handles the deployment of worker templates by either updating an existent template or creating a new one.
    The script expects a single command line argument that determines the target folder for deployment.
    If the command-line argument is not valid, or the specified folder does not exists, the scripts returns an error.

    Usage:
        Run the script from the command line providing the folder name as an argument.
        >>> python deploy.py <folder_name>
    """
    if len(sys.argv) != 2:
        print('Invalid argument. Usage: run.py deploy <folder_name|all>')
        sys.exit(1)

    input_string = sys.argv[1]

    folder_names = get_folder_names(input_string)

    if not folder_names:
        print(f'No matching worker folder found for "{input_string}".')
        sys.exit(1)

    # 'libs' holds shared code, it is not a worker so it must not be deployed.
    excluded_folders = {'libs'}
    for folder_name in folder_names:
        if folder_name in excluded_folders:
            continue

        worker_path = os.path.join(BASE_DIR, folder_name)

        worker_template = parse_template_files(worker_path, folder_name)

        # Check if the worker already exists to decide if create (POST) or update (PUT) the worker template
        worker_template_id = worker_template['id']
        base_url = get_base_url()
        method, url = ('PUT', f'{base_url}/{worker_template_id}') if worker_template_id else ('POST', base_url)
        status_code, message, new_worker_template = http_request(worker_template, method, url)

        print(message)

        template_path = os.path.join(worker_path, 'config', 'config.json')
        keys = []
        # Only a newly created worker (POST) writes anything back: the platform-minted
        # id plus its timestamps and icon. Updates (PUT) must NOT touch config.json, so
        # that a config.json diff means exactly "a new worker was created".
        if method == 'POST' and status_code == 200:
            keys = ['id', 'updated', 'created', 'icon']

        if keys:
            update_template(template_path, new_worker_template, keys)
            print(f"{new_worker_template['name']} config.json updated successfully.")

if __name__ == '__main__':
    # Load environment variables
    load_env()
    main()
