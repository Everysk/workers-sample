custom_indexes_query: str | BaseDict | list[str] = None

custom_indexes: list[CustomIndex] = None

def _retrieve_custom_indexes(self) -> None:
    """
    Fetches the `Custom Indexes` objects from the backend based on input parameters.
    """
    custom_indexes_variant: str = self.inputs_info.custom_indexes_query.variant

    self.custom_indexes = CustomIndex.script.fetch_list(self.custom_indexes_query, custom_indexes_variant)

    if not self.custom_indexes:
        raise WorkerError('Custom Index(es) not found')
