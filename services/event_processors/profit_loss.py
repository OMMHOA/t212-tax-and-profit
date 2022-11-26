from services.event_processors.processor import EventProcessor
from models.input import Event
from pydantic.dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


class ProfitLossProcessor(EventProcessor):
    @dataclass
    class Buy:
        ts: datetime
        amount: Decimal

    @dataclass
    class Sell:
        ts: datetime
        amount: Decimal
