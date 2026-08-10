from everysk.core.datetime import Date

portfolio_output: BaseDict = None
storage_settings: BaseDict = None

output_portfolio: Portfolio = None

def _initialize_output_portfolio(self) -> None:
    """
    Initializes a `Portfolio` object with form data and default fallback values.
    """
    self.output_portfolio = Portfolio(**self.portfolio_output)
    self.output_portfolio.workspace = self.output_portfolio.workspace or self.workspace
    self.output_portfolio.date = self.output_portfolio.date or Date.today()

def _finalize_output_portfolio(self) -> None:
    """
    Finalizes a `Portfolio` object filling securities and stores it accordingly.
    """
    self.output_portfolio.securities = __SECURITIES__
    self.output_portfolio = Portfolio.script.storage(self.output_portfolio, self.storage_settings)
