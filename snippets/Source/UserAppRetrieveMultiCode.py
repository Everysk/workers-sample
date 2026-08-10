user_apps_query_list: list[BaseDict] = None

user_apps: list[UserApp] = None

def _retrieve_user_apps(self) -> None:
    """
    Fetches the `User Apps` objects from the backend based on a list of input parameters.
    """
    user_apps_variant_list: list[str] = [entity.variant for entity in self.inputs_info.user_apps_query_list]

    self.user_apps = UserApp.script.fetch_multi(self.user_apps_query_list, user_apps_variant_list)

    if not self.user_apps:
        raise WorkerError('User App(s) not found')
