import numpy as np

class BandMatrixSystem:
    def __init__(self):
        self.N = 0
        self.A1 = 0
        self.A2 = 0
        self.A3 = 0
        self.Systems = []


    def CreateFullMatrix(self):
        #pentadiagonal matrix: a1 on the main diagonal, a2 on the first and a3 on the second off-diagonals
        A = np.diag(np.full(self.N, float(self.A1)))
        A += np.diag(np.full(self.N - 1, float(self.A2)), 1) + np.diag(np.full(self.N - 1, float(self.A2)), -1)
        A += np.diag(np.full(self.N - 2, float(self.A3)), 2) + np.diag(np.full(self.N - 2, float(self.A3)), -2)
        return A

    def CreateRightHandSideVector(self):
        return np.sin(9 * np.arange(self.N))

    def CreateNewSystem(self, N, a1, a2, a3):

        self.N = N
        self.A1 = a1
        self.A2 = a2
        self.A3 = a3

        A = self.CreateFullMatrix()
        b = self.CreateRightHandSideVector()
        x = None
        self.Systems.append((A, b, x))

    def GetSystem(self, index=0):
        return self.Systems[index]
    def PrintSystem(self):
        for i, (A, b, x) in enumerate(self.Systems):
            print(f"System {i}:")
            print("A:")
            print(A)
            print("b:")
            print(b)
            print("x:")
            print(x)
            print()
