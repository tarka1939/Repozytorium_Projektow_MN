import numpy as np
import Equation
import time
def lu(A):
    n = A.shape[0]
    L = np.zeros((n, n))
    U = A.copy().astype(float)
    P = np.eye(n)

    for i in range(n):
        # Pivoting
        pivot = np.argmax(np.abs(U[i:, i])) + i
        if U[pivot, i] == 0:
            raise ValueError("Macierz osobliwa (nieodwracalna) – nie można wykonać faktoryzacji LU")

        if pivot != i:
            # Zamiana wierszy w U i P
            U[[i, pivot], :] = U[[pivot, i], :]
            P[[i, pivot], :] = P[[pivot, i], :]
            # Zamiana wierszy w L (tylko lewej części)
            if i > 0:
                L[[i, pivot], :i] = L[[pivot, i], :i]

        # Główna pętla faktoryzacji
        L[i, i] = 1
        for j in range(i + 1, n):
            L[j, i] = U[j, i] / U[i, i]
            U[j, :] -= L[j, i] * U[i, :]

    return L, U, P


def SolveLU(equation, norm, max_iter,n=0):
    start = time.time()
    A, b, x = equation.GetSystem(n)
    L, U, P = lu(A)
    # DebugPrintMatrix(L)
    # DebugPrintMatrix(D)
    # DebugPrintMatrix(U)
    # y = L\P*b

    y = np.linalg.solve(L, P @ b)
    x = np.linalg.solve(U, y)

    end_time = time.time()
    r_norm = np.linalg.norm(A@x-b)
    return x, r_norm, end_time-start