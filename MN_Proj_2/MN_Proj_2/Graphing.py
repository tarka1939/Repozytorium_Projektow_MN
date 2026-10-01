import matplotlib.pyplot as plt
import numpy as np
def PlotTimeAndResidual(time_vector, residual_vector, title=""):
    iterations = np.arange(1, len(time_vector) + 1)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    if title:
        fig.suptitle(title)

    # Time per iteration (linear scale)
    ax1.plot(iterations, time_vector, marker='o', linestyle='-', color='blue')
    ax1.set_ylabel("Time [s]")
    ax1.set_title("Time per iteration")
    ax1.grid(True)

    # Residual norm (log scale)
    ax2.plot(iterations, residual_vector, marker='x', linestyle='-', color='red')
    ax2.set_yscale('log')
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Residual norm ||Ax - b||")
    ax2.set_title("Convergence (log scale)")
    ax2.grid(True, which='both')

    plt.tight_layout()
    plt.show()

def PlotTimeAndNumberOfUnknowns(numbers_of_unknowns, times_by_method, log_scale=False):
    #times_by_method: {method name: [time for every number of unknowns]}
    fig, ax1 = plt.subplots(figsize=(10, 6))
    markers = ['o', 'x', 's', '^', 'd']
    for (name, times), marker in zip(times_by_method.items(), markers):
        ax1.plot(numbers_of_unknowns, times, marker=marker, linestyle='-', label=name)
    ax1.set_xlabel("Number of unknowns N")
    ax1.set_ylabel("Time [s]")
    ax1.set_title("Solve time vs number of unknowns" + (" (log scale)" if log_scale else ""))
    if log_scale:
        ax1.set_yscale('log')
    ax1.grid(True, which='both')
    ax1.legend()
    plt.tight_layout()
    plt.show()
