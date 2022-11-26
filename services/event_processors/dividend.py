from services.event_processors.processor import EventProcessor
from models.output import Stock
from models.input import Event
from pydantic.dataclasses import dataclass
from decimal import Decimal


class DividendProcessor(EventProcessor):
    @dataclass
    class Dividend:
        stock: Stock
        dividend: Decimal = 0
        withholding_tax: Decimal = 0
        withholding_tax_currency: str = None

    def __init__(self) -> None:
        super().__init__()
        self.dividends_per_stock: dict[str, DividendProcessor.Dividend] = {}

    def process_dividend(self, event: Event):
        if event.isin not in self.dividends_per_stock:
            self.dividends_per_stock[event.isin] = DividendProcessor.Dividend(
                stock=Stock(ticker=event.ticker, name=event.name, isin=event.isin),
            )
        dividend = self.dividends_per_stock[event.isin]
        dividend.dividend += event.total_eur
        dividend.withholding_tax += event.withholding_tax
        dividend.withholding_tax_currency = event.withholding_tax_currency

    def result(self) -> list[Dividend]:
        return list(self.dividends_per_stock.values())
