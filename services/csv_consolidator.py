from models.input import Event, Action
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation

header_to_field_mapping = {
    "Action": "action",
    "Time": "time",
    "ISIN": "isin",
    "Ticker": "ticker",
    "Name": "name",
    "No. of shares": "shares_count",
    "Price / share": "price_per_share",
    "Currency (Price / share)": "price_currency",
    "Exchange rate": "exchange_rate",
    "Result (EUR)": "result_eur",
    "Total (EUR)": "total_eur",
    "Withholding tax": "withholding_tax",
    "Currency (Withholding tax)": "withholding_tax_currency",
    "Charge amount (EUR)": "charge_amount_eur",
    "Deposit fee (EUR)": "deposit_fee_eur",
    "Stamp duty reserve tax (EUR)": "stamp_duty_tax_eur",
    "Notes": "notes",
    "ID": "ID",
    "French transaction tax": "french_tax",
    "Currency conversion fee (EUR)": "conversion_fee_eur",
}


def to_decimal(x):
    try:
        x = x.strip()
        return Decimal(x) if x else 0.0
    except InvalidOperation as ex:
        return 0


action_mapper = {
    "Market buy": Action.BUY,
    "Market sell": Action.SELL,
    "Dividend (Ordinary)": Action.DIVIDEND,
    "Deposit": Action.DEPOSIT,
    "Withdrawal": Action.WITHDRAWAL,
    "Limit buy": Action.LIMIT_BUY,
    "Limit sell": Action.LIMIT_SELL,
}


def to_action(x):
    return action_mapper[x.strip()]


header_to_converter_mapping = {
    "action": to_action,
    "time": lambda x: datetime.fromisoformat(x),
    "isin": lambda x: x,
    "ticker": lambda x: x,
    "name": lambda x: x,
    "shares_count": to_decimal,
    "price_per_share": to_decimal,
    "price_currency": lambda x: x,
    "exchange_rate": to_decimal,
    "result_eur": to_decimal,
    "total_eur": to_decimal,
    "withholding_tax": to_decimal,
    "withholding_tax_currency": lambda x: x,
    "charge_amount_eur": to_decimal,
    "deposit_fee_eur": to_decimal,
    "stamp_duty_tax_eur": to_decimal,
    "notes": lambda x: x,
    "ID": lambda x: x,
    "french_tax": to_decimal,
    "conversion_fee_eur": to_decimal,
}


def deduplicate(csv_inputs: list[Event]) -> list[Event]:
    input_set = set()
    deduplicated = []
    for l in csv_inputs:
        if l not in input_set:
            deduplicated.append(l)
            input_set.add(l)
    return deduplicated


def consolidate(input_dir):
    inputs = []
    # parse from csv files
    for csv in os.listdir(input_dir):
        if csv == ".keep":
            continue
        with open(f"{input_dir}/{csv}", "r") as fo:
            headers = [
                header_to_field_mapping[h.strip()] for h in fo.readline().split(",")
            ]
            for line in fo:
                m = {}
                for i, v in enumerate(line.split(",")):
                    header = headers[i]
                    m[header] = header_to_converter_mapping[header](v)
                inputs.append(Event(**m))

    inputs = deduplicate(inputs)
    print(f"Consolidation done, got {len(inputs)} consolidated rows.")
    return inputs
