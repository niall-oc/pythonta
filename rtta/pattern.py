#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 21:26:17 2021

@author: xual
"""

class Pattern:
    
    def __init__(self, family, name, idx, y, direction, symbol, source, epoch, confirmation=None):
        """
        Capture the indexes and prices of an pattern on an asset from a source at a time.

        Parameters
        ----------
        family : string
            DESCRIPTION.
        name : TYPE
            DESCRIPTION.
        idx : TYPE
            DESCRIPTION.
        y : TYPE
            DESCRIPTION.
        direction : TYPE
            DESCRIPTION.
        symbol : TYPE
            DESCRIPTION.
        source : TYPE
            DESCRIPTION.
        epoch : TYPE
            DESCRIPTION.
        confirmation : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        self.family = family
        self.name = name
        self.idx = idx
        self.y = y
        self.direction = direction
        self.symbol = symbol
        self.source = source
        self.epoch = epoch
        self.confirmation = confirmation
        
