import base64
import six

from everysk.sdk.entities.tags import Tags

file_output: BaseDict = None
storage_settings: BaseDict = None

output_file: File = None

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

def _initialize_output_file(self) -> None:
    """
    Initializes a `File` object with form data and reference entity fallback values.
    """
    self.output_file = File(**{
        'name': self.file_output.name or self.__REFERENCE_ENTITY__.name,
        'workspace': self.file_output.workspace or self.workspace,
        'content_type': self.file_output.content_type,
        'date': self.file_output.date or self.__REFERENCE_ENTITY__.date,
        'link_uid': self.file_output.link_uid or self.__REFERENCE_ENTITY__.link_uid,
        'tags': Tags.unify(self.file_output.tags, self.__REFERENCE_ENTITY__.tags),
    })

def _finalize_output_file(self) -> None:
    """
    Finalizes a `File` object filling data and stores it accordingly.
    """
    self.output_file.data = self._transform_file_data(__DATA__)
    self.output_file = File.script.storage(self.output_file, self.storage_settings)
