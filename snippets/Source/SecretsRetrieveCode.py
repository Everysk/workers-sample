from everysk.sdk.entities import Secrets

def _get_secrets(self, value, variant, mandatory=True, field_name=None) -> str:
    """
    Normalize and retrieve a secret value.

    This method normalizes a secret using `Secrets.script.normalize` and optionally
    enforces that the result is non-empty. If the secret is mandatory and the normalized
    value is empty or missing, a `WorkerError` is raised. When `field_name` is provided,
    it is included in the error message for clearer diagnostics.

    Args:
        value: The raw input value to be normalized as a secret.
        variant: The normalization variant or format to apply.
        mandatory (bool, optional): Whether the secret is required. Defaults to True.
        field_name (str, optional): Optional field name used to enrich the error message.

    Returns:
        str: The normalized secret value.

    Raises:
        WorkerError: If the secret is mandatory but missing after normalization.
    """
    secret_value: str = Secrets.script.normalize(value, variant)

    if mandatory and not secret_value:
        error_msg: str = 'Missing mandatory field'

        if field_name is not None:
            error_msg = '{error_msg} `{field_name}`'

        raise WorkerError(error_msg)

    return secret_value
