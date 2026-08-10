custom_indexes_query_list: list[BaseDict] = None

custom_indexes: list[CustomIndex] = None

def _retrieve_custom_indexes(self) -> None:
    """
    Fetches the `Custom Indexes` objects from the backend based on a list of input parameters.
    """
    custom_indexes_variant_list: list[str] = [entity.variant for entity in self.inputs_info.custom_indexes_query_list]

    self.custom_indexes = CustomIndex.script.fetch_multi(self.custom_indexes_query_list, custom_indexes_variant_list)

    if not self.custom_indexes:
        raise WorkerError('Custom Index(es) not found')
