#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 19:38:41 2021

@author: xual
"""
from .ta_base import TABase
from db import Pattern #Overriding create_pattern 

class Divergence(TABase):
    
    def __init__(self, mkt_data):
        super(Divergence, self).__init__(mkt_data)
        self.family = "divergence"
        
    def classify(self, d, i, lows=False):
        """
        """
        name = False
        if lows: # Bullish divergence is on low points
            if d['indicator'][i] > d['indicator'][i-1] and d['peak_prices'][i] < d['peak_prices'][i-1]:
                name = "regular" # Low price strong indicator
            elif d['indicator'][i] < d['indicator'][i-1] and d['peak_prices'][i] > d['peak_prices'][i-1]:
                name = "hidden" # oversold at high price
            elif d['indicator'][i] < d['indicator'][i-1] and d['peak_prices'][i] == d['peak_prices'][i-1]:
                name = "exaggerated" # double bottom with bullish control on RSI
        else: # Bearish signals
            if d['indicator'][i] > d['indicator'][i-1] and d['peak_prices'][i] < d['peak_prices'][i-1]:
                name = "hidden" # Nearing over bought with price falling
            elif d['indicator'][i] < d['indicator'][i-1] and d['peak_prices'][i] > d['peak_prices'][i-1]:
                name = "regular" # Price gaining with bearish control
            elif d['indicator'][i] < d['indicator'][i-1] and d['peak_prices'][i] == d['peak_prices'][i-1]:
                name = "exaggerated" # Double top with weakinging RSI
        return name

    def create_pattern(self, x, y, name, direction, indicator):
        """
        """
        return Pattern(
            self.mkt_data.symbol,
            self.mkt_data.interval,
            self.mkt_data.source,
            self.df.index.values[x],
            y,
            self.df.index.values[x[-1]],
            derived_from = indicator,
            family = self.family,
            name = name,
            direction = direction,
            formed =True,
            idx = x
        )
    def search(self, time_limit=0, formed=True, only=None):
        self.found = []
        for indicator, p in self.mkt_data.indicator_peaks.items():

            # Bullish divergences occur on lows
            lows = p['lows']
            MAX = len(lows['idx'])
            d_len = len(self.mkt_data.df)
            time_limit = d_len - time_limit if time_limit else time_limit
            for i in range(1, MAX):
                if lows['idx'][i] > time_limit:
                    name = self.classify(lows, i, lows=True)
                    if name:
                        x = [lows['idx'][i-1], lows['idx'][i]]
                        y = [lows['indicator'][i-1], lows['indicator'][i]]
                        pattern = self.create_pattern(x, y, name, 'bullish', indicator)
                        self.found.append(pattern)
                        self.obs_values[x[0]] -= 1
                        self.obs_values[x[1]] -= 1
            
            # Bearish divergences occur on peaks
            highs = p['highs']
            MAX = len(highs['idx'])
            time_limit = MAX - time_limit if time_limit else time_limit
            for i in range(1, MAX):
                if highs['idx'][i] > time_limit:
                    name = self.classify(highs, i, lows=False)
                    if name:
                        x = [highs['idx'][i-1], highs['idx'][i]]
                        y = [highs['indicator'][i-1], highs['indicator'][i]]
                        pattern = self.create_pattern(x, y, name, 'bearish', indicator)
                        self.found.append(pattern)
                        self.obs_values[x[0]] += 1
                        self.obs_values[x[1]] += 1
        return self.get_patterns(formed=formed, only=only)
        
    def search_old(self, time_limit=0):
        # Highs are bearish
        self.divergences = []
        for indicator, p in self.mkt_data.indicator_peaks.items():
            d = p['lows']
            MAX = len(d['idx'])
            d_len = len(self.mkt_data.df)
            time_limit = d_len - time_limit if time_limit else time_limit
            for i in range(1, MAX):
                if d['idx'][i] > time_limit and\
                   (d['indicator'][i] > d['indicator'][i-1] and d['peak_prices'][i] < d['peak_prices'][i-1] ) or\
                   (d['indicator'][i] < d['indicator'][i-1] and d['peak_prices'][i] > d['peak_prices'][i-1] ) :
                    self.divergences.append({
                         'type': indicator,
                        'direction': 'bullish',
                        'peak_indexes': [d['idx'][i-1], d['idx'][i]], 
                        'peak_prices': [d['indicator'][i-1], d['indicator'][i]],
                    })
                    self.obs_values[d['idx'][i-1]] -= 1
                    self.obs_values[d['idx'][i]] -= 1
            # Lows are bullish
            d = p['highs']
            MAX = len(d['idx'])
            time_limit = MAX - time_limit if time_limit else time_limit
            for i in range(1, MAX):
                if d['idx'][i] > time_limit and\
                   (d['indicator'][i] > d['indicator'][i-1] and d['peak_prices'][i] < d['peak_prices'][i-1] ) or\
                   (d['indicator'][i] < d['indicator'][i-1] and d['peak_prices'][i] > d['peak_prices'][i-1] ) :
                    self.divergences.append({
                        'type': indicator,
                        'direction': 'bearish',
                        'peak_indexes': [d['idx'][i-1], d['idx'][i]], 
                        'peak_prices': [d['indicator'][i-1], d['indicator'][i]],
                    })
                    self.obs_values[d['idx'][i-1]] += 1
                    self.obs_values[d['idx'][i]] += 1
        return self.divergences
    
    def get_patterns(self, formed=True, only=None):
        patterns = self.found
        if formed:
            patterns =  [p for p in patterns if p.formed]
        if only in ('bullish', 'bearish',):
            patterns = [p for p in patterns if p.direction == only]
        return patterns
