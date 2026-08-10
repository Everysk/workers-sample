user_app_query: str | BaseDict | list[str] = None

user_app: UserApp = None

def _retrieve_user_app(self) -> None:
    """
    Fetches the `User App` object from the backend based on input parameters.
    """
    user_app_variant: str = self.inputs_info.user_app_query.variant

    self.user_app = UserApp.script.fetch(self.user_app_query, user_app_variant)

    if not self.user_app:
        raise WorkerError('User App not found')
