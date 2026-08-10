portfolios_query: str | BaseDict | list[str] = None
portfolios_query_workspace: str = None

portfolios: list[Portfolio] = None

def _retrieve_portfolios(self) -> None:
    """
    Fetches the `Portfolios` objects from the backend based on input parameters.
    """
    portfolios_variant: str = self.inputs_info.portfolios_query.variant
    portfolios_workspace: str = self.portfolios_query_workspace or self.workspace

    self.portfolios = Portfolio.script.fetch_list(self.portfolios_query, portfolios_variant, portfolios_workspace)

    if not self.portfolios:
        raise WorkerError('Portfolio(s) not found')
