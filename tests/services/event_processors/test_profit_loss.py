from test_utils import import_module_path
import_module_path()

from services.event_processors import ProfitLossProcessor
from test_utils import EventGenerator, stock_dict

# ONLY 1 STOCK
def test_simple_full_sale_profit():
    processor = ProfitLossProcessor()
    g = EventGenerator()
    processor.process_buy(g.buy_event(shares=1, price_per_share=50))
    processor.process_sell(g.sell_event(shares=1, price_per_share=55))
    result: list[ProfitLossProcessor.ProfitLoss] = processor.result()
    assert len(result) == 1
    assert result[0].profitloss == 5


def test_over_time_full_sale_profit():
    processor = ProfitLossProcessor()
    g = EventGenerator()
    processor.process_buy(g.buy_event(shares=2, price_per_share=50))
    processor.process_sell(g.sell_event(shares=1, price_per_share=55))
    processor.process_sell(g.sell_event(shares=1, price_per_share=60))
    result: list[ProfitLossProcessor.ProfitLoss] = processor.result()
    assert len(result) == 1
    assert result[0].profitloss == 15


def test_partial_sale_profit():
    processor = ProfitLossProcessor()
    g = EventGenerator()
    processor.process_buy(g.buy_event(shares=2, price_per_share=50))
    processor.process_sell(g.sell_event(shares=1, price_per_share=60))
    result: list[ProfitLossProcessor.ProfitLoss] = processor.result()
    assert len(result) == 1
    assert result[0].profitloss == 10


def test_profit_on_selling_granted_stock():
    processor = ProfitLossProcessor()
    g = EventGenerator()
    processor.process_sell(g.sell_event(shares=2, price_per_share=60))
    result: list[ProfitLossProcessor.ProfitLoss] = processor.result()
    assert len(result) == 1
    assert result[0].profitloss == 120


def test_loss_on_delisted_stock():
    processor = ProfitLossProcessor()
    g = EventGenerator()
    processor.process_buy(g.buy_event(shares=2, price_per_share=50))
    processor.process_sell(g.sell_event(shares=2, price_per_share=0))
    result: list[ProfitLossProcessor.ProfitLoss] = processor.result()
    assert len(result) == 1
    assert result[0].profitloss == -100


def test_fractional_shares():
    processor = ProfitLossProcessor()
    g = EventGenerator()
    processor.process_buy(g.buy_event(shares=1.5, price_per_share=50))
    processor.process_sell(g.sell_event(shares=1, price_per_share=55))
    processor.process_sell(g.sell_event(shares=0.5, price_per_share=60))
    result: list[ProfitLossProcessor.ProfitLoss] = processor.result()
    assert len(result) == 1
    assert result[0].profitloss == 10


def test_unsold_stock():
    processor = ProfitLossProcessor()
    g = EventGenerator()
    processor.process_buy(g.buy_event(shares=1.5, price_per_share=50))
    result: list[ProfitLossProcessor.ProfitLoss] = processor.result()
    assert len(result) == 1
    assert result[0].profitloss == 0


# MULTIPLE STOCKS
def test_simple_full_sale_profits():
    processor = ProfitLossProcessor()
    g = EventGenerator()
    processor.process_buy(g.buy_event(shares=1, price_per_share=50))
    processor.process_buy(g.buy_event(shares=1, price_per_share=100, stock="pg"))
    processor.process_sell(g.sell_event(shares=1, price_per_share=55))
    processor.process_sell(g.sell_event(shares=1, price_per_share=155, stock="pg"))
    result: list[ProfitLossProcessor.ProfitLoss] = processor.result()
    assert len(result) == 2
    assert __result_of("apple", result).profitloss == 5
    assert __result_of("pg", result).profitloss == 55


def __result_of(stock: str, results: list[ProfitLossProcessor.ProfitLoss]) -> ProfitLossProcessor.ProfitLoss:
    isin = stock_dict[stock]["isin"]
    filtered = list(filter(lambda r: r.stock.isin == isin, results))
    if len(filtered) == 1:
        return filtered[0]
    if len(filtered) == 0:
        return 404
    raise Exception(f"Something is very wrong. It seems like a stock result is available multiple times: {filtered}")
