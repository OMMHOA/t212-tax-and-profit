from services.event_processors.processor import EventProcessor
from models.input import Event
from pydantic.dataclasses import dataclass


class DividendProcessor(EventProcessor):
    @dataclass
    class Dividend:
        ticker: str
        name: str
        isin: str
        dividend: float = 0
        withholding_tax: float = 0
        withholding_tax_currency: str = None

    def __init__(self) -> None:
        super().__init__()
        self.dividends_per_stock: dict[str, DividendProcessor.Dividend] = {}

    def process_dividend(self, event: Event):
        if event.isin not in self.dividends_per_stock:
            self.dividends_per_stock[event.isin] = DividendProcessor.Dividend(
                ticker=event.ticker,
                name=event.name,
                isin=event.isin,
            )
        dividend = self.dividends_per_stock[event.isin]
        dividend.dividend += event.total_eur
        dividend.withholding_tax += event.withholding_tax
        dividend.withholding_tax_currency = event.withholding_tax_currency

    def result(self) -> list[Dividend]:
        return list(self.dividends_per_stock.values())
