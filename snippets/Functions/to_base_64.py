# Imports
import base64
import six

# Function
def _to_base_64(self, data: str | bytes) -> str:
    """
    Converts the input data (string or bytes) to a Base64 encoded string.

    Args:
        data (str or bytes): The input data to be encoded. This can be a string or bytes.

    Returns:
        str: The Base64 encoded version of the input data as a string.
    """
    return six.ensure_str(base64.b64encode(six.ensure_binary(data)))

def _transform_file_data(self, file_data: str | bytes) -> str:
    """
    Transforms the input file data into a Base64 encoded string.

    If the input data is a string, it is first encoded as UTF-8 before being Base64 encoded.
    If encoding fails, the function assumes the input is already in bytes and attempts Base64 encoding directly.

    Args:
        file_data (str or bytes): The input file data to be transformed. Can be a string or bytes.

    Returns:
        str: The Base64 encoded version of the input file data as a string.
    """
    data = None
    try:
        data = self._to_base_64(file_data.encode('utf-8'))
    except:
        data = self._to_base_64(file_data)

    return data
