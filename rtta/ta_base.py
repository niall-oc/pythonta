#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:31:37 2021

@author: xual
"""

from scipy.signal import argrelextrema
import numpy as np

class TABase:
    OPEN = 'open'
    LOW = 'low'
    HIGH = 'high'
    CLOSE = 'close'
    VOLUME = 'volume'
    CLOSE_TIME = 'close_time'
    
    def __init__(self, mkt_data):
        """
        """
        self.mkt_data = mkt_data
        # make lookups easier.
        self.df = self.mkt_data.df
        self.peak_indexes = mkt_data.peak_indexes
        self.peak_prices = mkt_data.peak_prices
        self.highs = mkt_data.highs
        self.lows = mkt_data.lows
        self.found = []
        self.obs_values = [0] * len(self.df)
    
    def is_valid_swing(self, t1, t2, up=True):
        """
        Between time t1 and time t2 if the max and min prices are at positions 
        [0] and [-1] then this is a consistent leg.
        
        In an up trend [0] is the lowest price and [-1] is the highest price.
        In a down trend [-1] is the lowest price and [0] is the highest price.

        Parameters
        ----------
        t1 : int
            DESCRIPTION.
        t2 : int
            DESCRIPTION.
        up : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        lows = self.df[self.LOW].values[self.peak_indexes[t1]:self.peak_indexes[t2]+1]
        highs = self.df[self.HIGH].values[self.peak_indexes[t1]:self.peak_indexes[t2]+1]
        # In an up trend the swing low is at the start and the swing high at the end
        # In a down trend the swing high is at the start and the swing low at the end
        swing_low, swing_high = (lows[0], highs[-1],) if up else (lows[-1], highs[0],)
        return swing_low == min(lows) and swing_high == max(highs)
    
    @staticmethod
    def is_leg(leg_prices, up=True):
        """
        The trend between two peaks is a leg of the range if no price in the
        range exceeds the swing high and swing low.

        Parameters
        ----------
        leg_prices : list
            list of prices in swing.
        up : bool, optional
            are we measuring up or down swings. The default is True.

        Returns
        -------
        bool
            This is a valid swing leg.

        """
        start, end = leg_prices[0], leg_prices[-1]
        leg_min, leg_max = min(leg_prices), max(leg_prices)
        if up and start == leg_min and end == leg_max:
            return True
        elif not up and start == leg_max and end == leg_min:
            return True
        return False