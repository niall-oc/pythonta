from market_data import CSV
from rtta import Divergence

def test_divergences():
    c = CSV()
    c.get_ticker_ohlc('ADAUSDT', '15m', 'tests/data/ada.csv')
    c.set_peaks()
    d = Divergence(c)
    d.search()
    assert(len(d.get_patterns()) == 113)
    print(d.get_patterns())
    p = d.get_patterns()[0]

if __name__ == '__main__':
    test_divergences()
