datastore_query: str | BaseDict | list[str] = None
datastore_query_workspace: str = None

datastore: Datastore = None

def _retrieve_datastore(self) -> None:
    """
    Fetches the `Datastore` object from the backend based on input parameters.
    """
    datastore_variant: str = self.inputs_info.datastore_query.variant
    datastore_workspace: str = self.datastore_query_workspace or self.workspace

    self.datastore = Datastore.script.fetch(self.datastore_query, datastore_variant, datastore_workspace)

    if not self.datastore:
        raise WorkerError('Datastore not found')
