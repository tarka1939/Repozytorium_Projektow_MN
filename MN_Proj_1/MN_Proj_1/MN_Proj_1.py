import random
import pandas as pd
import graphing as graph
import simulation as sim
import MACD_implementation as macd_impl

#import data from date X to date Y
X = '2021-01-01'
Y = '2026-01-01'
STARTING_CAPITAL = 10000
FEE = 0.0 #commission per transaction as a fraction of its value, e.g. 0.001 = 0.1%
data = pd.read_csv('data.csv', index_col='Date', parse_dates=True)
data = data.loc[X:Y]
#graph data
graph.graph_data(data)
macd, diff, signal = macd_impl.MACD(data, 12, 26, 9)
#graph the macd
graph.plot_MACD(macd, diff, signal, data)

#start the simulation and compare it with buying once and holding
history, transactions = sim.simulation(STARTING_CAPITAL, data, macd, FEE)
hold = sim.buy_and_hold(STARTING_CAPITAL, data, FEE)
graph.plot_simulation(data.index, history, hold)
#count how many transactions increased the total value since the previous one
gains = sum(1 for t in transactions if t > 0)
loses = len(transactions) - gains
#print formated results:
print(f"Period: {data.index[0].date()} to {data.index[-1].date()} ({len(data)} trading days)")
print("Total transactions: ", len(transactions))
print("Total gains: ", gains)
print("Total loses: ", loses)
print(f"Final value, MACD strategy: {history[-1][2]:.2f} (cash {history[-1][0]:.2f}, stock {history[-1][1]:.2f})")
print(f"Final value, buy and hold:  {hold[-1]:.2f}")

#zoom in on a random stretch of the chart from one crossover to the 8th crossover after it
crossovers = [i for i in range(len(macd)) if macd[i][0] != 0]
first = random.randrange(len(crossovers) - 8)
X_index = crossovers[first]
Y_index = crossovers[first + 8] + 1
data_subset = data.iloc[X_index:Y_index]
#graph data and macd on same plot
graph.graph_data(data_subset)
graph.plot_MACD(macd[X_index:Y_index], diff[X_index:Y_index], signal[X_index:Y_index], data_subset)
