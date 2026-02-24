from MACD_implementation import MACD
from graphing import plot_simulation
import pandas as pd
def simulation(starting_capital, data, macd):
    #use macd to simulate buying and selling of stock
    #buy when macd crosses signal line from below
    #sell when macd crosses signal line from above
    #initialise variables
    capital = starting_capital
    stock = 0
    stock_value = 0
    lttv = capital #last transaction total value
    total_value = capital
    #simulation constants
    percent_bought = 80
    percent_sold = 80
    #difference between transactions total value
    diff=[]
    #iterate through data
    simulation = []
    for i in range(1, len(macd)):
        if macd[i][0] == 1:
            #buy stock
            stock = stock + capital*percent_bought/100/ data['Open'][i]
            capital = capital - capital*percent_bought/100
            stock_value = stock * data['Close'][i]
            total_value = capital + stock_value
            diff.append(total_value - lttv) 
            lttv = total_value
        elif macd[i][0] == -1:
            #sell stock
            capital = capital + stock*percent_sold/100*data['Open'][i]
            stock = stock - stock*percent_sold/100
            stock_value = stock * data['Close'][i]
            total_value = capital + stock_value
            diff.append(total_value - lttv) 
            lttv = total_value
        stock_value = stock * data['Close'][i]
        total_value = capital + stock_value
        simulation.append([capital,stock_value, total_value])    
    
    plot_simulation(simulation)
    return capital, diff