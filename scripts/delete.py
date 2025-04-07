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
import requests

from scripts.helpers import get_folder_names, load_env, get_header, get_base_url, BASE_DIR

###############################################################################
# Functions
###############################################################################
def get_template_id(worker_path: str) -> str:
    """
    Retrieves the ID of the template from the `config.json` file.
    The function opens the `config.json` file, parses it as JSON and extracts the value associated with the `id` key.

    Args:
        worker_path (str): The string representing the path to the directory containing the configuration file.

    Usage:
        >>> from scripts.delete import get_template_id
        >>> get_template_id('worker')
        'worker_template_12345'

    Raises:
        FileNotFoundError: When `worker_path` argument does not match any file or directory or `config.json` simply does not exist.

    Returns:
        str: The extracted value associated with the key `id` from the dictionary `worker_template`.
    """
    template_path = os.path.join(worker_path, 'config', 'config.json')
    with open(template_path, 'r') as template_file:
        worker_template = json.load(template_file)
        template_id = worker_template['id']

    return template_id

def http_request(template_id: str,) -> None:
    """
    This function sends a DELETE request to a specific endpoint to delete a worker_template by its ID.
    The function constructs the request using authentication credentials from the environment variables.

    Args:
        template_id (str): The ID used for the deletion of the worker template.

    Usage:
        >>> from scripts.delete import http_request
        >>> http_request('wrkt_12345')
        'Successfuly deleted worker template'
    """
    headers = get_header()
    url = f'{get_base_url()}/{template_id}'
    answer = requests.delete(url, headers=headers)
    status_code = answer.status_code

    if status_code == 200:
        answer_json = answer.json()
        message = answer_json['worker_template']
        print(f'Successfuly deleted worker template {message}')
    else:
        print(f'Failed to delete {template_id}')
        print(answer.text)

    return

###############################################################################
# Scripts
###############################################################################
def main():
    """
    Execute the main routine for processing worker templates based on command-line arguments.

    This script expects a single command-line argument: the "template id" of a worker or "all" to process all workers.
    - If "all" is specified, the function retrieves all worker template IDs from a remote API, compares them with locally stored IDs,
      and performs HTTP requests for any IDs not present locally.
    - If a specific "template id" is given, it performs an HTTP request for that ID.

    Usage:
        >>> python script_name.py all
            - Retrieves all worker templates for the remote API, updating missing or outdated templates.
        >>> python script_name.py <template_id>
            - Processes a specific worker template by its ID.
    """
    if len(sys.argv) != 2:
        print('Enter the "template id" of the worker or "all" for all workers.')
        sys.exit(1)

    input_string = sys.argv[1]

    if input_string == 'all':
        all_ids = []

        headers = get_header()
        url = get_base_url()
        answer = requests.get(url, headers=headers)
        if answer.status_code != 200:
            print('Error retrieving all worker template ids.')
        else:
            all_ids = [w_t['id'] for w_t in answer.json()['worker_templates']]
        if not all_ids:
            sys.exit(1)

        folder_names = get_folder_names('all')
        local_template_ids = []
        for folder_name in folder_names:
            worker_path = os.path.join(BASE_DIR, folder_name)
            template_id = get_template_id(worker_path)
            if template_id:
                local_template_ids.append(template_id)

        for id in all_ids:
            if id not in local_template_ids:
                http_request(id)

    else:
        http_request(input_string)


if __name__ == '__main__':
    # Load environment variables
    load_env()
    main()
