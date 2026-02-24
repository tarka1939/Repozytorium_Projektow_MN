#Source: https://medium.com/@armand_aguilar/macd-with-python-9ddf2548dfb5 only for demonstration and debug purposes
import yfinance as yf
import matplotlib.pyplot as plt
import ta
import pandas as pd
X = '2021-01-01'
Y = '2026-01-01'
data = pd.read_csv('data.csv')
data = data.set_index('Date')
data.index = pd.to_datetime(data.index)
data = data.loc[X:Y]
data.head(10)
macd_object = ta.trend.MACD(data['Close'])
data['MACD'] = macd_object.macd()
data['MACD_Signal'] = macd_object.macd_signal()
data['MACD_Diff'] = macd_object.macd_diff()
data.tail()
plt.figure(figsize=(14,7))

#Plotting Close Price
plt.subplot(2,1,1)
plt.plot(data['Close'],label='Close Price')
plt.title('Microsoft Stock Price adn MACD')
plt.legend()

#Plottinf MACD
plt.subplot(2,1,2)
plt.plot(data['MACD'],label='MACD Line',color='blue')
plt.plot(data['MACD_Signal'], label='Signal Line', color='red')
plt.bar(data.index, data['MACD_Diff'],label='Histogram',color='grey',alpha=0.5)
plt.legend()

plt.show()
# Identify starting points of bullish and bearish trends
data['Bullish_Run_Start'] = (data['MACD'] > data['MACD_Signal']) & (data['MACD'].shift(1) <= data['MACD_Signal'].shift(1))
data['Bearish_Run_Start'] = (data['MACD'] < data['MACD_Signal']) & (data['MACD'].shift(1) >= data['MACD_Signal'].shift(1))

# Plot
plt.figure(figsize=(14, 10))

#Plot Close Price
plt.subplot(2, 1, 1)
plt.plot(data['Close'], label='Close Price')
plt.scatter(data.index[data['Bullish_Run_Start']], data['Close'][data['Bullish_Run_Start']], marker='^', color='g', label='Start Bullish Run')
plt.scatter(data.index[data['Bearish_Run_Start']], data['Close'][data['Bearish_Run_Start']], marker='v', color='r', label='Start Bearish Run')
plt.title('Microsoft Stock Price and MACD')
plt.legend()


# Identify bullish and bearish crossover points
data['Bullish_Crossover'] = (data['MACD'] > data['MACD_Signal']) & (data['MACD'].shift(1) <= data['MACD_Signal'].shift(1))
data['Bearish_Crossover'] = (data['MACD'] < data['MACD_Signal']) & (data['MACD'].shift(1) >= data['MACD_Signal'].shift(1))

# Plot
plt.figure(figsize=(14, 10))

# Plot MACD
plt.subplot(2, 1, 2)
plt.plot(data['MACD'], label='MACD Line', color='blue', alpha=0.5)
plt.plot(data['MACD_Signal'], label='Signal Line', color='red', alpha=0.5)
plt.bar(data.index, data['MACD_Diff'], label='Histogram', color='grey', alpha=0.5)

# Markers for bullish and bearish crossover
plt.scatter(data.index[data['Bullish_Crossover']], data['MACD'][data['Bullish_Crossover']], marker='^', color='g', label='Bullish Crossover')
plt.scatter(data.index[data['Bearish_Crossover']], data['MACD'][data['Bearish_Crossover']], marker='v', color='r', label='Bearish Crossover')

plt.legend()
plt.show()