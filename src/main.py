import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# 1. data, titik titik dan jarak
titik = ["Kos", "ATM", "Sembako", "Galon", "Fotokopi", "Laundry"]
jarak = np.array([
    [0.0, 0.4, 1.9, 1.8, 1.6, 0.4],
    [0.4, 0.0, 1.6, 1.8, 1.6, 0.7],
    [1.9, 1.6, 0.0, 1.7, 1.7, 1.9],
    [1.8, 1.8, 1.7, 0.0, 0.3, 1.5],
    [1.6, 1.6, 1.7, 0.3, 0.0, 1.2],
    [0.4, 0.7, 1.9, 1.5, 1.2, 0.0],
])
n = len(titik)
assert np.allclose(jarak, jarak.T), "Matriks jarak harus simetris"

def total(rute): # jarak Kos -> rute -> Kos
    path = [0, *rute, 0]
    return round(sum(jarak[a][b] for a, b in zip(path, path[1:])), 2)

# 2. algoritma
bf = min(itertools.permutations(range(1, n)), key=total) 

nn, now = [], 0 
while len(nn) < n - 1:
    now = min(set(range(1, n)) - set(nn), key=lambda j: jarak[now][j])
    nn.append(now)

asal = [titik.index(t) for t in ["Sembako", "Galon", "Laundry", "Fotokopi", "ATM"]] 
nama = lambda r: " -> ".join(titik[i] for i in [0, *r, 0])
for judul, r in [("Brute Force", bf), ("Nearest Neighbor", nn), ("Asal-asalan", asal)]:
    print(f"{judul:17}: {nama(r)} = {total(r):.1f} km")
print(f"Penghematan      : {total(asal) - total(bf):.1f} km")

# 3. graf berbobot
G = nx.Graph([(titik[i], titik[j], {"weight": jarak[i][j]}) for i in range(n) for j in range(i+1, n)])
pos = nx.circular_layout(G)
path = [0, *bf, 0]
merah = [(titik[a], titik[b]) for a, b in zip(path, path[1:])]
merah_set = {frozenset(e) for e in merah}

fig, ax = plt.subplots(figsize=(8, 6))
nx.draw(G, pos, ax=ax, with_labels=True, node_color="lightblue", node_size=2500, edge_color="gray")
nx.draw_networkx_edges(G, pos, edgelist=merah, edge_color="red", width=3, ax=ax)

# label manual
for i in range(n):
    for j in range(i + 1, n):
        t = 0.3 if j - i == 3 else 0.5
        x, y = (1 - t) * pos[titik[i]] + t * pos[titik[j]]
        aktif = frozenset((titik[i], titik[j])) in merah_set
        ax.text(x, y, f"{jarak[i][j]:.1f}", ha="center", va="center", fontsize=9,
                color="red" if aktif else "black", fontweight="bold" if aktif else "normal",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9), zorder=5)

ax.set_title(f"Rute Optimal Belanja Anak Kos: {total(bf):.1f} km\n{nama(bf)}", fontsize=10)
plt.savefig("rute_optimal.png", dpi=150, bbox_inches="tight")
plt.show()
