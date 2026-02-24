import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def get_evenly_spaced_nodes(x, y, nodes):
    x_new = np.linspace(x.min(), x.max(), nodes)
    y_new = np.interp(x_new, x, y)
    return x_new, y_new

def get_chebyshev_nodes(x, y, nodes):
        x_nodes = []
        y_nodes = []
        
        for n in range(nodes):
            x_nodes.append(0.5 * (x[0] + x[-1]) + 0.5 * (x[-1] - x[0]) * math.cos((2 * n + 1) * math.pi / (2 * nodes)))
        for node in x_nodes:
            closest = 0
            for i in range(len(x)):
                if abs(x[i] - node) < abs(x[closest] - node):
                    closest = i
            y_nodes.append(y[closest])
            x_nodes[x_nodes.index(node)] = x[closest]
            
        return x_nodes, y_nodes

def lagrange_interpolation(x, y):
    """Funkcja do interpolacji Lagrange'a."""
    x_intrp = np.linspace(min(x), max(x), 1000)
    y_intrp = np.zeros_like(x_intrp)

    def interpolation(x_val):
        n = len(x)
        result = 0.0
        for i in range(n):
            term = y[i]
            for j in range(n):
                if i != j:
                    term *= (x_val - x[j]) / (x[i] - x[j])
            result += term
        return result
    return np.vectorize(interpolation)(x_intrp)


def cubic_spline_interpolation(x, y):
    """Interpolacja funkcją sklejaną trzeciego stopnia — wersja z poprawnymi warunkami brzegowymi."""
    n = len(x)
    h = np.diff(x)
    alpha = np.zeros(n)
    for i in range(1, n - 1):
        alpha[i] = (3 / h[i]) * (y[i + 1] - y[i]) - (3 / h[i - 1]) * (y[i] - y[i - 1])

    l = np.ones(n)
    mu = np.zeros(n)
    z = np.zeros(n)

    # Warunki brzegowe naturalne
    l[0] = 1
    mu[0] = 0
    z[0] = 0

    for i in range(1, n - 1):
        l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]

    l[-1] = 1
    z[-1] = 0
    c = np.zeros(n)
    b = np.zeros(n - 1)
    d = np.zeros(n - 1)

    for j in range(n - 2, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b[j] = (y[j + 1] - y[j]) / h[j] - h[j] * (c[j + 1] + 2 * c[j]) / 3
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])

    # Interpolacja punktów pośrednich
    x_dense = np.linspace(x[0], x[-1], 1000)
    y_dense = np.zeros_like(x_dense)
    idx = np.searchsorted(x, x_dense, side='right') - 1
    idx = np.clip(idx, 0, n - 2)
    dx = x_dense - x[idx]
    y_dense = y[idx] + b[idx]*dx + c[idx]*dx**2 + d[idx]*dx**3

    return x_dense, y_dense


def plot(x, y,x_nodes, y_nodes, x_dense_original, y_lagrange, x_dense_spline, y_spline,n):
    """Funkcja do rysowania wykresu."""
    ymin = min(y)-0.1 * abs(min(y))
    ymax = max(y)+0.1 * abs(max(y))
    plt.figure(figsize=(10, 6))
    plt.ylim([ymin, ymax])
    plt.plot(x, y, label='Dane źródłowe',linestyle="-")
    plt.plot(x_nodes, y_nodes, 'x', label='Dane węzłowe')
    plt.plot(x_dense_original, y_lagrange, label='Interpolacja Lagrange\'a')
    plt.plot(x_dense_spline, y_spline,label='Interpolacja funkcją sklejaną trzeciego stopnia', linestyle='--')
    plt.xlabel('Odległość (km)')
    plt.ylabel('Wysokość (m)')
    plt.title('Porównanie interpolacji profilu wysokościowego dla ' + str(n) + ' węzłów')
    plt.legend()
    plt.grid(True)
    plt.show()

def testing(n,data):
    """Funkcja do testowania interpolacji dla różnych liczby węzłów."""
    x = data['distance'].values
    y = data['elevation'].values

    # Generowanie węzłów
    x_nodes, y_nodes = get_evenly_spaced_nodes(x, y, n)
    x_nodes_czybyszew, y_nodes_czybyszew = get_chebyshev_nodes(x, y, n)
    # Interpolacja Lagrange'a
    y_lagrange = lagrange_interpolation(x_nodes, y_nodes)
    y_lagrange_czybyszew = lagrange_interpolation(x_nodes_czybyszew, y_nodes_czybyszew)
    # Interpolacja funkcją sklejaną trzeciego stopnia
    x_dense_spline, y_spline = cubic_spline_interpolation(x_nodes, y_nodes)
    # Rysowanie wykresu
    x_dense = np.linspace(min(x), max(x), 1000)
    

    plot(x, y,x_nodes, y_nodes, x_dense, y_lagrange, x_dense_spline, y_spline, n)

    plot(x, y, x_nodes_czybyszew, y_nodes_czybyszew, x_dense,y_lagrange_czybyszew, x_dense_spline, y_spline, n)

    #Wypisanie informacji o interpolacji
    print(f"Interpolacja dla {n} węzłów:")
    print(f"Węzły: {x_nodes}")
    print(f"Wartości węzłów: {y_nodes}")
    # pokazujemy tylko pierwsze 5 wartości
    print(f"Interpolacja Lagrange'a: {y_lagrange[:5]}...")
    print(
        f"Interpolacja funkcją sklejaną trzeciego stopnia: {y_spline[:5]}...")
    print("\n" + "="*50 + "\n")
    # Zwracamy, aby zakończyć funkcję

    return


# Wczytaj dane z pliku CSV
data = pd.read_csv("Obiadek.csv")
#data = pd.read_csv("profil_etapu.csv")

nodes = [10,25,50]
for n in nodes:
    testing(n, data)
#data = pd.read_csv("Hel_yeah.csv")
for n in nodes:
    testing(n, data)