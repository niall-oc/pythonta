#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 21:26:17 2021

@author: xual
"""
import pandas as pd

class Pattern:
    BEARISH = 'bearish'
    BULLISH = 'bullish'

    def __init__(self, symbol, interval, source, epoch_idx, y, time, derived_from, direction=None, family=None, name=None ,idx=None, formed=False, retraces=None, confirmation=None):
        """
        This class enforces that a pattern always has these attributes.  
        It is done in code so that it can be applied to any database.
        """
        self.symbol = symbol
        self.interval = interval
        self.source = source
        self.direction = direction
        self.family = family
        self.name = name
        self.idx = idx # idx within the array of peak indexes ( not used in mongo db )
        self.epoch_idx = epoch_idx # epoch candle close times
        self.y = y
        self.time = time # Time of completion, technically when the pattern came into existance
        self.formed = formed
        self.derived_from = derived_from
        self.retraces = retraces
        self.confirmation = confirmation
        self._set_completion_prices()
    
    def _set_completion_prices(self):
        if self.direction == self.BULLISH:
            X = self.y[0]
            peak = max(self.y)
            height = peak - X
            self.completion_prices = {
                0.886 : peak - (height * .886),
                0.786 : peak - (height * .786),
                1.13 : peak - (height * 1.13),
                1.27 : peak - (height * 1.27),
                1.414: peak - (height * 1.14),
                1.618: peak - (height * 1.618)
            }

    def save(self, collection):
        collection.insert_one(self.to_dict())
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            getattr(self, key)
            setattr(self, key, value)

    def to_mongo(self):
        return dict(
            symbol = self.symbol,
            interval = self.interval,
            source = self.source,
            direction = self.direction,
            family = self.family,
            name = self.name,
            epoch_idx = self.epoch_idx.tolist(),
            y = self.y,
            time = pd.to_datetime(self.time),
            formed = self.formed,
            derived_from = self.derived_from,
            retraces = self.retraces,
            confirmation = self.confirmation
        )

    def to_dict(self):
        return dict(
            symbol = self.symbol,
            interval = self.interval,
            source = self.source,
            direction = self.direction,
            family = self.family,
            name = self.name,
            idx = self.idx,
            epoch_idx = self.epoch_idx,
            y = self.y,
            time = self.time,
            formed = self.formed,
            derived_from = self.derived_from,
            retraces = self.retraces,
            confirmation = self.confirmation
        )
    
    def __str__(self):
        return str(self.to_dict())
    
    def __repr__(self):
        args = [f'{k}={repr(v)}' for k, v in self.to_dict().items()]
        return f"Pattern({', '.join(args)})"


       
class Position:
    def __init__(self, symbol, interval, source, time, amount, strike_price, targets, patterns):
        """
        This class enforces that a position always has these attributes.  
        It is done in code so that it can be applied to any database.
        """
        self.symbol = symbol
        self.interval = interval
        self.source = source
        self.time = time
        self.amount = amount
        self.price = strike_price
        self.targets = targets
        self.patterns = patterns

    def save(self, collection):
        collection.insert_one(self.to_dict())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            getattr(self, key)
            self.__dict__[key] == value
    
    def to_dict(self):
        return dict(
            symbol = self.symbol,
            interval = self.interval,
            source = self.source,
            time = self.time,
            amount = self.amount,
            strike_price = self.strike_price,
            targets = self.targets,
            confirmation = self.confirmation,
        )
    
    def __str__(self):
        return str(self.to_dict())
    
    def __repr__(self):
        args = [f'{k}={repr(v)}' for k, v in self.to_dict().items()]
        return f"Position({', '.join(args)})"