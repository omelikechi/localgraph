# Local graph estimation with pathwise feature selection

> **Local graph estimation** is a framework for discovering local graph/network structure around specific variables of interest. **Pathwise feature selection (PFS)** is an algorithm for performing local graph estimation with pathwise false discovery control.

## Associated paper

- **Local graph estimation: Interpretable network discovery for complex data**  
	[Nature Communications](https://doi.org/10.1038/s41467-026-72796-9) • [arXiv](https://doi.org/10.48550/arXiv.2507.17172)

## Installation
```
pip install localgraph
```

## Usage
```python
from localgraph import pfs, plot_graph

# Load n-by-p data matrix X (n samples, p features)

# Specify the target features (list of indices)
target_features = [0, 1]

# Specify the pathwise q-value threshold
qpath_max = 0.2

# Optional: specify the maximum radius of the local graph (default is 3)
max_radius = 3

# Optional: specify the neighborhood FDR thresholds for nodes in each radius
fdr_local = [0.2, 0.1, 0.1]

# Run PFS (uses all available cores by default; set n_jobs=1 to disable parallelism)
Q = pfs(X, target_features, qpath_max=qpath_max, max_radius=max_radius, fdr_local=fdr_local)

# Plot the estimated subgraph
plot_graph(graph=Q, target_features=target_features, radius=max_radius)
```

### Outputs
- `Q`: Dictionary mapping edges `(i,j)` to q-values. Edges are undirected, so `(i,j)` and `(j,i)` are included.

### What PFS does
- Expands the local graph outward, layer by layer, starting from target variables.
- Performs neighborhood selection with FDR control using [**integrated path stability selection**](https://github.com/omelikechi/ipss).
- Controls pathwise false discoveries by summing q-values along candidate paths.

## Full list of `pfs` arguments

### Required arguments:
- `X`: n-by-p data matrix (NumPy array). Each column is a feature/variable.
- `target_features`: Feature index or list of indices to center the graph around.
- `qpath_max`: Maximum allowed sum of q-values along any path.

### Optional arguments:
- `max_radius`: Maximum number of expansion layers around each target (int; default `3`).
- `fdr_local`: Neighborhood FDR threshold at each radius (list of length `max_radius`; default `[qpath_max]*max_radius`).
- `custom_nbhd`: Dictionary specifying custom FDR cutoffs for certain features (dict; default `None`).
- `feature_names`: List of feature names; required if `custom_nbhd` is provided (list of strings).
- `criterion`: Rule for resolving multiple edges (default `'min'`).
- `n_jobs`: Number of cores to use for parallel computation (int; default `-1` uses all available cores). Passed directly to `qvalue_method`; has no effect for custom methods that do not support `n_jobs`. On machines with multiple cores this can substantially reduce runtime.
- `qvalue_method`: A method for computing q-values (function)
- `method_args`: Dictionary of arguments to pass to `qvalue_method` (dict; default `None`). Any `n_jobs` key here takes precedence over the `n_jobs` argument.
- `verbose`: Whether to print progress during selection (bool; default `False`)

## Graph plotting

Use `plot_graph` to visualize a local graph up to the specified `radius` around one or more target features.

```python
from localgraph import plot_graph

# Plot local graph around target_features using output Q from pfs
plot_graph(graph=Q, target_features=target_features, radius=3)
```

### Features and customization
`plot_graph` visualizes a local graph of a user-specified radius around one or more target features. It supports:
- Flexible input formats: edge dictionary, adjacency matrix, or NetworkX graph
- Automatic subgraph extraction around the targets
- Node coloring by distance from the target(s) (default), or user-specified colors (e.g., by variable type)
- Several layout algorithms (`'kamada_kawai'`, `'spring'`, `'circular'`, etc.)
- Customizable node size, font sizes, and edge thickness
- Optional display of q-values; edge widths can reflect q-value strength (`edge_widths='q_value'`)
- False positives shown in red if the true graph is provided
- Integration with custom plots via `ax` or `pos`
- Optional saving of figures (`save_fig`) and graphs (`save_graph`)

For a full list of arguments, see the [`plot_graph`](./localgraph/plotting/plot_graph.py) docstring.

### Returns
The function returns a dictionary containing:
- `feature_radius_list`: List of `(feature name, radius)` pairs for all nodes in the graph.
- `graph`: The NetworkX subgraph used for plotting.
- `positions`: Dictionary of node coordinates.
- `figure`: The matplotlib figure object (only if the function creates the figure).

### Further customization

To manually adjust node positions for publication-quality figures, you can export graphs to [**Gephi**](https://gephi.org/), edit them interactively, and re-import the updated layout into Python. See: [gephi_instructions.md](./gephi_instructions.md) for a full walkthrough.

## Examples

The `examples/` folder contains scripts that demonstrate end-to-end usage:

- `simple_example.py`: Simulate data, run PFS, and visualize the result.

## Evaluation tools

The `evaluation/` folder contains helper functions for measuring subgraph recovery in simulation settings.

- The `eval.py` script contains one function:
	- `tp_and_fp`: Count true and false positives compared to ground truth

These are useful for benchmarking PFS and other graph estimation methods when the true graph is known.
