from services.event_processors.processor import EventProcessor
from models.output import Stock
from models.input import Event
from pydantic.dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Tuple


class ProfitLossProcessor(EventProcessor):
    @dataclass
    class Buy:
        ts: datetime
        amount: Decimal
        shares: Decimal
        next: Any = None

    @dataclass
    class Sell:
        ts: datetime
        amount: Decimal
        shares: Decimal

    @dataclass
    class ProfitLoss:
        stock: Stock
        profitloss: Decimal
        remaining_shares: Decimal
        remaining_invested_amount: Decimal

    def __init__(self) -> None:
        super().__init__()
        self.__buys: dict[str, self.Buy] = {}
        self.__profits: dict[str, Decimal] = {}
        self.__stocks: dict[str, Stock] = {}

    def process_buy(self, event: Event):
        self._register_stock(event)
        buy_amount = (
            event.total_eur
            - event.french_tax
            - event.conversion_fee_eur
            - event.stamp_duty_tax_eur
        )
        buys = self._buys(event.isin)
        while buys.next is not None:
            buys = buys.next
        buys.next = self.Buy(
            ts=event.time, amount=buy_amount, shares=event.shares_count
        )

    def process_sell(self, event: Event):
        self._register_stock(event)
        profit = (
            event.total_eur
            - event.french_tax
            - event.conversion_fee_eur
            - event.stamp_duty_tax_eur
        )
        sold_shares = event.shares_count
        buy = self._buys(event.isin)
        while buy is not None:
            if event.time < buy.ts:
                break
            if sold_shares >= buy.shares:
                sold_shares -= buy.shares
                profit -= buy.amount
                self._set_buys(event.isin, buy.next)
            else:
                buy_price_per_share = buy.amount / buy.shares
                buy.shares -= sold_shares
                profit -= buy_price_per_share * sold_shares
                break
            buy = buy.next
        self._set_profit(event.isin, profit)

    def result(self) -> list[ProfitLoss]:
        def get_profitloss(isin, stock) -> self.ProfitLoss:
            profit = self.__profits[isin] if isin in self.__profits else Decimal(0)
            shares, invested = self._remaining_shares(isin)
            return self.ProfitLoss(
                stock=stock,
                profitloss=profit,
                remaining_shares=shares,
                remaining_invested_amount=invested,
            )

        return [get_profitloss(isin, stock) for isin, stock in self.__stocks.items()]

    def _remaining_shares(self, isin: str) -> Tuple[Decimal, Decimal]:
        def _sum(
            buy: self.Buy, shares: Decimal, invested: Decimal
        ) -> Tuple[Decimal, Decimal]:
            if buy is None:
                return (shares, invested)
            return _sum(buy.next, shares + buy.shares, invested + buy.amount)

        return _sum(self._buys(isin), Decimal(0), Decimal(0))

    def _buys(self, isin) -> Buy:
        if isin not in self.__buys or self.__buys[isin] is None:
            self.__buys[isin] = self.Buy(ts=datetime.min, amount=0, shares=0)
        return self.__buys[isin]

    def _set_buys(self, isin, buy) -> None:
        self.__buys[isin] = buy

    def _set_profit(self, isin, profit) -> None:
        if isin not in self.__profits:
            self.__profits[isin] = profit
        else:
            self.__profits[isin] += profit

    def _register_stock(self, event: Event) -> None:
        if event.isin not in self.__stocks:
            self.__stocks[event.isin] = Stock(
                ticker=event.ticker, name=event.name, isin=event.isin
            )
