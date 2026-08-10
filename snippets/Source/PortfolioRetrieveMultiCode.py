portfolios_query_list: list[BaseDict] = None

portfolios: list[Portfolio] = None

def _retrieve_portfolio(self) -> None:
    """
    Fetches the `Portfolios` objects from the backend based on a list of input parameters.
    """
    portfolio_query_list: list[str | BaseDict] = [entity.portfolio_query for entity in self.portfolio_query_list]
    portfolios_variant_list: list[str] = [entity.portfolio_query.variant for entity in self.inputs_info.portfolio_query_list]
    portfolios_workspace_list: list[str] = [entity.portfolio_query_workspace or self.workspace for entity in self.portfolio_query_list]

    self.portfolios = Portfolio.script.fetch_multi(portfolio_query_list, portfolios_variant_list, portfolios_workspace_list)

    if not self.portfolios:
        raise WorkerError('Portfolio(s) not found')
