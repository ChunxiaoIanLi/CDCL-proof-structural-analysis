# Hierarchical Community Structure Instance Generator
The scripts in this directory can be used to generate a CNF formula with user-specified HCS parameter values.
These scripts are partially dependent on the tools in `../hcs-param-computation/`. The Makefile in this directory will fetch the appropriate code. Run this Makefile using `make`.

## HCS_to_CNF_direct.py
This script generates a CNF formula using user-specified HCS parameter values.
This script requires `python3`, and is dependent on `generate_random_degree_distribution.py`.
Note that there are parameters which our parameter can scale but which are not presented as input parameters here. These parameter values are currently computed as fucntions of the input parameters:

  * powerlaw exponent: The powerlaw exponent is computed as a function of the clause width.
  * CVR: the CVR is a vector of numbers which is computed as a function of the depth.

Usage: `python3 ./HCS_to_CNF_direct.py <DEPTH> <LEAF_SIZE> <INTER_VAR_DENSITY> <DEGREE> <CLAUSE_WIDTH> <OUT_CNF>`

  * `DEPTH`: the depth of the hierarchical tree.
  * `LEAF_SIZE`: the number of variables in a leaf-community.
  * `INTER_VAR_DENSITY`: the fraction of variables (between 0 and 1) which participate in inter-community edges.
  * `DEGREE`: the number of child sub-communities for each non-leaf-community.
  * `CLAUSE_WIDTH`: the maximum number of variables in a clause.
  * `OUT_CNF`: the desired output file name for the generated CNF formula.

## test_HCS_to_CNF_direct.py
This script runs unit tests on `HCS_to_CNF_direct.py`.

Usage: `python3 ./test_HCS_to_CNF_direct.py`
