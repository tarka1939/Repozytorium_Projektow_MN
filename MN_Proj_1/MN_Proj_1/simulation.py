def simulation(starting_capital, data, macd, fee=0.0):
    #use macd to simulate buying and selling of stock
    #buy when macd crosses signal line from below
    #sell when macd crosses signal line from above
    #a crossover is only known after the day's close, so the order is filled at the NEXT day's open
    #fee: commission as a fraction of each transaction's value (0.001 = 0.1%)
    opens = data['Open'].to_numpy()
    closes = data['Close'].to_numpy()
    #initialise variables
    capital = starting_capital
    stock = 0
    lttv = capital #last transaction total value
    #simulation constants
    percent_bought = 80
    percent_sold = 80
    #difference between transactions total value
    diff = []
    #[capital, stock value, total value] at the close of every day
    simulation = []
    for i in range(len(closes)):
        order = macd[i-1][0] if i > 0 else 0
        if order == 1:
            #buy stock with part of the cash
            spent = capital * percent_bought / 100
            stock = stock + spent * (1 - fee) / opens[i]
            capital = capital - spent
        elif order == -1:
            #sell part of the stock
            sold = stock * percent_sold / 100
            capital = capital + sold * opens[i] * (1 - fee)
            stock = stock - sold
        if order != 0:
            total_value = capital + stock * opens[i]
            diff.append(total_value - lttv)
            lttv = total_value
        stock_value = stock * closes[i]
        simulation.append([capital, stock_value, capital + stock_value])
    return simulation, diff

def buy_and_hold(starting_capital, data, fee=0.0):
    #benchmark: invest everything at the first day's open and keep it; total value at every close
    stock = starting_capital * (1 - fee) / data['Open'].iloc[0]
    return list(stock * data['Close'].to_numpy())
