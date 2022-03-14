#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:14:00 2021

@author: xual
"""
from rtta.harmonics import HarmonicPatterns
from rtta.head_shoulders import HeadShoulders
from rtta.divergence import Divergence
from market_data.binance_data import Binance
from market_data.yahoo_data import Yahoo
from market_data.plotter import Plotter
import argparse
import os
import yaml
import datetime
import time
import sys
from copy import deepcopy
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config json file for polling binance endpoints")
    parser.add_argument("--symbol", help="Overide the symbols to be one symbol i.e. --symbol binance:BTCUSDT")
    parser.add_argument("--interval", help="Overide the interval eg 1h, 15m, 1d")
    parser.add_argument("--formed", help="default is 1 to consider only formed paterns, 0 detects patterns forming")
    parser.add_argument("--limit_to", help="limit the search to patterns that completed in the las n candles, 0 for no limit")
    parser.add_argument("--only", help="Can be set to bullish, bearish or all. Default is all trend directions")
    parser.add_argument("--output_path", help="Changes the output folder. Directory must exist first, this forces you to double check what you are doing ;-)")
    parser.add_argument("--markets", help="To use a specific list of markets and symbols contained in a yaml file.")
    parser.add_argument("--harmonics", help="To use a specific set of retrace values for harmonics contained in a yaml file. Families include Sharks, cyphers, harmonics and ABCDs")
    parser.add_argument("--pattern_variance", help="The percentage of variance applied to harmonic patterns. eg. 0.03 adds 3% either side of a 1.618 retrace")
    parser.add_argument("--peak_spacing", help="Peak finding sensitivity.  The lower the number the more peaks are found. This can increase the search time and add too much noise")
    parser.add_argument("--log_level", help="Override the log_level in settings.yaml")
    
    args = parser.parse_args()
    configuration  = yaml.load(open(args.config, "r"), Loader=yaml.FullLoader)
    
    if args.symbol:
        market, symbol = args.symbol.split(':')
        configuration['markets'] = {market: [symbol]}
    elif args.markets:
        configuration['markets'] = yaml.load(open(args.markets, "r"), Loader=yaml.FullLoader)
    else:
        configuration['markets'] = yaml.load(open(configuration['markets'], "r"), Loader=yaml.FullLoader)
    if args.interval:
        configuration['interval'] = args.interval
    if args.formed:
        configuration['formed'] = bool(int(args.formed))
    if args.limit_to:
        configuration['limit_to'] = int(args.limit_to)
    if args.only:
        configuration['only'] = args.only
    if args.output_path:
        configuration['output_path'] = args.output_path
    if args.harmonics:
        configuration['harmonics'] = args.harmonics
    if args.pattern_variance:
        configuration['pattern_variance'] = float(args.pattern_variance)
    if args.peak_spacing:
        configuration['peak_spacing'] = int(args.peak_spacing)
    if args.log_level:
        logger.info(f"flag log level is set to {args.log_level}")
        configuration['log_level'] = args.log_level

    if configuration['harmonics']:
        configuration['harmonics'] = yaml.load(open(configuration['harmonics'], "r"), Loader=yaml.FullLoader)
    return configuration

def debug_args(debug_settings):
    configuration  = yaml.load(open(debug_settings, "r"), Loader=yaml.FullLoader)
    configuration['markets'] = yaml.load(open(configuration['markets'], "r"), Loader=yaml.FullLoader)
    if configuration['harmonics']:
        configuration['harmonics'] = yaml.load(open(configuration['harmonics'], "r"), Loader=yaml.FullLoader)
    return configuration

def scan_patterns(configuration, market, symbols):
    if market.lower() == "yahoo":
        mkt = Yahoo
        kw_args = dict(period=configuration["period"])
    elif market.lower() == "binance":
        mkt = Binance
        kw_args = dict(num_ticks=configuration["num_ticks"])
    else:
        raise ValueError(f"Markets currently supported are binance or yahoo. You did not use one of these!")
    m = mkt()
    for symbol in symbols:
        logger.info(f"Starting symbol {symbol}")
        # load stock ticker data.
        limit_to = configuration['limit_to'] or 0
        
        m.get_ticker_ohlc(symbol, configuration["interval"], **kw_args)

        if not len(m.df):
            continue # No data no go
        
        m.post_ticker_setup(peak_spacing=configuration['peak_spacing']) 

        # scan for harmonics and divergences.
        patterns = deepcopy(configuration['harmonics']) # Beware of references vs copies of data
        h = HarmonicPatterns(m, variance=configuration["pattern_variance"], patterns=patterns)
        harmonic_patterns = h.search(
            limit_to=limit_to, 
            formed=configuration['formed'],
            only=configuration['only']
        )
        # print(harmonic_patterns)
        d = Divergence(m)
        divergences = d.search(limit_to=limit_to)
        
        m.merge_obs(h.obs_values)
        m.merge_obs(d.obs_values)
        hs = HeadShoulders(m)
        hands_patterns = hs.search(limit_to=limit_to)        
        
        # Find time point of newest D leg and report as forming or formed.
        
        # Plot image
        if harmonic_patterns:
            logger.debug(str(harmonic_patterns[-1]))
            p = Plotter(m, yahoo=bool(market.lower() == "yahoo"))
            p.add_harmonic_plots(harmonic_patterns)
            p.add_divergence_plots(divergences)
            p.add_head_shoulders_plots(hands_patterns)
            p.add_peaks(h)
            p.add_obs(m.obs_values)
            filename = f"{symbol}_{configuration['interval']}.png"
            image_path = os.path.join(configuration['output_path'], filename)
            p.save_plot_image(image_path)
            logger.info(f"saved {image_path}")
                
        time.sleep(configuration['sleep_time'])

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    # Runtime
    configuration = handle_args()
    # VS CODE debugging!! :-|
    # configuration = debug_args("debug_settings.yaml")

    # Logging preferences
    handler.setLevel(getattr(logging, configuration['log_level']))
    logger.setLevel(handler.level)

    for market, symbols in configuration['markets'].items():
        scan_patterns(configuration, market, symbols)
    print(datetime.datetime.now() - start_time)

   
