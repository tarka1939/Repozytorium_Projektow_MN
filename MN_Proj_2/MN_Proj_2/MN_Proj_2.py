import time
import numpy as np
import Equation as eq
import Gauss_Seidel as gs
import Jacobi as jc
import LU_Factor as lu
import Band_Solver as band
import Decomposition as dec
import Graphing as gp

TOLERANCE = 1e-9 #stop when ||Ax - b|| < TOLERANCE
MAX_ITER = 1000
N = 1279
SIZES = [100, 500, 1000, 2000, 3000]
REPEATS = 3 #every solve in the size sweep is timed this many times and the fastest run is kept

def run_iterative(name, solver, equation, index=0):
    start = time.perf_counter()
    x, residuals, times = solver(equation, TOLERANCE, MAX_ITER, index)
    total = time.perf_counter() - start
    if residuals[-1] < TOLERANCE:
        status = f"converged in {len(residuals)} iterations"
    elif len(residuals) < MAX_ITER:
        status = f"DIVERGED, stopped after {len(residuals)} iterations"
    else:
        status = f"not converged after {MAX_ITER} iterations"
    print(f"  {name:14s} {status}, residual {residuals[-1]:.2e}, {total:.3f} s")
    return residuals, times, total

def run_direct(name, solver, equation, index=0):
    x, residual, total = solver(equation, TOLERANCE, MAX_ITER, index)
    print(f"  {name:14s} residual {residual:.2e}, {total:.3f} s")
    return total

def numpy_solve(equation, norm, max_iter, n=0):
    #reference: LAPACK dense solver
    start = time.perf_counter()
    A, b, x = equation.GetSystem(n)
    x = np.linalg.solve(A, b)
    return x, np.linalg.norm(A @ x - b), time.perf_counter() - start

#the two systems: a1 = 13 (diagonally dominant) and a1 = 3, a2 = a3 = -1, b_n = sin(9n)
systems = {}
for label, a1 in (("A", 13), ("B", 3)):
    systems[label] = eq.BandMatrixSystem()
    systems[label].CreateNewSystem(N, a1, -1, -1)

for label, system in systems.items():
    A, b, x = system.GetSystem()
    print(f"System {label}: N = {N}, a1 = {A[0, 0]:g}")
    print(f"  spectral radius of the iteration matrix: Jacobi {dec.spectral_radius_jacobi(A):.4f}, "
          f"Gauss-Seidel {dec.spectral_radius_gauss_seidel(A):.4f} (converges only if < 1)")
    for name, solver in (("Jacobi", jc.SolveJacobi), ("Gauss-Seidel", gs.SolveGauss)):
        residuals, times, total = run_iterative(name, solver, system)
        gp.PlotTimeAndResidual(times, residuals, f"System {label}, {name}")
    run_direct("LU (dense)", lu.SolveLU, system)
    run_direct("LU (banded)", band.SolveBand, system)
    print()

#solve time against the number of unknowns for system A
sweep = eq.BandMatrixSystem()
for size in SIZES:
    sweep.CreateNewSystem(size, 13, -1, -1)
methods = {"Jacobi": jc.SolveJacobi, "Gauss-Seidel": gs.SolveGauss, "LU (dense)": lu.SolveLU,
           "LU (banded)": band.SolveBand, "numpy.linalg.solve": numpy_solve}
times_by_method = {name: [] for name in methods}
print(f"Time [s] for system A with N unknowns (best of {REPEATS} runs)")
print(f"  {'N':>6s}" + "".join(f"{name:>20s}" for name in methods))
for j, size in enumerate(SIZES):
    for name, solver in methods.items():
        best = float("inf")
        for repeat in range(REPEATS):
            start = time.perf_counter()
            solver(sweep, TOLERANCE, MAX_ITER, j)
            best = min(best, time.perf_counter() - start)
        times_by_method[name].append(best)
    print(f"  {size:6d}" + "".join(f"{times_by_method[name][-1]:20.4f}" for name in methods))

gp.PlotTimeAndNumberOfUnknowns(SIZES, times_by_method)
gp.PlotTimeAndNumberOfUnknowns(SIZES, times_by_method, log_scale=True)
