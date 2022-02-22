# pythonta
Python tool kit for TA

This package is a simple set of commandline tools that can used to scan OHLC stock ticker trends for harmonic patterns and divergences.  For more information on these patterns see harmonictrader.com.

## Example
```python3 pattern_scanner.py yahoo_scanner.json```

```python3 pattern_scanner.py yahoo_scanner.json --interval 15m --limit_to 20 --only bullish```

## Installation

Follow the video guide
<iframe width="560" height="315" src="https://www.youtube.com/embed/WQ4W04JqZ7o" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

https://youtu.be/WQ4W04JqZ7o

Git clone the project then cd into the cloned folder - OR - download the project zip and use the command line to reach the project folder.

Install all project dependencies

```pip3 install -r requirements.txt```

There are yaml config files for scanning assets on both binance and yahoo.  Open these files and set the output path to be the folder ( on your pc ) where you want pattern images installed. For example a user on a linux system may choose.

```
 --symbol,    Overide the symbols to be one symbol ie, --symbol MSFT
 --interval,    Overide the interval eg 1h, 15m, 1d  ie, --interval 1h
 --formed, default is 1 to consider only formed paterns, 0 detects patterns forming.
 --limit_to, limit the search to patterns that completed in the las n candles, 0 for no limit.  --limit_to 10
 --only, Can be set to bullish, bearish or all. Default is all trend directions --only all
 --output_path, Changes the output folder. Directory must exist first, this forces you to double check what you are doing ;-)
 ```
