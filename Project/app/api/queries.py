
import requests
from datetime import datetime
from app.config import Config


def check_stocks_ticker(ticker):
    ''' Function to check if given ticker exists
        Returns boolean '''
    url = 'https://www.alphavantage.co/query?'
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": ticker,
        "apikey": Config.APLHAADVANTAGE_API_KEY
    }
    req = requests.get(url, params=params)
    results = req.json()
    ticker_exists = False
    if results["bestMatches"][0]["1. symbol"] == ticker:
        ticker_exists = True
    return ticker_exists


def get_ticker_prices(tuple_of_tickers):
    ''' Function to get min and max prices for tuple of tickets
        Returns dict {ticker: {high: max_price, low: min_price}, } '''
    url = 'https://www.alphavantage.co/query?'
    params = {
        "function": "TIME_SERIES_DAILY",
        "apikey": Config.APLHAADVANTAGE_API_KEY
    }
    # dict to store data
    minmax_tickers = {}
    # given API doesn't give opportunity to ask in bulk
    for ticker in tuple_of_tickers:
        params['symbol'] = ticker
        req = requests.get(url, params=params)
        results = req.json()
        last_date = results["Meta Data"]["3. Last Refreshed"][0:10]
        price_candle = results["Time Series (Daily)"][last_date]
        minmax_tickers[ticker] = {
            "high": price_candle["2. high"],
            "low": price_candle["3. low"]
        }
    return minmax_tickers
