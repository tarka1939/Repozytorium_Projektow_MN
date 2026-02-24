import matplotlib.pyplot as plt
import numpy as np
def PlotTimeAndResidual(time_vector, residual_vector):
    iterations = np.arange(1, len(time_vector) + 1)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # Wykres czasu (skala liniowa)
    ax1.plot(iterations, time_vector, marker='o', linestyle='-', color='blue')
    ax1.set_ylabel("Czas [s]")
    ax1.set_title("Czas obliczeń na iterację")
    ax1.grid(True)

    # Wykres residuum (skala logarytmiczna)
    ax2.plot(iterations, residual_vector, marker='x', linestyle='-', color='red')
    ax2.set_yscale('log')
    ax2.set_xlabel("Numer iteracji")
    ax2.set_ylabel("Norma residuum")
    ax2.set_title("Zbieżność (residuum w skali logarytmicznej)")
    ax2.grid(True, which='both')

    plt.tight_layout()
    plt.show()
def PlotTimeAndNumberOfIterations(numbers_of_unknowns, gauss_times, jacobi_times, LU_times, np_times = None):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    # Wykres czasu (skala liniowa)
    ax1.plot(numbers_of_unknowns, gauss_times, marker='o',
             linestyle='-', color='blue', label='Gauss-Seidel')
    ax1.plot(numbers_of_unknowns, jacobi_times, marker='x',
             linestyle='-', color='green', label='Jacobi')
    ax1.plot(numbers_of_unknowns, LU_times, marker='s',
             linestyle='-', color='red', label='LU')
    if np_times is not None:
        ax1.plot(numbers_of_unknowns, np_times, marker='^',
                 linestyle='-', color='orange', label='NumPy')
    ax1.set_xlabel("Liczba niewiadomych")
    ax1.set_ylabel("Czas [s]")
    ax1.set_title("Czas obliczeń w zależności od liczby niewiadomych")
    ax1.grid(True)
    ax1.legend()
    plt.tight_layout()
    plt.show()

def PlotTimeAndNumberOfIterations_log(numbers_of_unknowns, gauss_times, jacobi_times, LU_times, np_times = None):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    # Wykres czasu (skala logarytmiczna)
    ax1.plot(numbers_of_unknowns, gauss_times, marker='o',
             linestyle='-', color='blue', label='Gauss-Seidel')
    ax1.plot(numbers_of_unknowns, jacobi_times, marker='x',
             linestyle='-', color='green', label='Jacobi')
    ax1.plot(numbers_of_unknowns, LU_times, marker='s',
             linestyle='-', color='red', label='LU')
    if np_times is not None:
        ax1.plot(numbers_of_unknowns, np_times, marker='^',
                 linestyle='-', color='orange', label='NumPy')
    ax1.set_xlabel("Liczba niewiadomych")
    ax1.set_ylabel("Czas [s]")
    ax1.set_title("Czas obliczeń w zależności od liczby niewiadomych")
    ax1.set_yscale('log')
    ax1.grid(True)
    ax1.legend()
    plt.tight_layout()
    plt.show()