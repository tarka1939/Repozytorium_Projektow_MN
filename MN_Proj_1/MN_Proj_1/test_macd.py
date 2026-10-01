#checks for the MACD implementation and the trading simulation
#run with: python test_macd.py   (or: python -m pytest test_macd.py)
import os
import numpy as np
import pandas as pd
import MACD_implementation as macd_impl
import simulation as sim

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.csv')

def load_data():
    return pd.read_csv(DATA_FILE, index_col='Date', parse_dates=True).loc['2021-01-01':'2026-01-01']

def test_ema_matches_pandas():
    values = list(np.random.default_rng(0).normal(100, 5, 500))
    for n in (3, 12, 26):
        expected = pd.Series(values).ewm(span=n, adjust=False).mean()
        assert np.allclose(macd_impl.EMA(values, n), expected)

def test_macd_lines_match_pandas():
    data = load_data()
    macd, diff, signal = macd_impl.MACD(data, 12, 26, 9)
    close = data['Close']
    line = close.ewm(span=12, adjust=False).mean() - close.ewm(span=26, adjust=False).mean()
    assert np.allclose([d[0] for d in diff], line)
    assert np.allclose([s[0] for s in signal], line.ewm(span=9, adjust=False).mean())
    assert len(macd) == len(data) and macd[5][1] == data.index[5]

def test_signals_only_use_past_prices():
    #the signal for day k must not change when the days after k are removed
    data = load_data()
    full, _, _ = macd_impl.MACD(data, 12, 26, 9)
    for k in (50, 300, 777):
        prefix, _, _ = macd_impl.MACD(data.iloc[:k + 1], 12, 26, 9)
        assert [m[0] for m in prefix] == [m[0] for m in full[:k + 1]]

def test_simulation_has_no_look_ahead():
    #changing prices after day k must not change the portfolio value up to day k
    data = load_data()
    k = 600
    changed = data.copy()
    rng = np.random.default_rng(1)
    for column in ('Open', 'High', 'Low', 'Close'):
        changed.iloc[k + 1:, changed.columns.get_loc(column)] *= rng.uniform(0.5, 1.5, len(data) - k - 1)
    history, _ = sim.simulation(10000, data, macd_impl.MACD(data, 12, 26, 9)[0])
    history_changed, _ = sim.simulation(10000, changed, macd_impl.MACD(changed, 12, 26, 9)[0])
    assert history[:k + 1] == history_changed[:k + 1]

def test_order_is_filled_at_next_open():
    dates = pd.date_range('2024-01-01', periods=5)
    data = pd.DataFrame({'Open': [10.0, 20.0, 40.0, 50.0, 80.0], 'Close': [11.0, 21.0, 41.0, 51.0, 81.0]}, index=dates)
    #buy signal at the close of day 1, sell signal at the close of day 3
    macd = [[0, dates[0], 0], [1, dates[1], 0], [0, dates[2], 0], [-1, dates[3], 0], [0, dates[4], 0]]
    history, transactions = sim.simulation(1000, data, macd, fee=0.01)
    stock = 800 * 0.99 / 40.0             #bought at day 2's open
    cash = 200 + stock * 0.8 * 80.0 * 0.99 #sold at day 4's open
    assert np.isclose(history[1][2], 1000)   #nothing happens on the signal day itself
    assert np.isclose(history[2][1], stock * 41.0)
    assert np.isclose(history[4][0], cash)
    assert np.isclose(history[4][2], cash + stock * 0.2 * 81.0)
    assert len(transactions) == 2

def test_buy_and_hold():
    data = load_data()
    hold = sim.buy_and_hold(10000, data)
    assert np.isclose(hold[-1], 10000 / data['Open'].iloc[0] * data['Close'].iloc[-1])

if __name__ == '__main__':
    tests = [f for name, f in sorted(globals().items()) if name.startswith('test_')]
    for test in tests:
        test()
        print('ok  ', test.__name__)
    print(f'{len(tests)} tests passed')
