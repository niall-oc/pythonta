from market_data import CSV
from rtta import HarmonicPatterns

def test_harmonics():
    c = CSV()
    c.get_ticker_ohlc('ADAUSDT', '15m', 'tests/data/ada.csv')
    c.set_peaks()
    h = HarmonicPatterns(c)
    h.search()
    assert(len(h.get_patterns()) == 30)
    print(h.get_patterns())

if __name__ == '__main__':
    test_harmonics()
