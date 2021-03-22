# Parameter Computation
The scripts in this directory can be used to compute various non-HCS-based parameter values over a CNF formula.
The Makefile in this directory will compile the code. Run this Makefile using `make`.

# compute_params
This is a standalone script which is used to compute clause-variable ratio, degree vector, and mergeability-related parameters over a CNF formula.
Usage: `./compute_params <OPTION [OPTIONS...]> <CNF_PATH [CNF_PATHS...]>`
	* `OPTION`:
		- `-a`: enable all computations
		- `-c`: compute clause-variable ratio (CVR)
		- `-d`: compute degree vector
		- `-r`: compute resolvability- and mergeability-related parameters
	* `CNF_PATH`: the path to the CNF file over which to compute parameter values.

# libmergeability.so
This is a dynamically-linked library for exposing the parameter computation capabilities of `compute_params` to python.

# PMILib.py
This is a python class which provides a convenient interface for working with the parameter computation from `compute_params`.
Note that this interface requires `libmergeability.so`, which can be compiled using the provided Makefile.

# libmergeabilityExample.py
This is a script which serves as an example for using `PMILib.py`.
Usage: `python ./libmergeabilityExample.py`

# test_PMI.py
This script runs unit tests on `PMILib.py`. This test relies on I/O tools in `../hcs-param-computation`. The Makefile in this directory will fetch the appropriate code.
Usage: `python ./test_PMI.py`
