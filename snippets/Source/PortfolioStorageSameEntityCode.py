from everysk.sdk.entities.tags import Tags

portfolio_output: BaseDict = None
storage_settings: BaseDict = None

output_portfolio: Portfolio = None

def _initialize_output_portfolio(self) -> None:
    """
    Initializes a `Portfolio` object with form data and reference entity fallback values.
    """
    self.output_portfolio = Portfolio(**self.portfolio)

    self.output_portfolio.update({
        'name': self.portfolio_output.name or self.portfolio.name,
        'workspace': self.portfolio_output.workspace or self.workspace,
        'base_currency': self.portfolio_output.base_currency or self.portfolio.base_currency,
        'nlv': self.portfolio_output.nlv or self.portfolio.nlv,
        'date': self.portfolio_output.date or self.portfolio.date,
        'link_uid': self.portfolio_output.link_uid or self.portfolio.link_uid,
        'tags': Tags.unify(self.portfolio_output.tags, self.portfolio.tags),
    })

def _finalize_output_portfolio(self) -> None:
    """
    Finalizes a `Portfolio` object filling securities and stores it accordingly.
    """
    self.output_portfolio.securities = __SECURITIES__
    self.output_portfolio = Portfolio.script.storage(self.output_portfolio, self.storage_settings)
