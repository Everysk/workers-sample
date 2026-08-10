from everysk.sdk.entities.tags import Tags

private_security_output: BaseDict = None
storage_settings: BaseDict = None

output_private_security: PrivateSecurity = None

def _initialize_output_private_security(self) -> None:
    """
    Initializes a `Private Security` object with form data and reference entity fallback values.
    """
    self.output_private_security = PrivateSecurity(**self.private_security)

    self.output_private_security.update({
        'name': self.private_security_output.name or self.private_security.name,
        'currency': self.private_security_output.currency or self.private_security.currency,
        'instrument_type': self.private_security_output.instrument_type or self.private_security.instrument_type,
        'tags': Tags.unify(self.private_security_output.tags, self.private_security.tags),
    })

def _finalize_output_private_security(self) -> None:
    """
    Finalizes a `Private Security` object filling data and stores it accordingly.
    """
    self.output_private_security.data = __DATA__
    self.output_private_security = PrivateSecurity.script.storage(self.output_private_security, self.storage_settings)
