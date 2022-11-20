from abc import ABC
from models.input import Event


class EventProcessor(ABC):
    def process_buy(self, event: Event):
        """Process event: Events with Action.BUY and Action.LIMIT_BUY."""
        pass

    def process_sell(self, event: Event):
        """Process event: Events with Action.SELL and Action.LIMIT_SELL."""
        pass

    def process_dividend(self, event: Event):
        pass

    def process_deposit(self, event: Event):
        pass

    def process_withdrawal(self, event: Event):
        pass
