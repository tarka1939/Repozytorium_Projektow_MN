import Equation
import numpy as np
#LDU factorisation without numpy
def get_L (A,n):
    k = n
    L = np.zeros((k, k))
    for i in range(k):
        for j in range(i + 1):
            if i == j:
                L[i, j] = 0
            else:
                L[i, j] = A[i, j]
    
    return L
def get_U(A,n):
    k = n
    U = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            if i < j:
                U[i, j] = A[i, j]
            else:
                U[i, j] = 0
    return U
def get_D(A,n):
    k = n
    D = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            if i == j:
                D[i, j] = A[i, j]
            else:
                D[i, j] = 0
    return D