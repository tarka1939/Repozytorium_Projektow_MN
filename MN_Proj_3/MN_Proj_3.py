#Interpolation of elevation profiles: Lagrange polynomial vs natural cubic spline,
#on evenly spaced vs Chebyshev nodes.
#usage: python MN_Proj_3.py               (show the plots)
#       python MN_Proj_3.py --save DIR    (write the plots to DIR as PNG files instead)
import glob
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import interpolation as ip

ROUTE = "Hel_yeah.csv"       #route used for the example plots
NODES = [10, 25, 50]         #numbers of nodes in the example plots
TABLE_NODES = [5, 10, 15, 25, 50]
NODE_TYPES = {"evenly spaced": ip.get_evenly_spaced_nodes, "Chebyshev": ip.get_chebyshev_nodes}
METHODS = {"Lagrange": ip.lagrange_interpolation, "cubic spline": ip.cubic_spline_interpolation}
SHORT = {"evenly spaced": "even", "Chebyshev": "Cheb", "Lagrange": "Lagrange", "cubic spline": "spline"}
MIN_SAMPLES = 100            #shorter files (profil_etapu.csv) are toy examples, left out of the statistics

save_dir = sys.argv[sys.argv.index("--save") + 1] if "--save" in sys.argv else None
if save_dir:
    os.makedirs(save_dir, exist_ok=True)

def show(name):
    if save_dir:
        plt.savefig(os.path.join(save_dir, name + ".png"), dpi=100)
        plt.close()
    else:
        plt.show()

def plot(x, y, x_nodes, y_nodes, x_dense, y_lagrange, y_spline, title, name):
    #the y axis is limited to the data range, so a diverging polynomial leaves the chart instead of flattening it
    ymin = min(y) - 0.1 * abs(min(y))
    ymax = max(y) + 0.1 * abs(max(y))
    plt.figure(figsize=(10, 6))
    plt.ylim([ymin, ymax])
    plt.plot(x, y, label='Elevation profile', linestyle="-")
    plt.plot(x_nodes, y_nodes, 'x', label='Nodes')
    plt.plot(x_dense, y_lagrange, label='Lagrange polynomial')
    plt.plot(x_dense, y_spline, label='Natural cubic spline', linestyle='--')
    plt.xlabel('Distance (m)')
    plt.ylabel('Elevation (m)')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    show(name)

#example plots for one route
x, y = ip.load_profile(ROUTE)
x_dense = np.linspace(x.min(), x.max(), 1000)
for n in NODES:
    for node_type, get_nodes in NODE_TYPES.items():
        x_nodes, y_nodes = get_nodes(x, y, n)
        y_lagrange = ip.lagrange_interpolation(x_nodes, y_nodes, x_dense)
        y_spline = ip.cubic_spline_interpolation(x_nodes, y_nodes, x_dense)
        plot(x, y, x_nodes, y_nodes, x_dense, y_lagrange, y_spline,
             f"{ROUTE}: {n} {node_type} nodes", f"{os.path.splitext(ROUTE)[0]}_{n}_{node_type.split()[0].lower()}")

#errors on every route: each interpolant is compared with the profile at all of its samples
routes = [p for p in sorted(glob.glob("*.csv") + glob.glob("*.txt") + glob.glob("*.data")) if p != "requirements.txt"]
combinations = [(node_type, method) for node_type in NODE_TYPES for method in METHODS]
relative = {(n, c): [] for n in TABLE_NODES for c in combinations}
print("RMSE [m] with 25 nodes (largest absolute error in brackets)")
print(f"{'route':26s} {'length':>8s} {'range':>7s}" + "".join(f"{SHORT[nt] + '/' + SHORT[m]:>24s}" for nt, m in combinations))
for route in routes:
    x, y = ip.load_profile(route)
    if len(x) < MIN_SAMPLES:
        continue
    elevation_range = y.max() - y.min()
    row = f"{route:26s} {x.max() / 1000:6.1f}km {elevation_range:6.0f}m"
    for n in TABLE_NODES:
        for node_type, method in combinations:
            x_nodes, y_nodes = NODE_TYPES[node_type](x, y, n)
            rmse, max_error = ip.errors(y, METHODS[method](x_nodes, y_nodes, x))
            relative[(n, (node_type, method))].append(rmse / elevation_range)
            if n == 25:
                row += f"{rmse:>12.3g} ({max_error:>8.3g})"
    print(row)

route_count = len(relative[(TABLE_NODES[0], combinations[0])])
print(f"\nMedian over {route_count} routes of RMSE / elevation range of the route")
print(f"{'nodes':>5s}" + "".join(f"{SHORT[nt] + '/' + SHORT[m]:>16s}" for nt, m in combinations))
for n in TABLE_NODES:
    print(f"{n:5d}" + "".join(f"{np.median(relative[(n, c)]):16.3g}" for c in combinations))

plt.figure(figsize=(10, 6))
for c in combinations:
    plt.plot(TABLE_NODES, [np.median(relative[(n, c)]) for n in TABLE_NODES], marker='o', label=f"{c[1]}, {c[0]} nodes")
plt.yscale('log')
plt.xlabel('Number of nodes')
plt.ylabel('Median RMSE / elevation range')
plt.title(f'Interpolation error over {route_count} elevation profiles')
plt.legend()
plt.grid(True, which='both')
show("error_vs_nodes")
