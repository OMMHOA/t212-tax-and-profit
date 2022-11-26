from pydantic.dataclasses import dataclass

@dataclass
class Stock:
    ticker: str
    name: str
    isin: str
