from ast import iter_child_nodes
import Equation as eq
import Gauss_Seidl as gs
import Jacobo as jc
import LU_Factor as lu
import numpy as np
import Graphing as gp
import time

i = 3  # Number of iterations for the loop
prod = 1

equation1 = eq.BandMatrixSystem()
equation2 = eq.BandMatrixSystem()

equation1.CreateNewSystem(1279, 13, -1, -1)
equation2.CreateNewSystem(1279, 3, -1, -1)

debug_equation = eq.BandMatrixSystem()
debug_equation.CreateNewSystem(15,13,-1,-1)
debug_equation.PrintSystem()
# Solve the first system using Gauss-Seidel
start = time.time()
solution1, residuals1, times1 = gs.SolveGauss(equation1, 1e-9, 1000)
end = time.time()
print("1) Łączny czas: " + str(end-start) + "s")
gp.PlotTimeAndResidual(times1,residuals1)

# debug_solution, debug_residuals, debug_times = jc.SolveJacobi(
#     debug_equation, 1e-9, 10000)
# gp.PlotTimeAndResidual(debug_times, debug_residuals)
## Solve the first system using Jacobi
start = time.time()
solution3, residuals3, times3 = jc.SolveJacobi(equation1, 1e-9, 1000)
end = time.time()
print("2) Łączny czas: " + str(end-start) + "s")
gp.PlotTimeAndResidual(times3, residuals3)

# #Solve the second system using Gauss-Seidel
if prod:
    start = time.time()
    solution2, residuals2, times2 = gs.SolveGauss(equation2, 1e-9, 1000)
    end = time.time()
    print("3) Łączny czas: " + str(end-start) + "s")
    gp.PlotTimeAndResidual(times2, residuals2)

    #Solve the second system using Jacobi
    start = time.time()
    solution4, residuals4, times4 = jc.SolveJacobi(equation2, 1e-9, 1000)
    end = time.time()
    print("4) Łączny czas: " + str(end-start) + "s")
    gp.PlotTimeAndResidual(times4, residuals4)

# Solve the first system using LU factorization
solution3, residuals3, times3 = lu.SolveLU(equation1, 1e-9, 1000)
print("Residuum: " + str(residuals3) + " Czas: " + str(times3) + "s")

# Solve the second system using LU factorization
solution4, residuals4, times4 = lu.SolveLU(equation2, 1e-9, 1000)
print("Residuum: " + str(residuals4) + " Czas: " + str(times4) + "s")

equation3 = eq.BandMatrixSystem()
equation3.CreateNewSystem(100, 13, -1, -1)
equation3.CreateNewSystem(500, 13, -1, -1)
gauss_times = []
jacobi_times = []
LU_times = []
iternum = []
iternum.append(100)
iternum.append(500)
for j in range(1, i+1):
    equation3.CreateNewSystem(1000*j, 13, -1, -1)
    iternum.append(1000*j)
    
for j in range(0, i+2):
    start = time.time()
    gs.SolveGauss(equation3, 1e-9, 1000,j)
    end = time.time()
    print("Gauss time " + str(j) + ": " + str(end-start) + "s")
    gauss_times.append(end-start)
    start = time.time()
    jc.SolveJacobi(equation3, 1e-9, 1000,j)
    end = time.time()
    print("Jacobi time " + str(j) + ": " + str(end-start) + "s")
    jacobi_times.append(end-start)
    start = time.time()
    lu.SolveLU(equation3, 1e-9, 1000,j)
    end = time.time()
    print("LU time " + str(j) + ": " + str(end-start) + "s")
    LU_times.append(end-start)
    print("completed:" + str((j+1)/(i+2)*100) + "%")

if prod: 
    gp.PlotTimeAndNumberOfIterations_log(iternum, gauss_times, jacobi_times, LU_times)
    gp.PlotTimeAndNumberOfIterations(iternum, gauss_times, jacobi_times, LU_times)

#debug numpy implementation benchmark
if prod==0:
    numpy_times = []
    for j in range (0,i+2):
        start = time.time()
        eq_A, eq_b, eq_x = equation3.GetSystem(j)
        np.linalg.solve(eq_A, eq_b)
        end = time.time()
        numpy_times.append(end-start)
        print("completed:" + str((j+1)/(i+2)*100) + "%")
        print("numpy time " + str(j) + ": " + str(end-start) + "s")

    gp.PlotTimeAndNumberOfIterations_log(iternum, gauss_times, jacobi_times, LU_times, numpy_times)
    gp.PlotTimeAndNumberOfIterations(iternum, gauss_times, jacobi_times, LU_times, numpy_times)