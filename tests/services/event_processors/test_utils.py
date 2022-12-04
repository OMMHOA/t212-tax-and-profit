def import_module_path():
    # add project root to module path if not added already
    import os
    import sys
    module_path = os.path.abspath(os.path.join('.'))
    if module_path not in sys.path and os.path.basename(module_path) == "t212-tax-and-profit":
        sys.path.append(module_path)
        print(f"Path '{module_path}' added to module path.")

import_module_path()

from models.input import Event, Action
from datetime import datetime, timedelta


stock_dict = {
    "apple": {
        "ticker": "AAPL",
        "name": "Apple",
        "isin": "US0378331005",
    },
    "pg": {
        "ticker": "PG",
        "name": "Procter & Gamble",
        "isin": "US7427181091"
    }
}


class EventGenerator:

    def __init__(self) -> None:
        self.time: datetime = datetime.strptime("2022-09-01 13:00:00", "%Y-%m-%d %H:%M:%S")
        self.idx = 0

    def buy_event(self, shares, price_per_share, stock="apple"):
        self.time += timedelta(hours=1)
        self.idx += 1
        stock = stock_dict[stock]
        return Event(
            action=Action.BUY,
            time=self.time,
            isin=stock["isin"],
            ticker=stock["ticker"],
            name=stock["name"],
            shares_count=shares,
            price_per_share=price_per_share,
            price_currency="USD",
            exchange_rate=1,
            total_eur=price_per_share * shares,
            ID=f"EOF{self.idx:010d}",
            conversion_fee_eur=0.1,
        )


    def sell_event(self, shares, price_per_share, stock="apple"):
        self.time += timedelta(hours=1)
        self.idx += 1
        stock = stock_dict[stock]
        return Event(
            action=Action.SELL,
            time=self.time,
            isin=stock["isin"],
            ticker=stock["ticker"],
            name=stock["name"],
            shares_count=shares,
            price_per_share=price_per_share,
            price_currency="USD",
            exchange_rate=1,
            total_eur=price_per_share * shares,
            ID=f"EOF{self.idx:010d}",
            conversion_fee_eur=0.1,
            result_eur=0, # dont care
        )