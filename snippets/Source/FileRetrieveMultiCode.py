import base64
import six

files_query_list: list[BaseDict] = None

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
    Fetches the `Files` objects from the backend based on a list of input parameters.
    """
    files_query_list: list[str | BaseDict] = [entity.files_query for entity in self.files_query_list]
    files_variant_list: list[str] = [entity.files_query.variant for entity in self.inputs_info.files_query_list]
    files_workspace_list: list[str] = [entity.files_query_workspace or self.workspace for entity in self.files_query_list]

    self.files = File.script.fetch_multi(files_query_list, files_variant_list, files_workspace_list)

    if not self.files:
        raise WorkerError('File(s) not found')

    for file in self.files:
        file.data = self._from_base_64(file.data)
