user_apps_query: str | BaseDict | list[str] = None

user_apps: list[UserApp] = None

def _retrieve_user_apps(self) -> None:
    """
    Fetches the `User Apps` objects from the backend based on input parameters.
    """
    user_apps_variant: str = self.inputs_info.user_apps_query.variant

    self.user_apps = UserApp.script.fetch_list(self.user_apps_query, user_apps_variant)

    if not self.user_apps:
        raise WorkerError('User App(s) not found')
