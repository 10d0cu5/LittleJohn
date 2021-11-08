# Create your views here.
import json
import random
import uuid
from typing import List, Dict, Any

from django.conf import settings
from loguru import logger
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import parser_classes, api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tickerstore.models import Account
from tickerstore.tickers import tickers
from tickerstore.utils import TickerHistoryStore


@api_view(['GET'])
@parser_classes([JSONParser])
def register_user(request) -> Response:
    """
    Registering a new user at the service
    with a randomly generated uuid as username and a random 1-10 stocks for the watchlist,
    that also serves as access token for the basic auth secured endpoints /tickers/
    :return: Username: Token
    """
    token = uuid.uuid4()
    amount_of_stocks: int = random.randint(1, 10)
    random_watchlist: List[str] = random.sample(tickers, amount_of_stocks)
    new_user = Account.objects.create_user(username=token, password='', watchlist=json.dumps(random_watchlist))
    new_user.save()
    logger.info(f"Created new user with watchlist {random_watchlist} and access token {token}")
    return Response({'status': 'success', 'username': token}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@parser_classes([JSONParser])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def tickers_by_user(request) -> Response:
    """
        Getting current prices for users watchlist
        :return: List of watchlist tickers and prices
    """
    user = request.user
    watchlist: List[str] = json.loads(user.account.watchlist)
    ticker_history_store: TickerHistoryStore = getattr(settings, 'TICKER_HISTORY_STORE')
    return Response([ticker_history_store.get_current_by_ticker(ticker) for ticker in watchlist],
                    status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def ticker_history(request, ticker: str) -> Response:
    """
        Getting historic prices for a specific ticker
        By default this is the last 90 days time period
        With a POST request you can also supply json encoded size and page attributes to access a specific point
        in time up to 10 years back from now for that ticker
        :return: List tickers price history by date
    """
    ticker_history_store: TickerHistoryStore = getattr(settings, 'TICKER_HISTORY_STORE')
    if ticker not in tickers:
        return Response({"status": f"ticker symbol {ticker} not supported"}, status=status.HTTP_404_NOT_FOUND)

    page: int = 0
    size: int = 90

    if request.method == 'POST':  # Look out for pagination else 90 days
        body: Dict[str, Any] = json.loads(request.body)
        page = body.get('page', 90)
        size = body.get('size', 0)

    history: List[Dict[str, Any]] = ticker_history_store.get_history_by_ticker_paginated(ticker_name=ticker, page=page,
                                                                                         size=size)
    if history:
        return Response(history,
                        status=status.HTTP_200_OK)
    else:
        return Response({"status": f"No entries found for page {page} with size {size}"},
                        status=status.HTTP_404_NOT_FOUND)
