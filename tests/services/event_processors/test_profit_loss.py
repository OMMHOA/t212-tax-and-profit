from test_utils import import_module_path
import_module_path()

from services.event_processors import ProfitLossProcessor
from test_utils import EventGenerator

def test_simple_full_sale_profit():
    processor = ProfitLossProcessor()
    g = EventGenerator()
    processor.process_buy(g.buy_event(shares=1, price=50))
    processor.process_sell(g.sell_event(shares=1, price=55))
    result: list[ProfitLossProcessor.ProfitLoss] = processor.result()
    assert len(result) == 1
    assert result[0].profitloss == 5


def test_over_time_full_sale_profit():
    processor = ProfitLossProcessor()
    g = EventGenerator()
    processor.process_buy(g.buy_event(shares=2, price=50))
    processor.process_sell(g.sell_event(shares=1, price=55))
    processor.process_sell(g.sell_event(shares=1, price=60))
    result: list[ProfitLossProcessor.ProfitLoss] = processor.result()
    assert len(result) == 1
    assert result[0].profitloss == 15


def test_partial_sale_profit():
    processor = ProfitLossProcessor()
    g = EventGenerator()
    processor.process_buy(g.buy_event(shares=2, price=50))
    processor.process_sell(g.sell_event(shares=1, price=60))
    result: list[ProfitLossProcessor.ProfitLoss] = processor.result()
    assert len(result) == 1
    assert result[0].profitloss == 10


