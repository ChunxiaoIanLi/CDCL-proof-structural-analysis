PMI_TEST = test_PMI.py
HCS_CNF_TEST = test_HCS_to_CNF.py
VIG_CNF_TEST = test_VIG_to_CNF.py

.PHONY: $(PMI_TEST) $(HCS_CNF_TEST)
test: $(PMI_TEST) $(HCS_CNF_TEST)

# Test PMILib
PMI_DIR = resolvability
PMI_DLL = libmergeability.so
PMI_LIB = PMILib.py
$(PMI_TEST): $(PMI_DLL) $(PMI_LIB)
	python $(PMI_TEST)
	rm $(PMI_DLL) $(PMI_LIB)

$(PMI_DLL):
	cp $(PMI_DIR)/$(PMI_DLL) .

$(PMI_LIB):
	cp $(PMI_DIR)/$(PMI_LIB) .

# Test HCS to CNF
$(HCS_CNF_TEST):
	python $(HCS_CNF_TEST) 2 10 0.4 2 80 3

# Test VIG to CNF
$(VIG_CNF_TEST):
	python $(VIG_CNF_TEST) mergeability_test_suite/1.cnf 50 3
