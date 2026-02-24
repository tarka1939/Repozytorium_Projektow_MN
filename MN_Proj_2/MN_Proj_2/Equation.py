import numpy as np

class BandMatrixSystem:
    def __init__(self):
        self.N = 0
        self.A1 = 0
        self.A2 = 0
        self.A3 = 0
        self.Systems = []

        
    def CreateFullMatrix(self):
        A = np.zeros((self.N, self.N))

        for i in range(self.N):
            A[i, i] = self.A1
            if i - 1 >= 0:
                A[i, i - 1] = self.A2
            if i + 1 < self.N:
                A[i, i + 1] = self.A2
            if i - 2 >= 0:
                A[i, i - 2] = self.A3
            if i + 2 < self.N:
                A[i, i + 2] = self.A3
        return A

    def CreateRightHandSideVector(self):
        return np.array([np.sin(9 * n) for n in range(self.N)])

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

