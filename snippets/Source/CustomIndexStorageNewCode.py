custom_index_output: BaseDict = None
storage_settings: BaseDict = None

output_custom_index: CustomIndex = None

def _initialize_output_custom_index(self) -> None:
    """
    Initializes a `Custom Index` object with form data and default fallback values.
    """
    self.output_custom_index = CustomIndex(**self.custom_index_output)

def _finalize_output_custom_index(self) -> None:
    """
    Finalizes a `Custom Index` object filling data and stores it accordingly.
    """
    self.output_custom_index.data = __DATA__
    self.output_custom_index = CustomIndex.script.storage(self.output_custom_index, self.storage_settings)
