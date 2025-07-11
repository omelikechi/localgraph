# Exporting and manually editing graphs in Gephi

[**Gephi**](https://gephi.org/) is an open-source graph visualization and exploration platform.  
It offers an intuitive interface for adjusting node positions, styling edges, and exporting publication-ready network figures. 

This guide explains how to:
- Export graphs from `localgraph` to Gephi
- Manually adjust the layout
- Re-import the modified graph layout back into Python for further use

The following workflow is especially useful for preparing publication-quality figures.

---

## Example workflow

### Step 1: Import data and run PFS

```python
# Assume you have an n-by-p data matrix X
from localgraph import pfs, plot_graph

target_features = [0]
qpath_max = 0.2
max_radius = 3

Q = pfs(X, target_features, qpath_max, max_radius=max_radius)
```

---

### Step 2: Plot and export the graph

```python
plot_args = {
	'graph': Q,
	'target_features': target_features,
	'radius': max_radius,
	'save_graph': True,
	'graph_name': 'my_graph'
}

plot_graph(**plot_args)
```

This will save the graph as a `.graphml` file named `my_graph.graphml`.

---

## Editing the graph in Gephi

1. Open **Gephi**.
2. Go to **File → Open**, and select `my_graph.graphml`.
3. If the graph appears collapsed:
   - Open the **Layout** panel (bottom left).
   - Select **"Noverlap"** from the dropdown menu and click **Run**.
4. Manually adjust the node positions as desired.
5. To save the adjusted layout:
   - Go to **File → Export → Graph File...**
   - Save the file as `my_graph_adjusted.graphml`.

---

## Load the adjusted layout in Python

```python
import networkx as nx
from localgraph import plot_graph

# Load manually adjusted graph
G_updated = nx.read_graphml('my_graph_adjusted.graphml')

# Extract node positions
pos_updated = {
	int(node): (float(data['x']), float(data['y']))
	for node, data in G_updated.nodes(data=True)
}

# Convert node labels to integers
G_updated = nx.relabel_nodes(G_updated, lambda x: int(x))
pos_updated = {int(k): v for k, v in pos_updated.items()}

# Re-plot using adjusted layout
plot_graph(
	graph=G_updated,
	target_features=target_features,
	radius=max_radius,
	pos=pos_updated,
	feature_names=feature_names
)
```

