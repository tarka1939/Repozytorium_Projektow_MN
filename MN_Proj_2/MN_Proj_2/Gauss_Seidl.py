import Equation as eq
import time
import numpy as np
def SolveGauss(equation, norm, max_iter,n=0):
    A, b, x = equation.GetSystem(n)
    n = len(b)
    x = np.zeros(n)
    residuals = []
    times = []
    for k in range(max_iter):
        start_time = time.time()
        x_new = np.copy(x)
        for i in range(n):
            sum1 = np.dot(A[i, :i], x_new[:i])
            sum2 = np.dot(A[i, i + 1:], x[i + 1:])
            x_new[i] = (b[i] - sum1 - sum2) / A[i, i]
        residual = np.linalg.norm(x_new - x)
        residuals.append(residual)
        times.append(time.time() - start_time)
        if residual < norm:
            break
        x = x_new
    return x, residuals, times