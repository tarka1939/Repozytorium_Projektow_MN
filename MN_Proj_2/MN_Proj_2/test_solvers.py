#checks for the linear system solvers
#run with: python test_solvers.py   (or: python -m pytest test_solvers.py)
import numpy as np
import Equation as eq
import Gauss_Seidel as gs
import Jacobi as jc
import LU_Factor as lu
import Band_Solver as band
import Decomposition as dec

def make_system(N, a1):
    system = eq.BandMatrixSystem()
    system.CreateNewSystem(N, a1, -1, -1)
    return system

def test_matrix_structure():
    A, b, x = make_system(6, 13).GetSystem()
    assert A[2, 2] == 13 and A[2, 1] == A[2, 3] == A[2, 0] == A[2, 4] == -1 and A[2, 5] == 0
    assert np.allclose(A, A.T) and np.allclose(b, np.sin(9 * np.arange(6)))

def test_iterative_methods_reach_tolerance():
    system = make_system(300, 13)
    A, b, x = system.GetSystem()
    expected = np.linalg.solve(A, b)
    for solver in (jc.SolveJacobi, gs.SolveGauss):
        x, residuals, times = solver(system, 1e-9, 1000)
        #the returned vector itself satisfies the tolerance, not just the last step size
        assert np.linalg.norm(A @ x - b) < 1e-9 and residuals[-1] < 1e-9
        assert np.allclose(x, expected, atol=1e-9)
        assert len(residuals) == len(times)

def test_iterative_methods_stop_when_diverging():
    system = make_system(300, 3)
    for solver in (jc.SolveJacobi, gs.SolveGauss):
        x, residuals, times = solver(system, 1e-9, 1000)
        assert len(residuals) < 1000 and residuals[-1] > 1e9 and np.isfinite(residuals[-1])

def test_max_iter_is_respected():
    for solver in (jc.SolveJacobi, gs.SolveGauss):
        x, residuals, times = solver(make_system(100, 13), 1e-30, 7)
        assert len(residuals) == 7

def test_spectral_radius_predicts_convergence():
    A13, _, _ = make_system(200, 13).GetSystem()
    A3, _, _ = make_system(200, 3).GetSystem()
    assert dec.spectral_radius_jacobi(A13) < 1 and dec.spectral_radius_gauss_seidel(A13) < 1
    assert dec.spectral_radius_jacobi(A3) > 1 and dec.spectral_radius_gauss_seidel(A3) > 1

def test_lu_factorisation_with_pivoting():
    rng = np.random.default_rng(0)
    for n in (1, 2, 5, 63, 64, 65, 150):
        A = rng.normal(size=(n, n))
        if n > 1:
            A[np.arange(n), np.arange(n)] = 0 #forces row swaps
        L, U, P = lu.lu(A)
        assert np.allclose(P @ A, L @ U)
        assert np.allclose(L, np.tril(L)) and np.allclose(np.diag(L), 1) and np.allclose(U, np.triu(U))
        assert np.abs(L).max() <= 1 + 1e-12 #partial pivoting keeps every multiplier <= 1

def test_triangular_solves():
    rng = np.random.default_rng(1)
    L = np.tril(rng.normal(size=(40, 40))) + 40 * np.eye(40)
    b = rng.normal(size=40)
    assert np.allclose(lu.forward_substitution(L, b), np.linalg.solve(L, b))
    assert np.allclose(lu.back_substitution(L.T, b), np.linalg.solve(L.T, b))

def test_direct_solvers_on_both_systems():
    for a1 in (13, 3):
        system = make_system(400, a1)
        A, b, x = system.GetSystem()
        expected = np.linalg.solve(A, b)
        for solver in (lu.SolveLU, band.SolveBand):
            x, residual, seconds = solver(system, 1e-9, 1000)
            assert residual < 1e-12 and np.allclose(x, expected)

def test_band_solver_on_random_band_matrices():
    rng = np.random.default_rng(2)
    for trial in range(200):
        n = int(rng.integers(1, 30))
        p, q = int(rng.integers(0, 4)), int(rng.integers(0, 4))
        A = np.zeros((n, n))
        for k in range(-p, q + 1):
            if abs(k) < n:
                A += np.diag(rng.normal(size=n - abs(k)), k)
        if trial % 2:
            A[np.arange(n), np.arange(n)] = 0 #forces row swaps
        if abs(np.linalg.det(A)) < 1e-6:
            continue
        b = rng.normal(size=n)
        assert np.allclose(band.band_solve(A, b, p, q), np.linalg.solve(A, b))

if __name__ == '__main__':
    tests = [f for name, f in sorted(globals().items()) if name.startswith('test_')]
    for test in tests:
        test()
        print('ok  ', test.__name__)
    print(f'{len(tests)} tests passed')
