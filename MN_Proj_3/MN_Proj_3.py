import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



"""Funkcja do interpolacji Lagrange'a."""
def lagrange(x, y):
    x_intrp = np.zeros(1000)
    y_intrp = np.zeros(1000)

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
    return np.vectorize(interpolation)

def get_evenly_spaced_nodes(x, y, nodes):
    x_nodes = np.zeros(nodes)
    y_nodes = np.zeros(nodes)
    x_nodes = [x[i] for i in range(0, len(x), len(x)//nodes)]
    y_nodes = [y[i] for i in range(0, len(y), len(y)//nodes)]
    
    return x_nodes, y_nodes

def get_czybyszew_nodes(x,y,n):
    """Funkcja do generowania węzłów Czebyszewa."""
    nodes_x = np.zeros(n)
    nodes_y = np.zeros(n)
    for i in range(n):
        # Oblicz współrzędne węzłów Czebyszewa
        angle = (2 * i + 1) * np.pi / (2 * n)
        nodes_x[i] = (x.max() - x.min()) / 2 * np.cos(angle) + (x.max() + x.min()) / 2
        nodes_y[i] = (y.max() - y.min()) / 2 * np.sin(angle) + (y.max() + y.min()) / 2
    return nodes_x, nodes_y

def cubic_spline(x, y):
    """Implementacja funkcji do interpolacji funkcją sklejaną trzeciego stopnia."""
    n = len(x)
    h = np.diff(x)
    alpha = np.zeros(n)
    for i in range(1, n-1):
        alpha[i] = (3/h[i]) * (y[i+1] - y[i]) - (3/h[i-1]) * (y[i] - y[i-1])

    l = np.ones(n)
    mu = np.zeros(n)
    z = np.zeros(n)
    for i in range(1, n-1):
        l[i] = 2 * (x[i+1] - x[i-1]) - h[i-1] * mu[i-1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i-1] * z[i-1]) / l[i]

    b = np.zeros(n-1)
    c = np.zeros(n)
    d = np.zeros(n-1)

    for j in range(n-2, -1, -1):
        c[j] = z[j] - mu[j] * c[j+1]
        b[j] = (y[j+1] - y[j]) / h[j] - h[j] * (c[j+1] + 2*c[j]) / 3
        d[j] = (c[j+1] - c[j]) / (3*h[j])

    def spline_func(x_val):
        # Find the right interval
        i = np.searchsorted(x, x_val) - 1
        if i < 0:
            i = 0
        elif i >= n-1:
            i = n-2
        dx = x_val - x[i]
        return y[i] + b[i]*dx + c[i]*dx**2 + d[i]*dx**3

    return np.vectorize(spline_func)

def plot(x, y, x_dense_original, y_lagrange, x_dense_spline, y_spline,n):
    """Funkcja do rysowania wykresu."""
    ymin = min(y)*1.1
    ymax = max(y)*1.1
    plt.figure(figsize=(10, 6))
    plt.ylim([ymin, ymax])
    plt.plot(x, y, 'o', label='Dane węzłowe')
    plt.plot(x_dense_original, y_lagrange, label='Interpolacja Lagrange\'a')
    plt.plot(x_dense_spline, y_spline,label='Interpolacja funkcją sklejaną trzeciego stopnia', linestyle='--')
    plt.xlabel('Odległość (km)')
    plt.ylabel('Wysokość (m)')
    plt.title('Porównanie interpolacji profilu wysokościowego dla ' + str(n) + ' węzłów')
    plt.legend()
    plt.grid(True)
    plt.show()
    #read input to close
    #input("Naciśnij Enter, aby zamknąć program...")



# Wczytaj dane z pliku CSV
#data = pd.read_csv("Obiadek.csv")
#data = pd.read_csv("profil_etapu.csv")
data = pd.read_csv("Hel_yeah.csv")
x = data['distance'].values
y = data['elevation'].values

# #dla wszystkich węzłów:
# # Przeskaluj dziedzinę do [0, 1] dla Lagrange'a
# x_scaled = (x - x.min()) / (x.max() - x.min())
# # Interpolacja Lagrange’a
# x_dense = np.linspace(x_scaled.min(), x_scaled.max(), 500)
# y_lagrange = lagrange(x_scaled, y)(x_dense)
# # Cofnij skalowanie
# x_dense_original = x_dense * (x.max() - x.min()) + x.min()
# # Interpolacja funkcją sklejaną trzeciego stopnia
# spline = cubic_spline(x, y)
# x_dense_spline = np.linspace(x.min(), x.max(), 500)
# y_spline = spline(x_dense_spline)
# n = len(x)
# plot(x, y, x_dense_original, y_lagrange, x_dense_spline, y_spline,n)


#dla 10 węzłów:
n = 10
x_even,y_even = get_evenly_spaced_nodes(x, y, n)
x_czybyszew, y_czybyszew = get_czybyszew_nodes(x, y, n)
# Przeskaluj dziedzinę do [0, 1] dla Lagrange'a
x_scaled = (x_even - x_even.min()) / (x_even.max() - x_even.min())
x_scaled_czybyszew = (x_czybyszew - x_czybyszew.min()) / (x_czybyszew.max() - x_czybyszew.min())

# Interpolacja Lagrange’a
x_dense = np.linspace(x_scaled.min(), x_scaled.max(), 500)
x_dense_czybyszew = np.linspace(x_scaled_czybyszew.min(), x_scaled_czybyszew.max(), 500)

y_lagrange = lagrange(x_scaled, y_even)(x_dense)
y_czybyszew_lagrange = lagrange(x_scaled_czybyszew, y_czybyszew)(x_dense)
# Cofnij skalowanie
x_dense_original = x_dense * (x_even.max() - x_even.min()) + x_even.min()
x_czybyszew_original = x_dense * (x_czybyszew.max() - x_czybyszew.min()) + x_czybyszew.min()

spline = cubic_spline(x_even, y_even)
spline_czybyszew = cubic_spline(x_czybyszew, y_czybyszew)
x_dense_spline = np.linspace(x.min(), x.max(), n)
x_dense_spline_czybyszew = np.linspace(x_czybyszew.min(), x_czybyszew.max(), n)
y_spline = spline(x_dense_spline)
y_spline_czybyszew = spline_czybyszew(x_dense_spline_czybyszew)
# Rysowanie wykresu dla 10 węzłów
plot(x, y, x_dense_original, y_lagrange, x_dense_spline, y_spline,n)
plot(x, y, x_czybyszew_original, y_czybyszew_lagrange,x_dense_spline, y_spline_czybyszew, n)



#dla 30 węzłów:
n=30
x_dense = np.linspace(x_scaled.min(), x_scaled.max(), n)
y_lagrange = lagrange(x_scaled, y)(x_dense)
# Cofnij skalowanie dla funkcji sklejaną
x_dense_original = x_dense * (x.max() - x.min()) + x.min()
x_dense_spline = np.linspace(x.min(), x.max(), n)
y_spline = spline(x_dense_spline)
plot(x, y, x_dense_original, y_lagrange, x_dense_spline, y_spline,n)




