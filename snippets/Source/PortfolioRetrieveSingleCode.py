portfolio_query: str | BaseDict | list[str] = None
portfolio_query_workspace: str = None

portfolio: Portfolio = None

def _retrieve_portfolio(self) -> None:
    """
    Fetches the `Portfolio` object from the backend based on input parameters.
    """
    portfolio_variant: str = self.inputs_info.portfolio_query.variant
    portfolio_workspace: str = self.portfolio_query_workspace or self.workspace

    self.portfolio = Portfolio.script.fetch(self.portfolio_query, portfolio_variant, portfolio_workspace)

    if not self.portfolio:
        raise WorkerError('Portfolio not found')
