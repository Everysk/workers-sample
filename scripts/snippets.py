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
import json

###############################################################################
# Globals
###############################################################################
BASE_DIR = 'snippets'
VS_CODE = '.vscode'

###############################################################################
# Functions
###############################################################################

def read_json_file(path: str) -> dict:
    """
    Reads a JSON file from the given path and returns its contents as a dictionary.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file.
    """
    with open(path, '+r') as file:
        json_str: str = file.read()
        return json.loads(json_str)

def read_python_file(path: str) -> str:
    """
    Reads a python file from the given path and returns its contents as a string.

    Args:
        path (str): The path to the python file.

    Returns:
        str: The contents of the python file.
    """
    with open(path, '+r') as file:
        return file.read()

def read_file(path: str, file_type: str) -> dict | str:
    """
    Reads a file based on its type and returns its contents.

    Args:
        path (str): The path to the file.
        file_type (str): The type of the file (either 'py' or 'json').

    Returns:
        dict | str: The contents of the file.
    """
    out: str | dict = None

    match file_type:
        case 'py':
            out = read_python_file(path)
        case 'json':
            out = read_json_file(path)

    return out

def parse_python_file(snippet_name: str, python_code: str) -> dict:
    """
    Creates a VS Code snippet template from Python code.

    Args:
        snippet_name (str): The name of the snippet.
        python_code (str): The Python code to be converted into a snippet.

    Returns:
        dict: A dictionary representing the VS Code snippet.
    """
    body: list = python_code.splitlines()

    return {
        'prefix': snippet_name,
        'scope': 'python',
        'body': body
    }

def parse_json_file(snippet_name: str, json_dict: dict) -> dict:
    """
    Creates a VS Code snippet template from a JSON dictionary.

    Args:
        snippet_name (str): The name of the JSON file.
        json_dict (dict): The JSON dictionary containing snippet information.

    Returns:
        dict: A dictionary representing the VS Code snippet.
    """
    if not isinstance(json_dict['body'], list):
        json_dict['body'] = [json_dict['body']]

    body: list = []
    for index, _json in enumerate(json_dict['body']):
        json_str: str = json.dumps(_json, indent=2)
        lines: list = json_str.splitlines()

        if index + 1 < len(json_dict['body']):
            lines[-1] += ','
        body.extend(lines)

    return {
        'prefix': json_dict.get('prefix', snippet_name),
        'scope': json_dict.get('scope', 'json,jsonl,jsonc'),
        'description': json_dict.get('description', ''),
        'body': body
    }

def parse_file(snippet_name: str, file_data: str | dict, file_type: str) -> dict:
    """
    Parses a file and creates a VS Code snippet template.

    Args:
        snippet_name (str): The name of the snippet.
        file_data (str | dict): The contents of the file.
        file_type (str): The type of the file (either 'py' or 'json').

    Returns:
        dict: A dictionary representing the VS Code snippet.
    """
    out: str | dict = None

    match file_type:
        case 'py':
            out = parse_python_file(snippet_name, file_data)
        case 'json':
            out = parse_json_file(snippet_name, file_data)

    return out

def create_snippet_dict(file_list: list[str]) -> dict:
    """
    Creates a dictionary of VS Code snippets from a list of JSON files.

    Args:
        file_list (list[str]): A list of JSON file names.

    Returns:
        dict: A dictionary containing the VS Code snippets.
    """
    out: dict = {}

    for file in file_list:
        file_name: str = os.path.split(file)[1]
        snippet_name, file_type = file_name.split('.')
        file_data: dict = read_file(file, file_type)
        out[snippet_name] = parse_file(snippet_name, file_data, file_type)

    return out

def list_files(base_path: str) -> list[str]:
    """
    Recursively lists all files in a given directory and its subdirectories.

    Args:
        base_path (str): The base directory path from which to list files.

    Returns:
        list[str]: A list of paths to all files found within the base directory and its subdirectories.
    """
    path_list = os.listdir(base_path)

    files_path_list: list[str] = []
    for path in path_list:
        new_path = os.path.join(base_path, path)
        if os.path.isdir(new_path):
            files_path_list.extend(list_files(new_path))
            continue
        files_path_list.append(new_path)
    return files_path_list

def main():
    """
    Main function that generates VS Code snippets from JSON files in the BASE_DIR.
    """
    file_list: list[str] = list_files(BASE_DIR)

    snippets_name: str = os.path.join(VS_CODE, 'everysk.code-snippets')

    with open(snippets_name, 'w') as snippets_file:
        json_dict: dict = create_snippet_dict(file_list)
        snippets_file.write(json.dumps(json_dict, indent=2))

if __name__ == '__main__':
    main()
