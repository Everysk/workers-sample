from everysk.sdk.entities import Secrets

def _get_secrets_file__SECRETS_NAME_(self) -> None:
    """
    Retrieve and normalize the secret file value for `_SECRETS_NAME_`.

    This method resolves the appropriate variant and workspace for the secret,
    then normalizes the value using `Secrets.script.normalize`. If the resulting
    secret value is empty or missing, a `WorkerError` is raised since this field
    is mandatory.

    The normalized secret is stored in `self._SECRETS_NAME_`.

    Raises:
        WorkerError: If the secret value is missing or empty after normalization.
    """
    secrets_file_variant: str = self.inputs_info._SECRETS_NAME__query.variant
    secrets_file_workspace: str = self._SECRETS_NAME__query_workspace or self.workspace
    self._SECRETS_NAME_: str = Secrets.script.normalize(self._SECRETS_NAME__query, secrets_file_variant, workspace=secrets_file_workspace)

    if not self._SECRETS_NAME_:
        raise WorkerError(f'Missing mandatory field `_SECRETS_NAME_`')
