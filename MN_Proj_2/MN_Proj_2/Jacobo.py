import time
import Equation
import Decomposition as dec
import numpy as np
def SolveJacobi(equation, norm, max_iter,n=0):
    A,b,x = equation.GetSystem(n)
    n = len(b)
    x = np.ones(n)

    residuals = []
    times = []
    L = dec.get_L(A,n)
    D = dec.get_D(A,n)
    U = dec.get_U(A,n)
    #DebugPrintMatrix(L)
    #DebugPrintMatrix(D)
    #DebugPrintMatrix(U)
    D_inv = np.linalg.inv(D)
    M = -D_inv @ (L + U)
    w = D_inv @ b

    i = 0
    inorm=1e22
    start_time = time.time()

    while inorm > norm and i < 1000:
        iter_start=time.time()
        x = M @ x + w
        inorm = np.linalg.norm(A @ x - b)
        i += 1
        residuals.append(inorm)
        times.append(time.time() - iter_start)
    end_time = time.time()
    elapsed = end_time - start_time
    return x, residuals, times


def DebugPrintMatrix(matrix):
    for row in matrix:
        print(" ".join(f"{val:.2f}" for val in row))