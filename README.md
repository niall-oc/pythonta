# pythonta
Python tool kit for TA

## What it is?
A simple set of libraries coded around yfinance and the binance-connector pip packages that detect harmonic patterns in stock trends.  The scans are published as images on your PC for you to review.

![This is an image](./images/BTCUSDT_1d.png)

## What it is not!
This library is **NOT FINANCIAL ADVICE!** This library can detect patterns and that is all.  Nobody in the world, not even with machine learning, can predict where a stock trend is going to move.  Anyone who says they can is a liar.  There is no certainty in fincial markets.  Please do not use this tool with the false assumption that it will tell you how to trade.  The tool will merely show you what trends have occured ( **past tense** )


## Installation

### Windows
Follow the video guide

[![Windows Installation Guide]](https://www.youtube.com/embed/WQ4W04JqZ7o)

https://youtu.be/WQ4W04JqZ7o

### Linux
Git clone the project then cd into the cloned folder - OR - download the project zip and use the command line to reach the project folder.

```git clone git@github.com:niall-oc/pythonta.git```

Setup a virtual env for dependencies ( my personal preference )

```
python3 -m virtualenv venv
source venv/bin/activate
```

Install all project dependencies

```pip3 install -r requirements.txt```

There are yaml config files for scanning assets on both binance and yahoo.  Open these files and set the output path to be the folder ( on your pc ) where you want pattern images installed. For example a user on a linux system may choose.

```output_path: /home/me/Pictures/Patterns```

### Command line parameters
```--symbol``` - Override the list of symbols in the yaml file and instead scan for only one symbol - ```--symbol MSFT```. Be sure that you can for a symbol that matches. _NOTE: the ```type: yahoo``` field in teh config file should match the assets you are scanning.  Crypto is on binance and stocks are on yahoo._

```--interval``` - Overide the interval eg 1h, 15m, 1d - ```--interval 1h```

```--formed``` - default is 1 to consider only formed paterns, 0 detects patterns forming - ```--formed 1``` is the default and ```--formed 0``` would also scan patterns that are forming ( of which there are many ).

```--limit_to``` - limit the search to patterns that completed in the last n candles, 0 for no limit -  ```--limit_to 10``` would limit the search to patterns that completed in the last 10 candles.  When coupled with ```--interval 1h``` this would mean patterns that completed in the last 10 hours.

```--only``` - Can be set to bullish, bearish or all. Default is all trend directions - ```--only all``` will scan for every trend direction. ```--only bullish``` for only bull patterns ( you optimist! ), ```--only bearish``` will show bearish patterns ( you know that shorting is being bullish in a bear market!

```--output_path``` - Changes the output folder. Directory must exist first, this forces you to double check what you are doing ;-) - ```--output_path /home/user/patterns/4hscans``` can print all your outputs to that folder.

## Using the tool

Using the command promt on windows or the shell on linux.

1. Linux ```cd /home/me/code/pythonta-main```. Windows ```cd c:\users\me\code\pythonta-main```
2. linux ```source venv/bin/activate```. Windows ```venv\Scripts\activate```
3. scan binance on the 1h ```python3 pattern_scanner.py binance_scanner.yaml --interval 1h```
4. scan AAPL for patterns that completed in the last week. ```python3 pattern_scanner.py yahoo_scanner.yaml --interval 1d --limit_to 7```
5. scan BTCUSDT for patterns that are forming right now. ```python3 pattern_scanner.py binance_scanner.yaml --interval 15m --limit_to 5```



## Bot posts scans to twitter
[Twitter bot](http://twitter.com/ZechsMarquie) is my twitter account which my bot posts to. Going forward I'm going to make this a daily thing with top crypto and stonks!

# Future thangs!
Patch this code base
- [ ] Patch - Remove Duplicate peaks created by argrelextrema so search is faster.

New code base
- [ ] Test first!  The new code base is test driven so that more can participate.
- [ ] Add hooks for storing patterns in mongodb for historical analysis.
- [ ] Add webserver for locally running UI
