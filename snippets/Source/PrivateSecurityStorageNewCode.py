private_security_output: BaseDict = None
storage_settings: BaseDict = None

output_private_security: PrivateSecurity = None

def _initialize_output_private_security(self) -> None:
    """
    Initializes a `Private Security` object with form data and default fallback values.
    """
    self.output_private_security = PrivateSecurity(**self.private_security_output)

def _finalize_output_private_security(self) -> None:
    """
    Finalizes a `Private Security` object filling data and stores it accordingly.
    """
    self.output_private_security.data = __DATA__
    self.output_private_security = PrivateSecurity.script.storage(self.output_private_security, self.storage_settings)
