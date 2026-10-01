import time
import numpy as np

#stop early when the residual grows this many times above ||b|| (the residual of the starting vector)
DIVERGENCE_FACTOR = 1e10

def SolveJacobi(equation, norm, max_iter, n=0):
    #iterate until ||Ax - b|| < norm, at most max_iter times, starting from x = 0
    #returns the solution, the residual norm after every iteration and the time of every iteration
    A, b, x = equation.GetSystem(n)
    d = np.diag(A)
    R = A - np.diag(d) #L + U
    x = np.zeros(len(b))
    b_norm = np.linalg.norm(b)

    residuals = []
    times = []
    for i in range(max_iter):
        iter_start = time.perf_counter()
        #x_i = (b_i - sum_{j != i} a_ij x_j) / a_ii, using only the previous iterate
        x = (b - R @ x) / d
        inorm = np.linalg.norm(A @ x - b)
        residuals.append(inorm)
        times.append(time.perf_counter() - iter_start)
        if inorm < norm or not np.isfinite(inorm) or inorm > DIVERGENCE_FACTOR * b_norm:
            break
    return x, residuals, times
