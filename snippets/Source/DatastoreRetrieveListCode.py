datastores_query: str | BaseDict | list[str] = None
datastores_query_workspace: str = None

datastores: list[Datastore] = None

def _retrieve_datastores(self) -> None:
    """
    Fetches the `Datastores` objects from the backend based on input parameters.
    """
    datastores_variant: str = self.inputs_info.datastores_query.variant
    datastores_workspace: str = self.datastores_query_workspace or self.workspace

    self.datastores = Datastore.script.fetch_list(self.datastores_query, datastores_variant, datastores_workspace)

    if not self.datastores:
        raise WorkerError('Datastore(s) not found')
