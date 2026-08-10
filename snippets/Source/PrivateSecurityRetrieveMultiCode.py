private_securities_query_list: list[BaseDict] = None

private_securities: list[PrivateSecurity] = None

def _retrieve_private_securities(self) -> None:
    """
    Fetches the `Private Securities` objects from the backend based on a list of input parameters.
    """
    private_securities_variant_list: list[str] = [entity.variant for entity in self.inputs_info.private_securities_query_list]

    self.private_securities = PrivateSecurity.script.fetch_multi(self.private_securities_query_list, private_securities_variant_list)

    if not self.private_securities:
        raise WorkerError('Private Security(es) not found')
