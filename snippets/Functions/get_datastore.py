def get_datastore(self, datastore_form_id: str, datastore_form_name: str) -> Datastore:
    datastore_query: BaseDict | str = self.script_inputs.get(datastore_form_id)
    datastore_variant: str = self.inputs_info.get(datastore_form_id).variant
    workspace = datastore_form_id + '_workspace'
    datastore_workspace: str = self.script_inputs.get(workspace) or self.workspace

    datastore: Datastore = Datastore.script.fetch(datastore_query, datastore_variant, datastore_workspace)
    if not datastore:
        raise WorkerError('No %s found' % datastore_form_name)

    return datastore
