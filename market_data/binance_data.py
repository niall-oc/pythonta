#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 11:41:20 2021

@author: xual
"""

from .market_data_base import MktDataBase
import pandas as pd
from binance.spot import Spot
import datetime

class Binance(MktDataBase):
    """
    General market sources
    """
    def __init__(self, key=None, secret=None, schema=None, time_zone='Europe/Dublin', indicator_config=None):
        """
        Binance API and Secret keys needed for lifting throttle limits or IP 
        restriction.
        
        Schema is a list of dicts matching the exact column order from binance.
        
        timezone is used to convert milisecond epoches to correct times for timezone.
        """
        super(Binance, self).__init__(indicator_config=indicator_config)
        if schema is None:
            self.schema = [
                {"name": "open_time", "type":"int"},
                {"name": "open", "type":"float"},
                {"name": "high", "type":"float"},
                {"name": "low", "type":"float"},
                {"name": "close", "type":"float"},
                {"name": "volume", "type":"float"},
                {"name": "close_time", "type":"int"},
                {"name": "quote_asset_volume", "type":"float"},
                {"name": "number_of_trades", "type":"int"},
                {"name": "taker_base_asset_volume", "type":"float"},
                {"name": "taker_quote_asset_colume", "type":"float"},
                {"name": "ignore", "type":"float"}
            ]
        
        self.columns = [c['name'] for c in self.schema]
        self.rc = Spot(key=key, secret=secret)
        self.time_zone = time_zone
        self.df = None
        self.symbol = None
        self.interval = None
    
    def _get_binance_time(self, t):
        """
        Returns the correct epoch for binance

        Parameters
        ----------
        t : TYPE
            DESCRIPTION.

        Returns
        -------
        int

        """
        if t is None:
            return None
        elif isinstance(t, (int, float,)):
            return int(t)
        elif isinstance(t, (datetime.date, datetime.datetime,)):
            return int(t.timestamp()*1000)
        else:
            raise ValueError('Binance start or end time must be epoch milliseconds')
        return None
    
    def _set_df(self, data):
        """
        

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.df = pd.DataFrame(data=data, columns=self.columns)
        for col in self.schema:
            self.df[col['name']] = self.df[col['name']].astype(col['type'])
        self.df['dts'] = pd.to_datetime(self.df['close_time'], unit='ms', utc=True).dt.tz_convert(self.time_zone)
        self.df = self.df.set_index('dts')
    
    def get_all_data(self, symbol, interval, start_time, chunks=1000):
        """
        

        Parameters
        ----------
        symbol : str
            Identfies the asset for the trend eg. APPL, MSFT, BTCUSDT
        interval : str
            The time represented by each candle in the trend.  1m, 15m, 1h, 4h, 1d
        start_time : int time in epoch
            Implementation specific time.
        chunks : int, optional
            Number of Ticks per chunk

        Returns
        -------
        pandas.DataFrame time is index, open, high, low, close, volume

        """
        self.symbol = symbol
        self.interval = interval
        start_time = self._get_binance_time(start_time)
        end_time = start_time + 1
        data = []
        while True:
            data += self.rc.klines(
                symbol, 
                interval, 
                startTime=start_time,
                limit=chunks
            )
            end_time = data[-1][6]
            if end_time == start_time:
                break
            else:
                start_time = end_time
        self._set_df(data)
        return self.df
         
    
    def get_ticker_ohlc(self, symbol, interval, start_time=None, end_time=None, num_ticks=200):
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
        self.symbol = symbol
        self.interval = interval
        data = self.rc.klines(
            symbol, 
            interval, 
            startTime=self._get_binance_time(start_time), 
            endTime=self._get_binance_time(end_time), 
            limit=num_ticks
        )
        self._set_df(data)
        return self.df
        
        