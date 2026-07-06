# Repozytorium Projektów MN (Numerical Methods Projects)

This repository collects three academic projects built for a **Numerical Methods** ("Metody Numeryczne") course. Each project implements a classical numerical algorithm from scratch (rather than relying on a black-box library call) and applies it to a realistic dataset, then benchmarks or visualizes the results. Together they demonstrate core computational techniques that show up repeatedly in quantitative finance, engineering simulation, and geospatial/data analytics — domains where correctness, performance, and numerical stability have direct business impact.

## Repository Structure

| Project | Folder | Topic |
|---|---|---|
| Project 1 | [MN_Proj_1/](MN_Proj_1) | Time-series signal processing & trading strategy backtesting (MACD) |
| Project 2 | [MN_Proj_2/](MN_Proj_2) | Iterative & direct solvers for large linear systems (Jacobi, Gauss-Seidel, LU) |
| Project 3 | [MN_Proj_3/](MN_Proj_3) | Function interpolation (Lagrange, cubic splines, Chebyshev nodes) on terrain elevation data |

---

## Project 1 — MACD Trading Signal Simulation

**Location:** [MN_Proj_1/MN_Proj_1](MN_Proj_1/MN_Proj_1)

Implements the **Moving Average Convergence/Divergence (MACD)** technical indicator from first principles (recursive exponential moving average, [MACD_implementation.py](MN_Proj_1/MN_Proj_1/MACD_implementation.py)), then uses it to drive a simple buy/sell trading simulation ([simulation.py](MN_Proj_1/MN_Proj_1/simulation.py)) over historical price data ([data.csv](MN_Proj_1/MN_Proj_1/data.csv)), with results plotted via [graphing.py](MN_Proj_1/MN_Proj_1/graphing.py).

**Business value:** This mirrors the core building block of algorithmic and quantitative trading systems — turning noisy time-series data into actionable buy/sell signals and measuring strategy profitability (win/loss counts, capital growth) before risking real capital. The same pattern (signal extraction → backtest → P&L evaluation) generalizes to any organization building automated trading, risk-signal, or anomaly-detection pipelines on streaming/financial data.

## Project 2 — Linear System Solvers & Performance Benchmarking

**Location:** [MN_Proj_2/MN_Proj_2](MN_Proj_2/MN_Proj_2)

Generates large banded ("pięciodiagonalna") matrix systems ([Equation.py](MN_Proj_2/MN_Proj_2/Equation.py)) and solves them using three independently implemented methods:
- **Jacobi iteration** ([Jacobo.py](MN_Proj_2/MN_Proj_2/Jacobo.py))
- **Gauss-Seidel iteration** ([Gauss_Seidl.py](MN_Proj_2/MN_Proj_2/Gauss_Seidl.py))
- **LU factorization** ([LU_Factor.py](MN_Proj_2/MN_Proj_2/LU_Factor.py))

[MN_Proj_2.py](MN_Proj_2/MN_Proj_2/MN_Proj_2.py) benchmarks convergence speed, residual error, and wall-clock time across increasing problem sizes (up to ~4000 unknowns), plotting the results (including log-scale comparisons) via [Graphing.py](MN_Proj_2/MN_Proj_2/Graphing.py).

**Business value:** Solving large sparse/banded linear systems efficiently is foundational to engineering simulation (structural analysis, circuit simulation, fluid dynamics, PDE solvers), computer graphics, and large-scale optimization. This project quantifies the real-world trade-off between iterative methods (cheap per step, scale well, but may converge slowly or not at all) and direct methods (numerically robust, but costlier) — the same trade-off engineering and simulation teams must make when choosing solvers for production systems where compute cost and accuracy both matter.

## Project 3 — Interpolation of Elevation Profiles

**Location:** [MN_Proj_3/](MN_Proj_3)

Reads real-world elevation/distance profile data (multiple cycling/hiking route CSVs, e.g. [MountEverest.csv](MN_Proj_3/MountEverest.csv), [WielkiKanionKolorado.csv](MN_Proj_3/WielkiKanionKolorado.csv), [SpacerniakGdansk.csv](MN_Proj_3/SpacerniakGdansk.csv)) and reconstructs continuous elevation curves from a sparse set of sampled points using:
- **Lagrange polynomial interpolation**
- **Cubic spline interpolation**
- **Chebyshev node sampling** (to reduce oscillation/error at the edges of the interpolation range — Runge's phenomenon)

Implemented in [MN_Proj_3.py](MN_Proj_3/MN_Proj_3.py) / [MN_Proj_3.1.py](MN_Proj_3/MN_Proj_3.1.py), with results visualized as comparison plots ([Figure_1.png](MN_Proj_3/Figure_1.png)–[Figure_12.png](MN_Proj_3/Figure_12.png)).

**Business value:** Reconstructing smooth, accurate curves from sparse or expensive-to-collect measurements is a recurring problem in GIS/mapping (route and terrain modeling), sensor data reconstruction, and any product that needs to estimate values between known data points. The project's direct comparison of interpolation strategies (and the sampling-node choice that stabilizes them) illustrates how the right numerical technique can materially improve accuracy without needing more raw data — reducing data-collection cost while improving product quality.

---

## Tech Stack

All projects are written in **Python** (Visual Studio Python project files, `.pyproj`/`.sln`), using:
- `numpy` / `pandas` for numerical and tabular data handling
- `matplotlib` (and `mplfinance`) for visualization
- `yfinance` / `ta` for market data and technical indicators (Project 1)
- `scipy` / `sympy` (Project 2, for supporting numerical/symbolic computation)

Each project folder contains its own `requirements.txt` for dependency installation:

```bash
pip install -r requirements.txt
```

## Notes

These are coursework/portfolio projects: algorithms are implemented manually to demonstrate understanding of the underlying numerical methods, rather than optimized production code. They are best read as worked demonstrations of how classical numerical analysis techniques translate into practical, business-relevant capabilities in finance, engineering, and data/geospatial analytics.
