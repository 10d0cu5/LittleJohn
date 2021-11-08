import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from django.conf import settings
from loguru import logger
from pydantic.main import BaseModel

from tickerstore.tickers import tickers


class TickerHistoryEntry(BaseModel):
    date: str
    price: float


class TickerHistory(BaseModel):
    ticker_name: str
    ticker_history: List[TickerHistoryEntry] = []


class TickerHistoryStore:
    __initialized: bool = False
    __ticker_histories: List[TickerHistory] = []

    def __init__(self):
        logger.info("Initializing the Ticker Histories")
        today: datetime = datetime.now().date()
        for ticker in tickers:
            ticker_current_value: float = 0.0
            for c in ticker:
                ticker_current_value += ord(c)

            ticker_history: TickerHistory = TickerHistory(ticker_name=ticker, ticker_history=[])
            ticker_history.ticker_history.append(TickerHistoryEntry(date=str(today), price=str(ticker_current_value)))

            for i in range(1, 3652):
                entry_date = (today - timedelta(days=i)).isoformat()
                entry_value = ticker_history.ticker_history[-1].price + random.randint(-10, 10)
                ticker_history.ticker_history.append(TickerHistoryEntry(date=str(entry_date), price=str(entry_value)))

            self.__ticker_histories.append(ticker_history)

        self.__initialized = True

    def __call__(self):
        if self.__initialized:
            return self

        return TickerHistoryStore()

    def get_ticker_histories(self) -> List[TickerHistory]:
        return self.__ticker_histories

    def get_current_by_ticker(self, ticker_name: str) -> Dict[str, Any]:
        for ticker_history in self.__ticker_histories:
            if ticker_history.ticker_name == ticker_name:
                return {
                    "symbol": ticker_name,
                    "price": ticker_history.ticker_history[0].price
                }

    def get_history_by_ticker(self, ticker_name: str) -> List[Dict[str, Any]]:
        for ticker_history in self.__ticker_histories:
            if ticker_history.ticker_name == ticker_name:
                return ticker_history.ticker_history

    def get_history_by_ticker_paginated(self, ticker_name: str, page: int, size: int) -> List[Dict[str, Any]]:
        for ticker_history in self.__ticker_histories:
            if ticker_history.ticker_name == ticker_name:
                if len(ticker_history.ticker_history) > (page * size):
                    return [{"date": ticker_history_item.date, "price": ticker_history_item.price} for
                            ticker_history_item in
                            ticker_history.ticker_history[page * size:page * size + size]]

        return []


def init_ticker_store():
    setattr(settings, 'TICKER_HISTORY_STORE', TickerHistoryStore())
