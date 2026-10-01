#checks for the interpolation methods
#run with: python test_interpolation.py   (or: python -m pytest test_interpolation.py)
import os
import tempfile
import numpy as np
import interpolation as ip

def natural_spline_reference(x, y, x_eval):
    #independent construction: solve the tridiagonal system for the second derivatives M_i
    #(M_0 = M_n = 0) and evaluate the spline written in terms of M
    n = len(x)
    h = np.diff(x)
    A = np.zeros((n, n))
    rhs = np.zeros(n)
    A[0, 0] = A[-1, -1] = 1
    for i in range(1, n - 1):
        A[i, i - 1], A[i, i], A[i, i + 1] = h[i - 1], 2 * (h[i - 1] + h[i]), h[i]
        rhs[i] = 6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])
    M = np.linalg.solve(A, rhs)
    k = np.clip(np.searchsorted(x, x_eval, side='right') - 1, 0, n - 2)
    t0, t1 = x[k + 1] - x_eval, x_eval - x[k]
    return (M[k] * t0**3 + M[k + 1] * t1**3) / (6 * h[k]) + (y[k] / h[k] - M[k] * h[k] / 6) * t0 \
        + (y[k + 1] / h[k] - M[k + 1] * h[k] / 6) * t1

def test_lagrange_reproduces_polynomials():
    x = np.array([0.0, 1.5, 2.0, 4.0, 7.0, 9.0])
    p = np.poly1d([0.3, -2.0, 1.0, 5.0, -1.0, 2.0]) #degree 5, 6 nodes
    x_eval = np.linspace(-1, 10, 57)
    assert np.allclose(ip.lagrange_interpolation(x, p(x), x_eval), p(x_eval))

def test_spline_matches_reference_and_passes_through_nodes():
    rng = np.random.default_rng(0)
    for n in (3, 4, 10, 30):
        x = np.sort(rng.uniform(0, 1000, n))
        y = rng.normal(100, 30, n)
        x_eval = np.linspace(x[0], x[-1], 500)
        assert np.allclose(ip.cubic_spline_interpolation(x, y, x_eval), natural_spline_reference(x, y, x_eval))
        assert np.allclose(ip.cubic_spline_interpolation(x, y, x), y)

def test_spline_is_exact_for_straight_lines():
    x = np.array([0.0, 1.0, 3.0, 3.5, 8.0])
    assert np.allclose(ip.cubic_spline_interpolation(x, 2 * x + 1, np.linspace(0, 8, 33)), 2 * np.linspace(0, 8, 33) + 1)

def test_chebyshev_nodes():
    x = np.linspace(100, 600, 501)
    y = np.sin(x / 50)
    x_nodes, y_nodes = ip.get_chebyshev_nodes(x, y, 9)
    assert np.all(np.diff(x_nodes) > 0) and x_nodes[0] > 100 and x_nodes[-1] < 600
    assert np.allclose(x_nodes - 350, -(x_nodes[::-1] - 350)) #symmetric around the middle
    assert np.allclose(x_nodes, 350 - 250 * np.cos((2 * np.arange(9) + 1) * np.pi / 18))
    #a spline through Chebyshev nodes needs increasing nodes and must pass through them
    assert np.allclose(ip.cubic_spline_interpolation(x_nodes, y_nodes, x_nodes), y_nodes)

def test_evenly_spaced_nodes():
    x = np.linspace(0, 10, 11)
    x_nodes, y_nodes = ip.get_evenly_spaced_nodes(x, x**2, 3)
    assert np.allclose(x_nodes, [0, 5, 10]) and np.allclose(y_nodes, [0, 25, 100])

def test_load_profile_formats():
    samples = {
        "header_comma.csv": "﻿distance,elevation\n0,10.5\n2.5,11\n",
        "polish_header.csv": "Dystans (m),Wysokość (m)\n0,10.5\n2.5,11\n",
        "no_header_space.txt": "0 10.5\n2.5 11\n",
        "tabs.txt": "0\t10.5\n2.5\t11\n\n",
    }
    with tempfile.TemporaryDirectory() as folder:
        for name, text in samples.items():
            path = os.path.join(folder, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            x, y = ip.load_profile(path)
            assert np.allclose(x, [0, 2.5]) and np.allclose(y, [10.5, 11]), name

def test_errors():
    rmse, max_error = ip.errors([0, 0, 0, 0], [1, -1, 1, -3])
    assert np.isclose(rmse, np.sqrt(3)) and max_error == 3

if __name__ == '__main__':
    tests = [f for name, f in sorted(globals().items()) if name.startswith('test_')]
    for test in tests:
        test()
        print('ok  ', test.__name__)
    print(f'{len(tests)} tests passed')
