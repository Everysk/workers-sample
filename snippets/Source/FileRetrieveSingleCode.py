import base64
import six

file_query: str | BaseDict | list[str] = None
file_query_workspace: str = None

file: File = None

def _from_base_64(self, file_data: str) -> str:
    """
    Decodes the base 64 string data to normal sting.
    Args:
        file_data (str or bytes): The input data to be decoded. This can be a string or bytes.

    Returns:
        str: The decoded version of the input data as a string.
    """
    return six.ensure_str(base64.b64decode(six.ensure_str(file_data)))

def _retrieve_file(self) -> None:
    """
    Fetches the `File` object from the backend based on input parameters.
    """
    file_variant: str = self.inputs_info.file_query.variant
    file_workspace: str = self.file_query_workspace or self.workspace

    self.file = File.script.fetch(self.file_query, file_variant, file_workspace)

    if not self.file:
        raise WorkerError('File not found')

    self.file.data = self._from_base_64(self.file.data)
