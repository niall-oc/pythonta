from market_data import CSV
from rtta import HeadShoulders

def test_head_shoulders():
    c = CSV()
    c.get_ticker_ohlc('ADAUSDT', '15m', 'tests/data/ada.csv')
    c.set_peaks()
    h = HeadShoulders(c)
    h.search()
    assert(len(h.get_patterns()) == 1628)
    print(h.get_patterns())

if __name__ == '__main__':
    test_head_shoulders()
