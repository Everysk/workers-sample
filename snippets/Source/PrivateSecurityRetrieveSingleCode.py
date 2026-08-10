private_security_query: str | BaseDict | list[str] = None

private_security: PrivateSecurity = None

def _retrieve_private_security(self) -> None:
    """
    Fetches the `Private Security` object from the backend based on input parameters.
    """
    private_security_variant: str = self.inputs_info.private_security_query.variant

    self.private_security = PrivateSecurity.script.fetch(self.private_security_query, private_security_variant)

    if not self.private_security:
        raise WorkerError('Private Security not found')
