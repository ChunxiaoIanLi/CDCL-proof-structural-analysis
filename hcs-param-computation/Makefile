HCS_PARAM_COMPUTATION_DIR = ../hcs-param-computation
PARAM_COMPUTATION_DIR = ../param-computation
PY_INTERFACE = PMILib.py
PMI_LIB = libmergeability.so

.PHONY: all clean	

all: $(PY_INTERFACE) $(PMI_LIB)

$(PY_INTERFACE):
	cp $(PARAM_COMPUTATION_DIR)/$(PY_INTERFACE) .

$(PMI_LIB):
	cd $(PARAM_COMPUTATION_DIR) && $(MAKE)
	cp $(PARAM_COMPUTATION_DIR)/$(PMI_LIB) .

clean:
	rm *.pyc $(PY_INTERFACE) $(PMI_LIB)
