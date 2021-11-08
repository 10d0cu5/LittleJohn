import json
import random
import uuid
from typing import List

from django.conf import settings
from django.test import TestCase

from tickerstore.models import Account
from tickerstore.tickers import tickers
from tickerstore.utils import TickerHistoryStore, init_ticker_store


class TickerStoreTests(TestCase):
    new_user: Account = None
    token = uuid.uuid4()
    ticker_history_store: TickerHistoryStore = None
    init_ticker_store()

    def setUp(self):
        amount_of_stocks: int = random.randint(1, 10)
        random_watchlist: List[str] = random.sample(tickers, amount_of_stocks)
        self.new_user = Account.objects.create_user(username=self.token, password='',
                                                    watchlist=json.dumps(random_watchlist))

        self.ticker_history_store = getattr(settings, 'TICKER_HISTORY_STORE')

    def test_get_current_by_ticker(self):
        self.assertIsNotNone(self.new_user.watchlist)
        self.assertTrue(len(self.new_user.watchlist) > 0)
        ticker_prices = []
        for ticker in self.new_user.watchlist:
            ticker_prices.append(self.ticker_history_store.get_current_by_ticker(ticker))
        self.assertTrue(len(self.new_user.watchlist) == len(ticker_prices))

    def test_get_90_day_ticker_history_AAPL(self):
        ticker_name = 'AAPL'
        _90_day_history = self.ticker_history_store.get_history_by_ticker_paginated(ticker_name=ticker_name, size=90,
                                                                                    page=0)
        self.assertTrue(len(_90_day_history) == 90)

    def test_get_10_day_page_1_ticker_history_AAPL(self):
        ticker_name = 'AAPL'
        _10_day_history = self.ticker_history_store.get_history_by_ticker_paginated(ticker_name=ticker_name, size=10,
                                                                                    page=1)
        self.assertTrue(len(_10_day_history) == 10)

    def test_get_out_of_bounds_ticker_history_AAPL(self):
        ticker_name = 'AAPL'
        _out_of_bounds_history = self.ticker_history_store.get_history_by_ticker_paginated(ticker_name=ticker_name,
                                                                                           size=50,
                                                                                           page=10000)
        self.assertTrue(len(_out_of_bounds_history) == 0)

    def test_get_unknown_ticker_history_AAPL(self):
        ticker_name = 'XYZ'
        _unknown_history = self.ticker_history_store.get_history_by_ticker_paginated(ticker_name=ticker_name,
                                                                                     size=90,
                                                                                     page=0)
        self.assertTrue(len(_unknown_history) == 0)
