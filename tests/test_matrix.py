import pytest
from rtta import FibonnaciMatrix
from market_data import CSV

def load_test_data():
    c = CSV()
    c.get_ticker_ohlc('ADAUSDT', '15m', 'data/ada.csv')
    c.set_peaks()
    fm = FibonnaciMatrix(c)
    fm.set_peak_type()
    return fm

@pytest.fixture
def fib_matrix():
    return load_test_data()

def test_peak_count(fib_matrix):
    peak_count = {1: 62, 2: 57, 3: 0}
    this_count = {1:0, 2:0, 3:0}
    for i in fib_matrix.peak_type:
        this_count[i] += 1
    assert(peak_count == this_count)
    print(fib_matrix.peak_type)

def test_matrix_data(fib_matrix):
    matrix = fib_matrix.build_matrix()
    for r in matrix:
        print(r)
        pass

if __name__ == "__main__":
    fm = load_test_data()
    test_peak_count(fm)
    test_matrix_data(fm)