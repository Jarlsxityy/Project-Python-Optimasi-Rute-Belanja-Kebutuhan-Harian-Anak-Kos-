import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# 1. DATA: titik dan matriks jarak (km)
titik = ["Kos", "Sembako", "Galon", "Laundry", "Fotokopi", "ATM"]
jarak = np.array([
    [0, 0.5, 0.8, 0.4, 1.2, 1.0],
    [0.5, 0, 0.4, 0.6, 0.9, 0.7],
    [0.8, 0.4, 0, 0.9, 0.6, 0.5],
    [0.4, 0.6, 0.9, 0, 1.0, 1.1],
    [1.2, 0.9, 0.6, 1.0, 0, 0.3],
    [1.0, 0.7, 0.5, 1.1, 0.3, 0],
])

def total(rute): # jarak Kos -> rute -> Kos
    p = [0, *rute, 0]
    return sum(jarak[a][b] for a, b in zip(p, p[1:]))

# 2. ALGORITMA
bf = min(itertools.permutations(range(1, 6)), key=total)   # Brute Force (5! = 120 rute)

nn, now = [], 0                                            # Nearest Neighbor
while len(nn) < 5:
    now = min(set(range(1, 6)) - set(nn), key=lambda j: jarak[now][j])
    nn.append(now)

asal = range(1, 6)                                         # rute asal-asalan (pembanding)
nama = lambda r: " -> ".join(titik[i] for i in [0, *r, 0])
for judul, r in [("Brute Force", bf), ("Nearest Neighbor", nn), ("Asal-asalan", asal)]:
    print(f"{judul:17}: {nama(r)} = {total(r):.1f} km")
print(f"Penghematan      : {total(asal) - total(bf):.1f} km")

# 3. GRAF BERBOBOT: semua jarak tampil, rute optimal merah
G = nx.Graph([(titik[i], titik[j], {"weight": jarak[i][j]}) for i in range(6) for j in range(i+1, 6)])
pos = nx.circular_layout(G)
p = [0, *bf, 0]
merah = [(titik[a], titik[b]) for a, b in zip(p, p[1:])]

plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2500, edge_color="gray")
nx.draw_networkx_edges(G, pos, edgelist=merah, edge_color="red", width=3)
nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, "weight"), label_pos=0.3, font_size=9)
plt.title(f"Rute Optimal Belanja Anak Kos: {total(bf):.1f} km\n{nama(bf)}", fontsize=10)
plt.savefig("rute_optimal.png", dpi=150, bbox_inches="tight")
plt.show()
