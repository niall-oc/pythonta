from db.objects import Pattern, Position

def test_pattern():
    p = Pattern('ADAUSDT', '15m', 'binance', None, None, None, None, None, None, None, 'ticker')
    print(p)
    p.update(direction='bullish', name='crab', idx=[3, 6, 18, 23, 29], epoch_idx=[7126357621, 71265376215, 1234324, 12343214, 1234234])
    print(p)

if __name__ == '__main__':
    test_pattern()
