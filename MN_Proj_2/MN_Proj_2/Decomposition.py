import numpy as np
#A = L + D + U split used by the iterative methods
def get_L(A):
    #strictly lower triangular part
    return np.tril(A, -1)

def get_U(A):
    #strictly upper triangular part
    return np.triu(A, 1)

def get_D(A):
    return np.diag(np.diag(A))

#an iterative method x_{k+1} = M x_k + w converges for every starting vector
#if and only if the spectral radius of M is below 1
def spectral_radius_jacobi(A):
    #M = -D^-1 (L + U)
    M = -(get_L(A) + get_U(A)) / np.diag(A)[:, None]
    return np.abs(np.linalg.eigvals(M)).max()

def spectral_radius_gauss_seidel(A):
    #M = -(D + L)^-1 U
    M = -np.linalg.solve(get_D(A) + get_L(A), get_U(A))
    return np.abs(np.linalg.eigvals(M)).max()
