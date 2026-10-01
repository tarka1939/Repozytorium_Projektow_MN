import numpy as np

def load_profile(path):
    #elevation profile: distance [m] and elevation [m] on every line, separated by a comma, tab or spaces,
    #with or without a header line
    x, y = [], []
    with open(path, encoding='utf-8-sig') as f:
        for line in f:
            parts = line.replace(',', ' ').split()
            if len(parts) < 2:
                continue
            try:
                x.append(float(parts[0]))
                y.append(float(parts[1]))
            except ValueError:
                continue #header
    return np.array(x), np.array(y)

def get_evenly_spaced_nodes(x, y, nodes):
    x_new = np.linspace(x.min(), x.max(), nodes)
    y_new = np.interp(x_new, x, y)
    return x_new, y_new

def get_chebyshev_nodes(x, y, nodes):
    #Chebyshev nodes (zeros of T_n) mapped onto [x.min(), x.max()], in increasing order;
    #the elevation at a node is read from the profile like for evenly spaced nodes
    k = np.arange(nodes)
    x_new = 0.5 * (x.min() + x.max()) - 0.5 * (x.max() - x.min()) * np.cos((2 * k + 1) * np.pi / (2 * nodes))
    y_new = np.interp(x_new, x, y)
    return x_new, y_new

def lagrange_interpolation(x, y, x_eval):
    """Lagrange interpolation polynomial through (x, y), evaluated at x_eval."""
    x_eval = np.asarray(x_eval, dtype=float)
    result = np.zeros_like(x_eval)
    n = len(x)
    for i in range(n):
        term = np.full_like(x_eval, y[i])
        for j in range(n):
            if i != j:
                term *= (x_eval - x[j]) / (x[i] - x[j])
        result += term
    return result

def cubic_spline_interpolation(x, y, x_eval):
    """Natural cubic spline through (x, y) (x increasing), evaluated at x_eval."""
    n = len(x)
    h = np.diff(x)
    alpha = np.zeros(n)
    for i in range(1, n - 1):
        alpha[i] = (3 / h[i]) * (y[i + 1] - y[i]) - (3 / h[i - 1]) * (y[i] - y[i - 1])

    l = np.ones(n)
    mu = np.zeros(n)
    z = np.zeros(n)

    # Natural boundary conditions: second derivative 0 at both ends
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

    # Evaluate the piece that contains each point (the end pieces are extended outside [x[0], x[-1]])
    x_eval = np.asarray(x_eval, dtype=float)
    idx = np.searchsorted(x, x_eval, side='right') - 1
    idx = np.clip(idx, 0, n - 2)
    dx = x_eval - x[idx]
    return y[idx] + b[idx] * dx + c[idx] * dx**2 + d[idx] * dx**3

def errors(y_true, y_approx):
    #root mean square error and largest absolute error
    diff = np.asarray(y_approx) - np.asarray(y_true)
    return np.sqrt(np.mean(diff**2)), np.abs(diff).max()
