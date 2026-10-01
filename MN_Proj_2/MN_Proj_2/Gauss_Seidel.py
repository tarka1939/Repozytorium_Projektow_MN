import time
import numpy as np

#stop early when the residual grows this many times above ||b|| (the residual of the starting vector)
DIVERGENCE_FACTOR = 1e10

def SolveGauss(equation, norm, max_iter, n=0):
    #iterate until ||Ax - b|| < norm, at most max_iter times, starting from x = 0
    #(the same stopping rule and starting vector as SolveJacobi, so iteration counts are comparable)
    #returns the solution, the residual norm after every iteration and the time of every iteration
    A, b, x = equation.GetSystem(n)
    n = len(b)
    x = np.zeros(n)
    b_norm = np.linalg.norm(b)
    residuals = []
    times = []
    for k in range(max_iter):
        start_time = time.perf_counter()
        #updating x in place: x_j for j < i are already the new values
        for i in range(n):
            x[i] = (b[i] - A[i, :i] @ x[:i] - A[i, i + 1:] @ x[i + 1:]) / A[i, i]
        residual = np.linalg.norm(A @ x - b)
        residuals.append(residual)
        times.append(time.perf_counter() - start_time)
        if residual < norm or not np.isfinite(residual) or residual > DIVERGENCE_FACTOR * b_norm:
            break
    return x, residuals, times
