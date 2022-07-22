#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import yaml
import datetime
import sys
import logging

from finviz.screener import Screener


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config json file for finviz_config")
    parser.add_argument("--filter_query", help="Changes the filter query to use.")
    parser.add_argument("--output_yaml", help="Changes the output yaml file.")
    parser.add_argument("--log_level", help="Override the log_level in settings.yaml")
    
    args = parser.parse_args()
    configuration  = yaml.load(open(args.config, "r"), Loader=yaml.FullLoader)
    
    if args.filter_query:
        configuration['filter_query'] = args.filter_query
    else:
        configuration['filter_query'] = configuration.get('filter_query')
    if args.output_yaml:
        configuration['output_yaml'] = args.output_yaml
    if args.log_level:
        logger.info(f"flag log level is set to {args.log_level}")
        configuration['log_level'] = args.log_level

    return configuration


def finviz_populate(configuration):
    filters_query = configuration.get("filter_query")
    output_yaml = configuration.get("output_yaml", "finviz_found_yahoo.yaml")
    if filters_query is None:
        raise ValueError(f"filter_query must be defined!")

    filters = filters_query.split(",")
    # table = "Performance"
    table = "Custom"
    columns_s = "0,1,2,3,4,5,6,7,65,66,67,68"
    columns = columns_s.split(",")
    stock_list = Screener(filters=filters, table=table, order="-marketcap", custom=columns)
    symbols = [str(s["Ticker"]) for s in stock_list]
    
    yaml_struct = {"yahoo": symbols}

    with open(output_yaml, 'w') as file:
        yaml.dump(yaml_struct, file)    


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    configuration = handle_args()

    handler.setLevel(getattr(logging, configuration.get('log_level', "INFO")))
    logger.setLevel(handler.level)

    finviz_populate(configuration)
    print(datetime.datetime.now() - start_time)

   
