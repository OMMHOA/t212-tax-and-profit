from models.input import Action, Event
from services.event_processors import EventProcessor


class EventEmitter:
    def __init__(self) -> None:
        self.subscribers: dict[Action, list[EventProcessor]] = dict(
            [(a, []) for a in Action]
        )

    def subscribe(self, subscriber: EventProcessor, action: Action | list[Action]):
        """Subscribe processor to an Action or list of Actions."""

        def add_subscriber(action, subscriber):
            self.subscribers[action].append(subscriber)

        if type(action) is Action:
            add_subscriber(action, subscriber)
        elif type(action) is list:
            for a in action:
                add_subscriber(a, subscriber)
        else:
            raise TypeError("The action param can be Action or list[Action] only.")

    def start(self, events: list[Event]):
        for e in events:
            match e.action:
                case Action.SELL | Action.LIMIT_SELL:
                    for s in self.subscribers[Action.SELL]:
                        s.process_sell(e)
                    for s in self.subscribers[Action.LIMIT_SELL]:
                        s.process_sell(e)
                case Action.BUY | Action.LIMIT_BUY:
                    for s in self.subscribers[Action.BUY]:
                        s.process_buy(e)
                    for s in self.subscribers[Action.LIMIT_BUY]:
                        s.process_buy(e)
                case Action.DIVIDEND:
                    for s in self.subscribers[Action.DIVIDEND]:
                        s.process_dividend(e)
                case Action.DEPOSIT:
                    for s in self.subscribers[Action.DEPOSIT]:
                        s.process_deposit(e)
                case Action.WITHDRAWAL:
                    for s in self.subscribers[Action.WITHDRAWAL]:
                        s.process_withdrawal(e)
