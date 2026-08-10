# Imports
import base64
import six

# Function
def _from_base_64(self, file_data: str) -> str:
    """
    Decodes the base 64 string data to normal sting.
    Args:
        file_data (str or bytes): The input data to be decoded. This can be a string or bytes.

    Returns:
        str: The decoded version of the input data as a string.
    """
    return six.ensure_str(base64.b64decode(six.ensure_str(file_data)))
