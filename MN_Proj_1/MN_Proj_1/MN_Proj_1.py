import pandas as pd
import numpy as np
import graphing as graph
import simulation as sim
import MACD_implementation as macd
import random

# Read data from file
import pandas as pd
#import data from date X to date Y
X = '2021-01-01'
Y = '2026-01-01'
data = pd.read_csv('data.csv')
data = data.set_index('Date')
data.index = pd.to_datetime(data.index)
data = data.loc[X:Y]
data.index.name = 'Date'
data.shape
data.head(3)
data.tail(3)
#graph data
graph.graph_data(data)
macd, diff, signal = macd.MACD(data, 12, 26, 9)
#graph the macd
graph.plot_MACD(macd, diff, signal, data)
#start the simulation

capital, diff = sim.simulation(10000, data, macd)
#count how many transactions generated profit and how many loses 
gains = 0
loses = 0
for t in diff:
    if t>0:
        gains += 1
    else:
        loses += 1
#print formated results:
print("Total transactions: ", gains + loses)
print("Total gains: ", gains)
print("Total loses: ", loses)  
print(capital)

#generate a random number between 0 and length of macd
random_index = random.randint(0, len(macd)-1)
#select a new dataset from the the date of macd[random_index] to the date of macd[random index + 8]
X = macd[random_index][1]
i=1
j=0
while (j<8):
    if(macd[random_index+i]==0):
        i+=1
    else:
        i+=1
        j+=1
Y = macd[random_index + i][1]
data = data.loc[X:Y]
data.index.name = 'Date'
data.shape
data.head(3)
data.tail(3)

#find indexes of macd with date X and Y
X_index = macd.index.get_loc(X)
Y_index = macd.index.get_loc(Y)
#create subset of macd, signal and diff from date X to Y
macd_subset = macd[X_index:Y_index]
diff_subset = diff[X_index:Y_index]
signal_subset = signal[X_index:Y_index]

#graph data and macd on same plot
graph.graph_data(data)
graph.plot_MACD(macd_subset, diff_subset, signal_subset, data)




