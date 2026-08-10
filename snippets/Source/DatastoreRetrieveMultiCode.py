datastores_query_list: list[BaseDict] = None

datastores: list[Datastore] = None

def _retrieve_datastores(self) -> None:
    """
    Fetches the `Datastores` objects from the backend based on a list of input parameters.
    """
    datastores_query_list: list[str | BaseDict] = [entity.datastores_query for entity in self.datastores_query_list]
    datastores_variant_list: list[str] = [entity.datastores_query.variant for entity in self.inputs_info.datastores_query_list]
    datastores_workspace_list: list[str] = [entity.datastores_query_workspace or self.workspace for entity in self.datastores_query_list]

    self.datastores = Datastore.script.fetch_multi(datastores_query_list, datastores_variant_list, datastores_workspace_list)

    if not self.datastores:
        raise WorkerError('Datastore(s) not found')
