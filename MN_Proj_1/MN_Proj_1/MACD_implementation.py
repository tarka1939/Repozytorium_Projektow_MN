import pandas as pd
def MACD(data, m, n, s):
    i=0
    diff = [] 
    signal = []
    for d in data['Close']:
        diff.append([MACD_diff(data['Close'], m, n, i),data.index[i]])
        #diff with no timestamp
        diff_temp = []
        for j in range(len(diff)):
            diff_temp.append(diff[j][0])
        signal.append([MACD_signal(diff_temp, s, i),data.index[i]])
        i+=1
    #combine diff and signal into one array
    macd_temp = []
    for i in range(len(diff)):
        macd_temp.append([diff[i][0],signal[i][0]])
    #find when diff crosses signal and mark it in array as -1 or 1 for buy or sell
    macd = []
    for i in range(1, len(macd_temp)):
        if macd_temp[i][0] > macd_temp[i][1] and macd_temp[i-1][0] <= macd_temp[i-1][1]:
            macd.append([1,data.index[i],macd_temp[i][0]])
        elif macd_temp[i][0] < macd_temp[i][1] and macd_temp[i-1][0] >= macd_temp[i - 1][1]:
            macd.append([-1,data.index[i],macd_temp[i][0]])
        else:
            macd.append([0,data.index[i],macd_temp[i][0]])
    return macd, diff, signal
def MACD_signal(diff, s, i):
    return EMA_n(s, diff, i,0)
    
def MACD_diff(data, m, n, i):
    return EMA_n(m, data, i,0) - EMA_n(n, data, i,0)

def EMA_n(n, data, i, r):
    #max recursion depth = 50
    if r == 50:
        return data[i]
    if i==0:
        return data[0]
    a = 2 / (n + 1)
    x = data[i]
    value = a * x + (1 - a) * EMA_n(n, data, i - 1, r+1)
    return value