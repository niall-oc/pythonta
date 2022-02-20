#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 19:38:41 2021

@author: xual
"""
from .ta_base import TABase

class Divergence(TABase):
    
    def __init__(self, mkt_data):
        super(Divergence, self).__init__(mkt_data)
    
    def search(self, time_limit=0):
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