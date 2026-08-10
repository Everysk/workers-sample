from everysk.sdk.entities import Secrets

def _get_secrets__FIELD_ID_(self) -> None:
    """
    Normalize and validate the secret value for `_FIELD_ID_`.

    This method retrieves the appropriate variant from the input configuration
    and normalizes the secret using `Secrets.script.normalize`. The normalized
    value is stored in `self._FIELD_ID_`. If the resulting value is missing or
    empty, a `WorkerError` is raised since this field is mandatory.

    Raises:
        WorkerError: If the normalized secret value is missing or empty.
    """
    _FIELD_ID__variant: str = self.inputs_info._FIELD_ID_.variant
    self._FIELD_ID_: str = Secrets.script.normalize(self._FIELD_ID_, _FIELD_ID__variant)

    if not self._FIELD_ID_:
        raise WorkerError(f'Missing mandatory field `_FIELD_ID_`')
