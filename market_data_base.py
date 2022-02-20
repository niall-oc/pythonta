#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 17:02:46 2021

@author: xual
"""
from ta.trend import MACD
from ta.momentum import StochasticOscillator, RSIIndicator
from ta.volume import ChaikinMoneyFlowIndicator
from scipy.signal import argrelextrema
import numpy as np

class MktDataBase:
    OPEN_TIME = 'open_time'
    CLOSE_TIME = 'close_time'
    OPEN = 'open'
    LOW = 'low'
    HIGH = 'high'
    CLOSE = 'close'
    VOLUME = 'volume'
    COLUMNS = [OPEN, HIGH, LOW, CLOSE, VOLUME]
    INDICATOR_CONFIG = {
        'macd': {'window_slow': 26, 'window_fast': 12, 'window_sign': 9},
        'stoch_rsi': {'window': 14, 'smooth_window': 3},
        'rsi': {'window': 14},
        'mfi': {'window': 20}
    }
    macd=None
    rsi=None
    stoch_rsi=None
    mfi=None

    def __init__(self, indicator_config=None):
        self.INDICATOR_CONFIG = indicator_config or {
            'macd': {'window_slow': 26, 'window_fast': 12, 'window_sign': 9},
            'stoch_rsi': {'window': 14, 'smooth_window': 3},
            'rsi': {'window': 14},
            'mfi': {'window': 20}
        }
        self.obs_values = None
    
    def merge_obs(self, array):
        for i in range(len(self.obs_values)):
            self.obs_values[i] += array[i]
    
    def set_peaks(self, peak_spacing=6):
        self.obs_values = [0] * len(self.df)
        self.set_indicators()
        self.find_price_peaks(peak_spacing=peak_spacing)
        self.indicator_peaks = {
            'macd': self.find_indicator_peaks(self.macd.macd_diff(), peak_spacing=peak_spacing),
            'rsi': self.find_indicator_peaks(self.rsi.rsi(), peak_spacing=peak_spacing),
            'mfi': self.find_indicator_peaks(self.mfi.chaikin_money_flow(), peak_spacing=peak_spacing)
        }
        self.add_obs_values(self.highs, bullish=False, value=1)
        self.add_obs_values(self.lows, bullish=True, value=1)
        for key in self.indicator_peaks.keys():
            self.add_obs_values(self.indicator_peaks[key]['highs']['idx'], bullish=False, value=1)
            self.add_obs_values(self.indicator_peaks[key]['lows']['idx'], bullish=True, value=1)
        
        for i in range(len(self.indicator_peaks['rsi']['highs']['idx'])):
            reading = self.indicator_peaks['rsi']['highs']['indicator'][i]
            self.obs_values[self.indicator_peaks['rsi']['highs']['idx'][i]] += (reading-50)/10
        
        for i in range(len(self.indicator_peaks['rsi']['lows']['idx'])):
            reading = self.indicator_peaks['rsi']['lows']['indicator'][i]
            self.obs_values[self.indicator_peaks['rsi']['lows']['idx'][i]] -= (50-reading)/10
            
    def add_obs_values(self, indexes, bullish=True, value=1):
        """
        

        Parameters
        ----------
        indexes : list
            A list of trend indexes that represent areas of over bought or over sold significance.
        bullish : bool, optional
            bullish == True subtracts value otherwise we add value. The default is True.
        value : int, optional
            How much value to add to the OBS index. The default is 1.

        Returns
        -------
        None.

        """
        for i in indexes:
            if bullish:
                self.obs_values[i] -= value
            else:
                self.obs_values[i] += value
        
    
    def find_indicator_peaks(self, series, peak_spacing=6):
        """
        
        Parameters
        ----------
        series: pd.Series
            The the indicator sub trend you are scanning for peak_indexes.
        order : int, optional
            Helps argelextrema find true peak_indexes and removes noise. The default is 10.

        Returns
        -------
        list of tuples, peak_idx, peak_price

        """
        highs = list(argrelextrema(series.values, np.greater_equal, order=peak_spacing)[0])
        lows = list(argrelextrema(series.values, np.less_equal, order=peak_spacing)[0])
        peaks = dict(
            highs = {'idx': highs, 'indicator': series.values[highs], 'peak_prices': self.df[self.HIGH].values[highs]},
            lows = {'idx': lows, 'indicator': series.values[lows], 'peak_prices': self.df[self.LOW].values[lows]}
        )
        return peaks
    
    def find_price_peaks(self, peak_spacing=6):
        """
        
        Parameters
        ----------
        order : int, optional
            Helps argelextrema find true peaks and removes noise. The default is 10.

        Returns
        -------
        list of tuples, peak_idx, peak_price

        """
        self.highs = list(argrelextrema(self.df[self.HIGH].values, np.greater_equal, order=peak_spacing)[0])
        self.lows = list(argrelextrema(self.df[self.LOW].values, np.less_equal, order=peak_spacing)[0])
        idxes = sorted(
            list(zip(self.highs, self.df[self.HIGH].values[self.highs])) +\
            list(zip(self.lows, self.df[self.LOW].values[self.lows]))
        )
        self.peak_prices = [float(p[1]) for p in idxes]
        self.peak_indexes = [int(p[0]) for p in idxes]
    
    def set_indicators(self, indicator_config=None):
        if indicator_config:
            for key, params in indicator_config.items:
                self.INDICATOR_CONFIG[key] = params
        self.macd = MACD( close=self.df[self.CLOSE], **self.INDICATOR_CONFIG['macd'])
        self.stoch_rsi = StochasticOscillator(
            high=self.df[self.HIGH],
            close=self.df[self.CLOSE],
            low=self.df[self.LOW],
            **self.INDICATOR_CONFIG['stoch_rsi']
        )
        self.rsi = RSIIndicator(close=self.df[self.CLOSE], **self.INDICATOR_CONFIG['rsi'])
        self.mfi = ChaikinMoneyFlowIndicator(
            high=self.df[self.HIGH],
            close=self.df[self.CLOSE],
            low=self.df[self.LOW],
            volume=self.df[self.VOLUME],
            **self.INDICATOR_CONFIG['mfi']
        )
    
    
    