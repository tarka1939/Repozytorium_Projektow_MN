import mplfinance as mpf
import matplotlib.pyplot as plt
#graph csv data on a plot as Candlestick chart type graph
def graph_data(data):
    #plotting the data
    mpf.plot(data, type='candle', style='charles', volume=True, title='Microsoft Stocks', ylabel='Price', ylabel_lower='Volume', warn_too_much_data=len(data) + 1)
    return


def plot_MACD(macd, diff, signal, data):
    # plot the MACD
    # Extract x and y values from diff
    x_values_diff = [item[1] for item in diff]
    y_values_diff = [item[0] for item in diff]

    # Extract x and y values from signal
    x_values_signal = [item[1] for item in signal]
    y_values_signal = [item[0] for item in signal]
    # plot macd as points with green up arrow on 1, red down arrow on -1 and nothing at 0
    bullish_run = []
    bearish_run = []

    for i in range(len(macd)):
        if macd[i][0] == 1:
            bullish_run.append([macd[i][1], macd[i][2]])
        elif macd[i][0] == -1:
            bearish_run.append([macd[i][1], macd[i][2]])

    plt.plot(x_values_diff, y_values_diff, label='MACD_diff')
    plt.plot(x_values_signal, y_values_signal, label='MACD_signal')

    if bullish_run:
        plt.scatter([item[0] for item in bullish_run], [item[1] for item in bullish_run], marker='^', color='g', label='Start Bullish Run', zorder = 2)
    if bearish_run:
        plt.scatter([item[0] for item in bearish_run], [item[1] for item in bearish_run], marker='v', color='r', label='Start Bearish Run', zorder = 2)
    plt.title('MACD')
    plt.xlabel('Days')
    plt.ylabel('Value')
    plt.legend()
    plt.show()
    return

def plot_simulation(dates, simulation, benchmark=None):
    #plot the total value of the simulated portfolio, optionally next to a buy-and-hold benchmark
    y_values_total = [item[2] for item in simulation]
    plt.plot(dates, y_values_total, label='MACD strategy')
    if benchmark is not None:
        plt.plot(dates, benchmark, label='Buy and hold')
    plt.title('Simulation')
    plt.xlabel('Date')
    plt.ylabel('Total value')
    plt.legend()
    plt.show()
    return
