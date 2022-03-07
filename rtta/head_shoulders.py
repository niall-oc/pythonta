#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 16:01:00 2021

@author: xual
"""

from .ta_base import TABase

class HeadShoulders(TABase):
    
    def __init__(self, mkt_data):
        """
        """
        super(HeadShoulders, self).__init__(mkt_data)
        self.family = 'head and shoulders'
        
    
    def is_neckline_formed(self, p1, p2, p3, p4, bullish=True):
        """
        Find the slope of the line between 2 points, needed for Head and shoulders
        type patterns.

        Parameters
        ----------
        p1 : TYPE
            DESCRIPTION.
        p2 : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        status = False
        # First get the equation of the slope at the neck.
        m = (self.peak_prices[p3]-self.peak_prices[p2]) / (self.peak_indexes[p3]-self.peak_indexes[p2]) # Equation of a slope
        predicted_start_price = self.peak_prices[p2] - ((self.peak_indexes[p2]-self.peak_indexes[p1]) * m)
        
        predicted_end_price = self.peak_prices[p3] + ((self.peak_indexes[p4]-self.peak_indexes[p3]) * m)
        
        if bullish and self.peak_prices[p1] > predicted_start_price:
            status = dict(stage='forming')
            if self.peak_prices[p4] > predicted_end_price:
                status['stage'] = 'formed'
        elif not bullish and self.peak_prices[p1] < predicted_start_price:
            status = dict(stage='forming')
            if self.peak_prices[p4] < predicted_end_price:
                status['stage'] = 'formed'
        if status:
            # must walk the neckline and ensure it is not broken by other prices
            for p in range(p1, p4):
                tick = self.df.iloc[p]
                if p < p3:
                    predicted_line_price = self.peak_prices[p] - ((self.peak_indexes[p3]-self.peak_indexes[p]) * m)
                else:
                    predicted_line_price = self.peak_prices[p] + ((self.peak_indexes[p]-self.peak_indexes[p3]) * m)
                
                if (bullish and predicted_line_price < tick[self.mkt_data.HIGH]) or\
                   (not bullish and predicted_line_price > tick[self.mkt_data.LOW]) :
                    # if the neck line is pierced the pattern is invalid
                    return False
        return status
        
    
    def bearish_scan_from(self, T):
        """
        From the final point in the pattern we can traverse from T back to 0
        and scan each peak to see if a pattern fits.
        
        As head and shoulders patterns are found they are pussed into an array

        Parameters
        ----------
        D : int
            Index of the final point in the M pattern.

        Returns
        -------
        None.

        """
        for D in range(T-1, -1, -1):
            if self.peak_prices[D] < self.peak_prices[T]:
                break # Let C become D
            elif self.peak_indexes[D] in self.highs and \
                self.is_valid_swing(D, T, up=False): # C to D must be a downward leg
                ##print(f"got here {__name__} D:{D}, T:{T}")
                for C in range(D-1, -1, -1):

                    if self.peak_prices[C] > self.peak_prices[D]:
                        break # Let C become D
                    elif self.peak_indexes[C] in self.lows and \
                        self.is_valid_swing(C, D, up=True): # C to D must be a upward leg
                        #print(f"got here {__name__} C:{C}, D:{D}")
                        for B in range(C-1, -1, -1):
            
                            if self.peak_prices[B] < self.peak_prices[C]:
                                break # let C become B
                            elif self.peak_indexes[B] in self.highs and \
                                self.peak_prices[B] > self.peak_prices[D] and\
                                self.is_valid_swing(B, C, up=False): # B to C must be an downward leg
                                #print(f"got here {__name__} B:{B}, C:{C}")
                                for A in range(B-1, -1, -1):
                                    
                                    if self.peak_prices[A] > self.peak_prices[B]: # Not a bull pattern
                                        break # Let A become B
                                    elif self.peak_indexes[A] in self.lows and \
                                        self.is_valid_swing(A, B, up=True): # A to B must be a downward leg
                                        #print(f"got here {__name__} A:{A}, B:{B}")
                                        for X in range(A-1, -1, -1):
                                            
                                            if self.peak_prices[X] < self.peak_prices[A]: # Not a bull pattern
                                                break # let X become A
                                            elif self.peak_indexes[X] in self.highs and \
                                                self.peak_prices[X] < self.peak_prices[B] and \
                                                self.is_valid_swing(X, A, up=False):
                                                # print(f"got here {__name__} X:{X}, A:{A}")
                                                for O in range(X-1, -1, -1):
                                                    if self.peak_prices[O] > self.peak_prices[X]: # Not a bull pattern
                                                        break # Let A become B
                                                    elif self.peak_indexes[O] in self.lows and \
                                                        self.is_valid_swing(O, X, up=True) and \
                                                        self.is_neckline_formed(O, A, C, T, bullish=False):  
                                                        self.add_pattern([O, X, A, B, C, D, T], 'bearish') 
                                                        
    def bullish_scan_from(self, T):
        """
        Is there a W pattern where the middle peak is the highest, indicating
        a bearish head and shoulders is forming.
        
        As W patterns are found they are appended into an array

        Parameters
        ----------
        D : int
            Index of the final point in the M pattern.

        Returns
        -------
        None.

        """
        for D in range(T-1, -1, -1):

            if self.peak_prices[D] > self.peak_prices[T]:
                break # Let C become D
            elif self.peak_indexes[D] in self.lows and \
                self.is_valid_swing(D, T, up=True): # C to D must be a downward leg
                
                for C in range(D-1, -1, -1):

                    if self.peak_prices[C] < self.peak_prices[D]:
                        break # Let C become D
                    elif self.peak_indexes[C] in self.highs and \
                        self.is_valid_swing(C, D, up=False): # C to D must be a upward leg
                        
                        for B in range(C-1, -1, -1):
            
                            if self.peak_prices[B] > self.peak_prices[C]:
                                break # let C become B
                            elif self.peak_indexes[B] in self.lows and \
                                self.peak_prices[B] < self.peak_prices[D] and\
                                self.is_valid_swing(B, C, up=True): # B to C must be an downward leg
                                
                                for A in range(B-1, -1, -1):
                                    
                                    if self.peak_prices[A] < self.peak_prices[B]: # Not a bull pattern
                                        break # Let A become B
                                    elif self.peak_indexes[A] in self.highs and \
                                        self.is_valid_swing(A, B, up=False): # A to B must be a downward leg
                                        
                                        for X in range(A-1, -1, -1):
                                            
                                            if self.peak_prices[X] > self.peak_prices[A]: # Not a bull pattern
                                                break # let X become A
                                            elif self.peak_indexes[X] in self.lows and \
                                                self.peak_prices[X] > self.peak_prices[B] and \
                                                self.is_valid_swing(X, A, up=True):
                                                
                                                for O in range(X-1, -1, -1):
                                                    if self.peak_prices[O] < self.peak_prices[X]: # Not a bull pattern
                                                        break # Let A become B
                                                    elif self.peak_indexes[O] in self.highs and \
                                                        self.is_valid_swing(O, X, up=False) and \
                                                        self.is_neckline_formed(O, A, C, T, bullish=True):    
                                                        self.add_pattern([O, X, A, B, C, D, T], 'bullish')    
    
    def add_pattern(self, idx, direction):
        pattern = self.create_pattern(
            idx,
            direction = direction,
            formed = True,
            family = self.family,
            name = self.family,
        )
        self.found.append(pattern)

    def search(self, time_limit=0, formed=True, peak_spacing=6, only='all'):
        """
        Working backwards through the trend until while the D leg is still later
        than the time limit. Scan for bull if D is a low or bear patterns if D
        is a high.
        
        """
        MAX = len(self.peak_indexes)
        d_len = len(self.mkt_data.df)
        time_limit = d_len - time_limit if time_limit else time_limit
        for T in range(MAX-1, -1, -1):
            # First only follow paths where D is recent enough.
            if self.peak_indexes[T] < time_limit:
                break # stop the search
            else:
                if self.peak_indexes[T] in self.lows:
                    # print("got bear here {__name__}")
                    # If T is a low point for a leg up
                    self.bearish_scan_from(T)
                else:
                    # print("got bull here {__name__}")
                    # D is a high point for a leg down.
                    self.bullish_scan_from(T)
        return self.get_patterns(formed=formed, only=only)

    def get_patterns(self, formed=True, only=None):
        patterns = self.found
        if formed:
            patterns =  [p for p in patterns if p.formed]
        if only in ('bullish', 'bearish',):
            patterns = [p for p in patterns if p.direction == only]
        return patterns
