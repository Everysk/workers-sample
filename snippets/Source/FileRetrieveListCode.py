import base64
import six

files_query: str | BaseDict | list[str] = None
files_query_workspace: str = None

files: list[File] = None

def _from_base_64(self, file_data: str) -> str:
    """
    Decodes the base 64 string data to normal sting.
    Args:
        file_data (str or bytes): The input data to be decoded. This can be a string or bytes.

    Returns:
        str: The decoded version of the input data as a string.
    """
    return six.ensure_str(base64.b64decode(six.ensure_str(file_data)))

def _retrieve_files(self) -> None:
    """
    Fetches the `Files` objects from the backend based on input parameters.
    """
    files_variant: str = self.inputs_info.files_query.variant
    files_workspace: str = self.files_query_workspace or self.workspace

    self.files = File.script.fetch_list(self.files_query, files_variant, files_workspace)

    if not self.files:
        raise WorkerError('File(s) not found')

    for file in self.files:
        file.data = self._from_base_64(file.data)
