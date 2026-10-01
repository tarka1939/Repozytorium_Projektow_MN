import time
import numpy as np

def lu(A, block=64):
    #LU factorisation with partial pivoting: P A = L U
    #Blocked (right-looking) version: a panel of `block` columns is factorised column by column,
    #then the rest of the matrix is updated with one matrix product, which numpy runs as BLAS code.
    #Same O(N^3) operation count as the column-by-column version, but far less memory traffic.
    n = A.shape[0]
    LU = A.astype(float) #L below the diagonal (unit diagonal not stored), U on and above it
    perm = np.arange(n)
    for k0 in range(0, n, block):
        k1 = min(k0 + block, n)
        for i in range(k0, k1):
            # Pivoting: largest |value| in column i at or below the diagonal
            pivot = np.argmax(np.abs(LU[i:, i])) + i
            if LU[pivot, i] == 0:
                raise ValueError("Singular matrix, LU factorisation is not possible")
            if pivot != i:
                # Swap whole rows: the computed part of L and the not yet reduced part move together
                LU[[i, pivot], :] = LU[[pivot, i], :]
                perm[[i, pivot]] = perm[[pivot, i]]
            # Multipliers for column i, then eliminate inside the panel
            LU[i + 1:, i] /= LU[i, i]
            LU[i + 1:, i + 1:k1] -= np.outer(LU[i + 1:, i], LU[i, i + 1:k1])
        # Rows of U to the right of the panel: L11 U12 = A12
        for i in range(k0 + 1, k1):
            LU[i, k1:] -= LU[i, k0:i] @ LU[k0:i, k1:]
        # Update the rest of the matrix: A22 -= L21 U12
        LU[k1:, k1:] -= LU[k1:, k0:k1] @ LU[k0:k1, k1:]

    L = np.tril(LU, -1) + np.eye(n)
    U = np.triu(LU)
    P = np.eye(n)[perm]
    return L, U, P

def forward_substitution(L, b):
    #solve L y = b for lower triangular L
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - L[i, :i] @ y[:i]) / L[i, i]
    return y

def back_substitution(U, y):
    #solve U x = y for upper triangular U
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]
    return x

def SolveLU(equation, norm, max_iter, n=0):
    #direct method; norm and max_iter are unused, kept so all solvers share one signature
    #returns the solution, the residual norm ||Ax - b|| and the total time
    start = time.perf_counter()
    A, b, x = equation.GetSystem(n)
    L, U, P = lu(A)
    # L y = P b, then U x = y
    y = forward_substitution(L, P @ b)
    x = back_substitution(U, y)

    end_time = time.perf_counter()
    r_norm = np.linalg.norm(A @ x - b)
    return x, r_norm, end_time - start
