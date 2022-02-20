#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 11:41:20 2021

@author: xual
"""

from .market_data_base import MktDataBase
import yfinance as yf

class Yahoo(MktDataBase):
    """
    General market sources
    """
    def __init__(self, schema=None):
        """
        Schema is a list of dicts matching the exact column order from binance.
        """
        if schema is None:
            self.schema = [
                {"name": "open", "type":"float"},
                {"name": "high", "type":"float"},
                {"name": "low", "type":"float"},
                {"name": "close", "type":"float"},
                {"name": "volume", "type":"float"},
                {"name": "dividends", "type":"float"},
                {"name": "stock_splits", "type":"int"}
            ]
        
        self.columns = [c['name'] for c in self.schema]
        self.df = None
        self.symbol = None
        self.interval = None
        
    
    def get_ticker_ohlc(self, symbol, interval, start_time=None, end_time=None, period='30d'):
        """
        Requires an api endpoint to source the ticker data from.  Requires any
        API keys or credentials to be setup before hand.

        Parameters
        ----------
        symbol : str
            Identfies the asset for the trend eg. APPL, MSFT, BTCUSDT
        interval : str
            The time represented by each candle in the trend.  1m, 15m, 1h, 4h, 1d
        start_time : int str datetime, optional
            Implementation specific time.
        end_time : int str datetime, optional
            Implementation specific time.
        num_ticks : int, optional
            Implementation specific. Number of historical ticks requrieds The default is 200.

        Returns
        -------
        pandas.DataFrame time is index, open, high, low, close, volume

        """
        tick = yf.Ticker(symbol)
        self.df = tick.history(period=period, interval=interval, start=start_time, end=end_time)
        rename_columns = {c: c.lower().replace(' ', '_') for c in self.df.columns}
        self.df = self.df.rename(columns=rename_columns)
        self.symbol = symbol
        self.interval = interval
        return self.df
        
        
        