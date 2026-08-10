custom_index_query: str | BaseDict | list[str] = None

custom_index: CustomIndex = None

def _retrieve_custom_index(self) -> None:
    """
    Fetches the `Custom Index` object from the backend based on input parameters.
    """
    custom_index_variant: str = self.inputs_info.custom_index_query.variant

    self.custom_index = CustomIndex.script.fetch(self.custom_index_query, custom_index_variant)

    if not self.custom_index:
        raise WorkerError('Custom Index not found')
