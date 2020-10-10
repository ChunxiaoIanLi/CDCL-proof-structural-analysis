import sys

def compute_modularity(m, vwpairs, expected_edge):
	q = (vwpairs - expected_edge * vwpairs) / (2 * m)
	return q

def generate_hierarchy_bottom_up(k, c, m, vwpairs, expected_edge, level, k_minus):
	if level == 5:
		return
	i = 0
	if level == 1:
		i = k - k_minus
		#initial total number of edges
		m = (c * (k**2 - k) + (c**2 - c) * i * k)/2
		#initial number of vw pairs, where v!=w and v, w are both from the same community.
		vwpairs = c * (k**2 - k)
		#initial (kv*kw)/2m
		expected_edge = float((k - 1 + (c - 1) * i)**2) / (2 * m)


	current_q = compute_modularity(m, vwpairs, expected_edge)
	if level == 1:
		print("level: {0} i: {1} k: {2} i/k: {3} q: {4}".format(level, i, k, float(i)/k, current_q))
	
	# print(m, vwpairs, expected_edge)
	# print(current_q)
	i = 1
	while True:
		#look for largest i that satisfies next_q > current_q
		next_k = c * k
		next_m = (c * m * 2 + (c**2 - c) * i * next_k)/2
		next_vwpairs = c * m * 2
		next_expected_edge = float((m * 2/ next_k + (c - 1) * i)**2) / (2 * next_m)
		# print(next_m, next_vwpairs, next_expected_edge)
		# print(compute_modularity(next_m, next_vwpairs, next_expected_edge))
		next_q = compute_modularity(next_m, next_vwpairs, next_expected_edge)
		if next_q <= current_q:
			break
		i += 1
	i = i - 1
	next_k = c * k
	next_m = (c * m * 2 + (c**2 - c) * i * next_k)/2
	next_vwpairs = c * m * 2
	next_expected_edge = float((m * 2/ next_k + (c - 1) * i)**2) / (2 * next_m)
	# print(next_m, next_vwpairs, next_expected_edge)
	# print(compute_modularity(next_m, next_vwpairs, next_expected_edge))
	next_q = compute_modularity(next_m, next_vwpairs, next_expected_edge)

	level += 1
	print("level: {0} i: {1} k: {2} i/k: {3} q: {4}".format(level, i, next_k, float(i)/next_k, next_q))
	generate_hierarchy_bottom_up(next_k, c, next_m, next_vwpairs, next_expected_edge, level, k_minus)
	return

#size of each community
k = int(sys.argv[1])
#degree of the hierarchy tree
c = int(sys.argv[2])
#i = k - k_minus
if len(sys.argv) == 4:
	k_minus = int(sys.argv[3])
else:
	k_minus = 2

#initial total number of edges
m = 0
#initial number of vw pairs, where v!=w and v, w are both from the same community.
vwpairs = 0
#initial (kv*kw)/2m
expected_edge = 0
level = 1



generate_hierarchy_bottom_up(k, c, m, vwpairs, expected_edge, level, k_minus)



