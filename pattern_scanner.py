#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:14:00 2021

@author: xual
"""

import argparse
import yaml
import datetime
import time
from rtta.harmonics import HarmonicPatterns
from rtta.head_shoulders import HeadShoulders
from rtta.divergence import Divergence
from market_data.binance_data import Binance
from market_data.yahoo_data import Yahoo
from market_data.plotter import Plotter

# In your terminal please set your environment variables by running the following lines of code.
# export 'CONSUMER_KEY'='<your_consumer_key>'
# export 'CONSUMER_SECRET'='<your_consumer_secret>'
def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config json file for polling binance endpoints")
    parser.add_argument("--symbol", help="Overide the symbols to be one symbol")
    parser.add_argument("--interval", help="Overide the interval eg 1h, 15m, 1d")
    parser.add_argument("--formed", help="default is 1 to consider only formed paterns, 0 detects patterns forming")
    parser.add_argument("--limit_to", help="limit the search to patterns that completed in the las n candles, 0 for no limit")
    args = parser.parse_args()
    configuration  = yaml.load(open(args.config, "r"), Loader=yaml.FullLoader)
    configuration['safe'] = True
    if args.symbol:
        configuration['symbols'] = [args.symbol]
    if args.interval:
        configuration['interval'] = args.interval
    if args.formed:
        configuration['formed'] = bool(int(args.formed))
    if args.limit_to:
        configuration['limit_to'] = int(args.limit_to)
        
    return configuration

def scan_patterns(configuration):
    if configuration["type"].lower() == "yahoo":
        mkt = Yahoo
        kw_args = dict(period=configuration["period"])
    elif configuration["type"].lower() == "binance":
        mkt = Binance
        kw_args = dict(num_ticks=configuration["num_ticks"])
    else:
        raise ValueError(f"configuration type {configuration['type']} is unknown!")
    m = mkt()
    for symbol in configuration['symbols']:
        print(f"Starting symbol {symbol}")
        # load stock ticker data.
        time_limit = configuration['limit_to'] or 0
        
        m.get_ticker_ohlc(symbol, configuration["interval"], **kw_args)
        m.set_peaks(peak_spacing=configuration['peak_spacing'])
        # scan for harmonics and divergences.
        h = HarmonicPatterns(m, variance=configuration["pattern_variance"])
        h.search(
            time_limit=time_limit, 
            formed=configuration['formed'],
            only=configuration['only']
        )
        harmonic_patterns = h.get_patterns(formed=configuration['formed'])
        
        d = Divergence(m)
        divergences = d.search(time_limit=time_limit)
        
        m.merge_obs(h.obs_values)
        m.merge_obs(d.obs_values)
        hs = HeadShoulders(m)
        hands_patterns = hs.search(time_limit=time_limit)        
        
        # Find time point of newest D leg and report as forming or formed.
        
        # Plot image
        if harmonic_patterns:
            p = Plotter(m)
            p.add_harmonic_plots(harmonic_patterns)
            p.add_divergence_plots(divergences)
            p.add_head_shoulders_plots(hands_patterns)
            p.add_peaks(h)
            p.add_obs(m.obs_values)
            filename = f"{symbol}_{configuration['interval']}.png"
            image_path = f"{configuration['output_path']}/{filename}"
            p.save_plot_image(image_path)
                
        time.sleep(configuration['sleep_time'])

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    configuration = handle_args()
    scan_patterns(configuration)
    print(datetime.datetime.now() - start_time)

   
