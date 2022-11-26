from services.event_processors.processor import EventProcessor
from models.input import Event
from pydantic.dataclasses import dataclass
from decimal import Decimal


class DepositWithdrawalProcessor(EventProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.deposit = 0
        self.deposit_fee = 0
        self.withdrawal = 0

    def process_deposit(self, event: Event):
        self.deposit += event.total_eur
        self.deposit_fee += event.deposit_fee_eur

    def process_withdrawal(self, event: Event):
        self.withdrawal += event.total_eur

    @dataclass(frozen=True, eq=True)
    class Result:
        deposit: Decimal
        deposit_fee: Decimal
        withdrawal: Decimal

    def result(self) -> Result:
        return DepositWithdrawalProcessor.Result(
            deposit=self.deposit,
            deposit_fee=self.deposit_fee,
            withdrawal=self.withdrawal,
        )
