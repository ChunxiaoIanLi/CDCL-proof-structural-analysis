test: test_pmi


# Test PMILib
test_pmi: libmergeability.so PMILib.py
	python testPMI.py

libmergeability.so:
	cp resolvability/libmergeability.so .

PMILib.py:
	cp resolvability/PMILib.py .