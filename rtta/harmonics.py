#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:24:53 2021

@author: xual
"""

from .ta_base import TABase

class HarmonicPatterns(TABase):
    """
    Search for patterns that are M or W, abcd, OXABC e.t.c
    """
    
    def __init__(self, mkt_data,  patterns=None, variance=.02):
        """
        

        Parameters
        ----------
        market_data : MktDataBase
            An instance of a market data object.

        Returns
        -------
        None.

        """
        super(HarmonicPatterns, self).__init__(mkt_data)
        self.PATTERNS_FAMILIES = patterns or {
            "HARMONICS" : {
                "crab": {
                    "XAB": {"min": 0.382, "max": 0.618},
                    "ABC": {"min": 0.382, "max": 0.886},
                    "BCD": {"min": 2.618, "max": 3.618},
                    "XAD": {"min": 1.618, "max": 1.618}
                },
                "crab-deep": {
                    "XAB": {"min": 0.886, "max": 0.886},
                    "ABC": {"min": 0.382, "max": 0.886},
                    "BCD": {"min": 2.227, "max": 3.618},
                    "XAD": {"min": 1.618, "max": 1.618}
                },
                "butterfly-deep": {
                    "XAB": {"min": 0.786, "max": 0.786},
                    "ABC": {"min": 0.382, "max": 0.886},
                    "BCD": {"min": 1.618, "max": 2.618},
                    "XAD": {"min": 1.618, "max": 1.618}
                },
                "butterfly": {
                    "XAB": {"min": 0.786, "max": 0.786},
                    "ABC": {"min": 0.382, "max": 0.886},
                    "BCD": {"min": 1.618, "max": 2.618},
                    "XAD": {"min": 1.27, "max": 1.27}
                },
                "bat": {
                    "XAB": {"min": 0.382, "max": 0.50},
                    "ABC": {"min": 0.382, "max": 0.886},
                    "BCD": {"min": 1.618, "max": 2.618},
                    "XAD": {"min": 0.886, "max": 0.886}
                },
                "bat-alternate": {
                    "XAB": {"min": 0.382, "max": 0.382},
                    "ABC": {"min": 0.382, "max": 0.886},
                    "BCD": {"min": 2.0, "max": 3.618},
                    "XAD": {"min": 1.13, "max": 1.13}
                },
                "gartley": {
                    "XAB": {"min": 0.618, "max": 0.618},
                    "ABC": {"min": 0.382, "max": 0.886},
                    "BCD": {"min": 1.27, "max": 1.618},
                    "XAD": {"min": 0.786, "max": 0.786}
                },
                "bartley": {
                    "XAB": {"min": 0.618, "max": 0.681},
                    "ABC": {"min": 0.382, "max": 0.886},
                    "BCD": {"min": 1.27, "max": 2.618},
                    "XAD": {"min": 0.886, "max": 0.886}
                }
            },
            
            "CYPHERS": {
                "cypher": {
                    "XAB": {"min": 0.382, "max": 0.618},
                    "XAC": {"min": 1.13, "max": 1.417},
                    "XCD": {"min": 0.786, "max": 0.786}
                }
            },
            
            "SHARKS": {
                "shark": {
                    "XAB": {"min": 0.386, "max": 0.618},
                    "ABC": {"min": 1.13, "max": 1.13},
                    "XAD": {"min": 0.886, "max": 0.886},
                    "XCD": {"min": 0.886, "max": 0.886},
                    "BCD": {"min": 1.618, "max": 2.24},
                },
                "shark-deep": {
                    "XAB": {"min": 0.386, "max": 0.618},
                    "ABC": {"min": 1.618, "max": 1.618},
                    "XAD": {"min": 1.13, "max": 1.13},
                    "XCD": {"min": 1.13, "max": 1.13},
                    "BCD": {"min": 1.618, "max": 2.24},
                }
            },
            "ABCD":{
                "ABCD-382-1": {
                    "ABC": {"min": 0.382, "max": 0.382},
                    "BCD": {"min": 2.24, "max": 2.24},
                },
                "ABCD-382-2": {
                    "ABC": {"min": 0.382, "max": 0.382},
                    "BCD": {"min": 2.618, "max": 2.618},
                },
                "ABCD-50": {
                    "ABC": {"min": 0.5, "max": 0.5},
                    "BCD": {"min": 2, "max": 2},
                },
                "ABCD-618": {
                    "ABC": {"min": 0.618, "max": 0.618},
                    "BCD": {"min": 1.618, "max": 1.618},
                },
                "ABCD-707": {
                    "ABC": {"min": 0.707, "max": 0.707},
                    "BCD": {"min": 1.41, "max": 1.41},
                },
                "ABCD-786": {
                    "ABC": {"min": 0.786, "max": 0.786},
                    "BCD": {"min": 1.27, "max": 1.27},
                },
                "ABCD-886": {
                    "ABC": {"min": 0.886, "max": 0.886},
                    "BCD": {"min": 1.13, "max": 1.13},
                }
            }
        }
        
        # set pattern variance
        for family, patterns in self.PATTERNS_FAMILIES.items():
            for pattern, legs in patterns.items():
                for leg, details in legs.items():
                    details["min"] = details["min"] * (1-variance)
                    details["max"] = details["max"] * (1+variance)
        # print(f"Variance={1-variance} - {1+variance} \n {self.PATTERNS}")
        self.harmonics = self.PATTERNS_FAMILIES['HARMONICS']
        self.cyphers = self.PATTERNS_FAMILIES['CYPHERS']
        self.sharks = self.PATTERNS_FAMILIES['SHARKS']
        self.family = 'harmonic'
    
    def set_obs(self):
        self.obs_values = [0] * len(self.df)
        # Bullish
        for pattern in self.get_patterns(formed=True):
            if pattern['direction'] == 'bullish':
                self.obs_values[pattern['idx'][-1]] -= 1
            else:
                self.obs_values[pattern['idx'][-1]] += 1
    
    def m_scan_from(self, D):
        """
        From the final point in the bullish M pattern we can traverse from D 
        back to 0 and scan each peak to see if a pattern fits.
        
        As M patterns are found they are appended into an array

        Parameters
        ----------
        D : int
            Index of the final point in the M pattern.

        Returns
        -------
        None.

        """
        for C in range(D-1, -1, -1):

            if self.peak_prices[C] < self.peak_prices[D]:
                break # Let C become D
            elif self.peak_indexes[C] in self.highs and \
                self.is_valid_swing(C, D, up=False): # C to D must be a downward leg
                        
                for B in range(C-1, -1, -1):
            
                    if self.peak_prices[B] < self.peak_prices[D] and self.peak_prices[B] > self.peak_prices[C]:
                        # B must be lower than C
                        break # let C become B
                    elif self.peak_indexes[B] in self.lows and \
                        self.is_valid_swing(B, C, up=True): # B to C must be an upward leg
                        
                        for A in range(B-1, -1, -1):
                            
                            if self.peak_prices[A] < self.peak_prices[B]: # Not a bull pattern
                                break # Let A become B
                            elif self.peak_indexes[A] in self.highs and \
                                self.is_valid_swing(A, B, up=False): # A to B must be a downward leg
                                pattern = self._is_abcd(A, B, C, D)
                                if pattern:
                                    self.add_pattern(pattern, 'bullish')
                                    
                                for X in range(A-1, -1, -1):
                                    
                                    if self.peak_prices[X] > self.peak_prices[A]: # Not a bull pattern
                                        break # let X become A
                                    elif self.peak_indexes[X] in self.lows and \
                                        self.peak_prices[X] < self.peak_prices[B] and \
                                        self.is_valid_swing(X, A, up=True): # Bat action magnet

                                        pattern = self._is_5_harmonic(X, A, B, C, D)
                                        if pattern:
                                            self.add_pattern(pattern, 'bullish')
                                        
                                        pattern = self._is_abcd(X, A, B, C)
                                        if pattern:
                                            self.add_pattern(pattern, 'bearish')

    
    def w_scan_from(self, D):
        """
        From the final point in the bearish W pattern we can traverse from D 
        back to 0 and scan each peak to see if a pattern fits.
        
        As W patterns are found they are appended into an array

        Parameters
        ----------
        D : int
            Index of the final point in the M pattern.

        Returns
        -------
        None.

        """
        for C in range(D-1, -1, -1):

            if self.peak_prices[C] > self.peak_prices[D]:
                break # Let C become D
            elif self.peak_indexes[C] in self.lows and \
                self.is_valid_swing(C, D, up=True): # C to D must be a upward leg
                        
                for B in range(C-1, -1, -1):
            
                    if self.peak_prices[B] > self.peak_prices[D] and self.peak_prices[B] < self.peak_prices[C]:
                        break # let C become B
                    elif self.peak_indexes[B] in self.highs and \
                        self.is_valid_swing(B, C, up=False): # B to C must be an downward leg
                        
                        for A in range(B-1, -1, -1):
                            
                            if self.peak_prices[A] > self.peak_prices[B]: # Not a bull pattern
                                break # Let A become B
                            elif self.peak_indexes[A] in self.lows and \
                                self.is_valid_swing(A, B, up=True): # A to B must be a downward leg
                                # possible ABCD formation
                                pattern = self._is_abcd(A, B, C, D)
                                if pattern:
                                    self.add_pattern(pattern, 'bearish')
                                
                                for X in range(A-1, -1, -1):
                                    
                                    if self.peak_prices[X] < self.peak_prices[A]: # Not a bull pattern
                                        break # let X become A
                                    elif self.peak_indexes[X] in self.highs and \
                                        self.peak_prices[X] > self.peak_prices[B] and \
                                        self.is_valid_swing(X, A, up=False): # Bat action magnet

                                        pattern = self._is_5_harmonic(X, A, B, C, D)
                                        if pattern:
                                            self.add_pattern(pattern, 'bearish')
                                        
                                        pattern = self._is_abcd(X, A, B, C)
                                        if pattern:
                                            self.add_pattern(pattern, 'bullish')
                                            
    def add_pattern(self, pattern, direction):
        pattern.update(
            direction = direction,
        )
        if direction == 'bullish':
            self.obs_values[pattern.idx[-1]] -= 1
        else:
            self.obs_values[pattern.idx[-1]] += 1
        self.found.append(pattern)

        
    def search(self, limit_to=0, formed=True, only='all'):
        """
        Working backwards through the trend until while the D leg is still later
        than the time limit. Scan for bull if D is a low or bear patterns if D
        is a high.
        """
        MAX = len(self.peak_indexes)
        self.obs_values = [0] * len(self.df)
        d_len = len(self.mkt_data.df)
        time_limit = d_len - limit_to if limit_to else limit_to
        for D in range(MAX-1, 5, -1):
            # First only follow paths where D is recent enough.
            if self.peak_indexes[D] < time_limit:
                break
            else:
                if self.peak_indexes[D] in self.lows: 
                    # If D is a low point for a leg up
                    self.m_scan_from(D)
                else:
                    # D is a high point for a leg down.
                    self.w_scan_from(D)
        return self.get_patterns(formed=formed, only=only)
    
    def _match(self, retrace, stage, pattern_class, limit=None):
        """    
        """
        fit = set()
        for pattern, legs in self.PATTERNS_FAMILIES[pattern_class].items():
            if (limit is None or pattern in limit) and \
            legs[stage]['min'] <= retrace and retrace <= legs[stage]['max']: #('D' in stage or retrace <= legs[stage]['max']):
                # checking if the retrace is a D leg allows pattern completion 
                # to hit within the candle but not be limited to the peak
                fit.add(pattern)
        return fit
    
    def _is_abcd(self, A, B, C, D):
        """
        Finds the price range of each leg, calculates the retrace values and
        looks for a harmonic match
        """
        pattern = False
        AB = abs(self.peak_prices[A] - self.peak_prices[B])
        BC = abs(self.peak_prices[B] - self.peak_prices[C])
        # AD = abs(self.peak_prices[A] - self.peak_prices[D])
        CD = abs(self.peak_prices[C] - self.peak_prices[D])
        if 0.0 in (AB, BC): # double top or double bottom
            return pattern
        retraces = dict(
            ABC = BC/AB,
            BCD = CD/BC,
        )
        fits = self._match(retraces['ABC'], 'ABC', 'ABCD')
        if fits:
            pattern = self.create_pattern(
                (A, B, C, D),
                family = self.family,
                name = ', '.join(s for s in fits),
                retraces = retraces,
            )
            fits = self._match(retraces['BCD'], 'BCD', 'ABCD', limit=fits)
            if fits:
                # print(status)
                pattern.update(formed = True, name = ', '.join(s for s in fits))
        return pattern
    
    def _is_5_harmonic(self, X, A, B, C, D):
        """
        Finds the price range of each leg, calculates the retrace values and
        looks for a harmonic match
        """
        pattern = False
        XA = abs(self.peak_prices[X] - self.peak_prices[A])
        AB = abs(self.peak_prices[A] - self.peak_prices[B])
        BC = abs(self.peak_prices[B] - self.peak_prices[C])
        AD = abs(self.peak_prices[A] - self.peak_prices[D])
        XC = abs(self.peak_prices[X] - self.peak_prices[C])
        CD = abs(self.peak_prices[C] - self.peak_prices[D])
        if 0.0 in (XA, AB, BC, AD, XC, CD): # double top or double bottom
            return pattern
        retraces = dict(
            XAB = AB/XA,
            XAD = AD/XA,
            XCD = CD/XC,
            ABC = BC/AB,
            XAC = XC/XA,
            BCD = CD/BC
        )
        fits = self._match(retraces['XAB'], 'XAB', 'HARMONICS')
        fits = fits | self._match(retraces['XAB'], 'XAB', 'CYPHERS')
        fits = fits | self._match(retraces['XAB'], 'XAB', 'SHARKS')
        if fits:
            h_fits = fits & self._match(retraces['ABC'], 'ABC', 'HARMONICS', limit=fits)
            c_fits = fits & self._match(retraces['XAC'], 'XAC', 'CYPHERS', limit=fits)
            s_fits = fits & self._match(retraces['ABC'], 'ABC', 'SHARKS', limit=fits)
            fits = h_fits | c_fits | s_fits
            if fits:
                # BCD measurements are critical to harmonics, they account for fib time reaction too.
                if h_fits:
                    h_fits = fits & self._match(retraces['XAD'], 'XAD', 'HARMONICS', limit=h_fits)
                    h_fits = fits & self._match(retraces['BCD'], 'BCD', 'HARMONICS', limit=h_fits)
                if c_fits:
                    c_fits = fits & self._match(retraces['XCD'], 'XCD', 'CYPHERS', limit=c_fits)
                    # Cyphers got no BCD restriction
                if s_fits:
                    s_fits = fits & self._match(retraces['XCD'], 'XCD', 'SHARKS', limit=s_fits)
                    s_fits = fits & self._match(retraces['BCD'], 'BCD', 'SHARKS', limit=s_fits)
                pattern = self.create_pattern(
                    (X, A, B, C, D),
                    family = self.family,
                    name = ', '.join(s for s in fits),
                    retraces = retraces
                )
                fits = h_fits | c_fits | s_fits
                if fits:
                    # print(status)
                    # print(f"Pattern fits{fits}")
                    pattern.update(formed = True, name = ', '.join(s for s in fits))
        
        return pattern
    
    def get_patterns(self, formed=True, only=None):
        patterns = self.found
        if formed:
            patterns =  [p for p in patterns if p.formed]
        if only in ('bullish', 'bearish',):
            patterns = [p for p in patterns if p.direction == only]
        return patterns
                        
    def matrix_search(self, limit_to=0, formed=True, only='all'):
        """
        """
        