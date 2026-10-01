import time
import numpy as np

def band_solve(A, b, p=2, q=2):
    #Gaussian elimination with partial pivoting for a band matrix with p subdiagonals and q superdiagonals.
    #Only a (p+1) x (p+q+1) window of rows is kept, so the cost is O(N p (p+q)) instead of O(N^3).
    #Row swaps can only bring rows from within p rows below, so U gets at most p+q superdiagonals.
    n = len(b)
    w = p + q + 1 #width of a row: columns i .. i+p+q
    diagonals = {k: np.diagonal(A, k) for k in range(-p, q + 1)}

    def band_row(j, first_col):
        #row j of A over columns first_col .. first_col+w-1
        row = np.zeros(w)
        for k in range(-p, q + 1):
            col = j + k
            if 0 <= col < n and 0 <= col - first_col < w:
                row[col - first_col] = diagonals[k][min(j, col)]
        return row

    U = np.zeros((n, w)) #U[i, k] = entry (i, i+k) of the upper triangular factor
    y = np.zeros(n)
    rows = [band_row(j, 0) for j in range(min(p + 1, n))]
    rhs = [float(b[j]) for j in range(min(p + 1, n))]
    for i in range(n):
        #rows[k] holds row i+k (after swaps) over columns i .. i+w-1
        pivot = max(range(len(rows)), key=lambda k: abs(rows[k][0]))
        if rows[pivot][0] == 0:
            raise ValueError("Singular matrix")
        rows[0], rows[pivot] = rows[pivot], rows[0]
        rhs[0], rhs[pivot] = rhs[pivot], rhs[0]
        for k in range(1, len(rows)):
            m = rows[k][0] / rows[0][0]
            rows[k] = rows[k] - m * rows[0]
            rhs[k] -= m * rhs[0]
        U[i] = rows[0]
        y[i] = rhs[0]
        #move the window one column to the right and bring in the next row
        rows = [np.append(r[1:], 0.0) for r in rows[1:]]
        rhs = rhs[1:]
        if i + p + 1 < n:
            rows.append(band_row(i + p + 1, i + 1))
            rhs.append(float(b[i + p + 1]))
    #back substitution with the banded U
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        last = min(w, n - i)
        x[i] = (y[i] - U[i, 1:last] @ x[i + 1:i + last]) / U[i, 0]
    return x

def SolveBand(equation, norm, max_iter, n=0):
    #direct method for the pentadiagonal systems of this project; same signature and results as SolveLU
    start = time.perf_counter()
    A, b, x = equation.GetSystem(n)
    x = band_solve(A, b, 2, 2)
    end_time = time.perf_counter()
    r_norm = np.linalg.norm(A @ x - b)
    return x, r_norm, end_time - start
