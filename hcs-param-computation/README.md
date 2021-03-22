# Hierarchical Community Structure Parameter Computation
The scripts in this directory can be used to compute HCS parameter values over a CNF formula.
These scripts are dependent on the parameter computation tools in `../param-computation/`. The Makefile in this directory will compile and fetch the appropriate code. Run this Makefile using `make`.
These scripts are also dependent on python-igraph, which needs to be installed separately. Installation instructions are available [here](https://igraph.org/python/)

## clustering_ed.py
This script recursively computes HCS parameters.
Usage: `python ./clustering_ed.py <CNF_PATH>`
  * `CNF_PATH`: the path to the CNF formula over which to calculate HCS parameters.

## test_clustering_ed.py
This script runs unit tests on `clustering_ed.py`.
Usage: `python ./test_clustering_ed.py`

## HCS_query.py
This script aggregates the output data from `clustering_ed.py` to produce a summary of the HCS decomposition.
This script should be run after running `clustering_ed.py`.
Usage: `python ./HCS_query.py <CNF_PATH>`
  * `CNF_PATH`: the path to the CNF formula over which to summarize the HCS decomposition.

## test_HCS_query.py
This script runs unit tests on `HCS_query.py`.
Usage: `python ./test_HCS_query.py`
