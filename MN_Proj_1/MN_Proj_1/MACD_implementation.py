def EMA(values, n):
    #exponential moving average with smoothing factor 2/(n+1), started from the first value
    #ema[i] = a*x[i] + (1-a)*ema[i-1], one pass over the data
    #(same result as pandas Series.ewm(span=n, adjust=False).mean())
    a = 2 / (n + 1)
    ema = [values[0]]
    for x in values[1:]:
        ema.append(a * x + (1 - a) * ema[-1])
    return ema

def MACD(data, m, n, s):
    close = list(data['Close'])
    dates = data.index
    #MACD line = EMA_m - EMA_n of the close price, signal line = EMA_s of the MACD line
    diff_values = [fast - slow for fast, slow in zip(EMA(close, m), EMA(close, n))]
    signal_values = EMA(diff_values, s)
    diff = [[diff_values[i], dates[i]] for i in range(len(close))]
    signal = [[signal_values[i], dates[i]] for i in range(len(close))]
    #macd[i] describes day i: 1 if the MACD line crossed above the signal line at that day's close (buy),
    #-1 if it crossed below (sell), 0 otherwise. It only uses closes up to day i.
    macd = [[0, dates[0], diff_values[0]]]
    for i in range(1, len(close)):
        if diff_values[i] > signal_values[i] and diff_values[i-1] <= signal_values[i-1]:
            macd.append([1, dates[i], diff_values[i]])
        elif diff_values[i] < signal_values[i] and diff_values[i-1] >= signal_values[i-1]:
            macd.append([-1, dates[i], diff_values[i]])
        else:
            macd.append([0, dates[i], diff_values[i]])
    return macd, diff, signal
