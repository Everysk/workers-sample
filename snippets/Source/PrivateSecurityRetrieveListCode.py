private_securities_query: str | BaseDict | list[str] = None

private_securities: list[PrivateSecurity] = None

def _retrieve_private_securities(self) -> None:
    """
    Fetches the `Private Securities` objects from the backend based on input parameters.
    """
    private_securities_variant: str = self.inputs_info.private_securities_query.variant

    self.private_securities = PrivateSecurity.script.fetch_list(self.private_securities_query, private_securities_variant)

    if not self.private_securities:
        raise WorkerError('Private Security(es) not found')
