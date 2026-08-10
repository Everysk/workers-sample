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
from dotenv import load_dotenv

###############################################################################
# Globals
###############################################################################
BASE_DIR = 'workers'

###############################################################################
# Functions
###############################################################################
def get_folder_names(folder_name: str) -> list:
    """
    Get the folder names from the BASE_DIR.
    The functions searches the BASE_DIR for directories that match the given 'folder_name'.
    If `folder_name` is 'all', it returns names of all directories found.
    If a directory matches the `folder_name`, it returns a list containing only that directory name.
    If there is no match and `folder_name` is not 'all', it returns an empty list.

    Args:
        folder_name (str): The specific folder name to filter for or 'all' to get names of all directories in BASE_DIR.

    Usage:
        Get the name of a specific folder:
        >>> from scripts.helpers import get_folder_names
        >>> get_folder_names('specific_folder')

        Get the name of all folders
        >>> get_folder_names('all')

    Returns:
        list: A list containing the matched folders name(s). Returns all folder names if 'all' is specified
    """
    folder_names = [name for name in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, name))]
    if folder_name in folder_names:
        folder_names = [folder_name]
    elif folder_name != 'all':
        folder_names = []
    return folder_names

def get_header() -> dict:
    """
    Get the header for the HTTP request.
    The function constructs a dictionary containing the authorization header for the HTTP request.

    Usage:
        >>> from scripts.helpers import get_header
        >>> get_header()

    Returns:
        dict: The dictionary containing the authorization header.
    """
    return {
        'Authorization': f"Bearer {os.getenv('EVERYSK_API_SID')}:{os.getenv('EVERYSK_API_TOKEN')}",
        'Content-Type': 'application/json',
        'Everysk-Managed-Deploy': os.getenv('EVERYSK_MANAGED_DEPLOY', 'None')
    }

def get_base_url() -> str:
    """
    Get the base URL for the HTTP request.
    The function constructs the base URL for the HTTP request.

    Usage:
        >>> from scripts.helpers import get_base_url
        >>> get_base_url()

    Returns:
        str: The base URL for the HTTP request.
    """
    scheme = os.getenv('EVERYSK_API_URL_SCHEME', 'https')
    domain = os.getenv('EVERYSK_API_URL_DOMAIN', 'api.everysk.com')
    version = os.getenv('EVERYSK_API_VERSION', 'v2')

    return f'{scheme}://{domain}/{version}/worker_templates'

def load_env():
    """
    Load the environment variables from the .env file.
    """
    load_dotenv()
