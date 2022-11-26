from datetime import datetime
from pydantic.dataclasses import dataclass
from enum import Enum
from decimal import Decimal


class Action(Enum):
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    LIMIT_BUY = "limit buy"
    LIMIT_SELL = "limit sell"


@dataclass(frozen=True, eq=True)
class Event:
    action: Action = None
    time: datetime = None
    isin: str = None
    ticker: str = None
    name: str = None
    shares_count: Decimal = 0
    price_per_share: Decimal = 0
    price_currency: str = None
    exchange_rate: Decimal = 0
    result_eur: Decimal = 0
    total_eur: Decimal = 0
    withholding_tax: Decimal = 0
    withholding_tax_currency: str = None
    charge_amount_eur: Decimal = 0
    deposit_fee_eur: Decimal = 0
    stamp_duty_tax_eur: Decimal = 0
    notes: str = None
    ID: str = None
    french_tax: Decimal = 0
    conversion_fee_eur: Decimal = 0

    class Config:
        anystr_strip_whitespace = True
