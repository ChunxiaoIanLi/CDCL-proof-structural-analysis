import igraph
import math
import sys
import os
import VIG_to_CNF

def generate_cnf(cnf_dir, n, p, k, m):
	g = igraph.Graph.Erdos_Renyi(n, p=p)
	while len(g.es) == 0: g = igraph.Graph.Erdos_Renyi(n, p=p)
	n = g.vcount()
	cnf = VIG_to_CNF.VIG_to_CNF(g, m, k)
	VIG_to_CNF.write_cnf(cnf, n, m, "{}/{}_{}_{}_{}.cnf".format(cnf_dir, n, p, m, k))

def generate_cnfs(cnf_dir, n, p, k, m_min = None, num_cvr = 20, num_cnf = 10, growth_factor = 1.2, scale_factor = 10):
	"""
	Generate different CNFs to determine the threshold CVR for a given edge density
	@param out_dir: The output directory

	@param n: The number of variables in the CNF
	@param p: The density of the Erdos-Renyi graph
	@param k: The maximum clause width

	@param m_min: The number of clauses to start from
	@param num_cvr: The number of CVRs to consider
	@param num_cnf: The number of CNFs to generate at each CVR
	@param growth_factor: The base of the exponential
	@param scale_factor: The coeffient of the exponential
	"""

	# The lower bound for m is O(p n^2 / k)
	if not m_min: m_min = 0
	m_min = max(m_min, (p * n * (n + 1)) / (2 * k))

	# Grow m exponentially
	for i in range(0, num_cvr):
		m = int(round(m_min + scale_factor * growth_factor**i))

		# Generate CNFs according to the G(n, p) model with m clauses
		for j in range(0, num_cnf):
			cnf = generate_cnf(cnf_dir, n, p, k, m)

def get_parameters_from_filename(filename):
	components = filename.split('_')
	n = int(components[0])
	p = float(components[1])
	m = int(components[2])
	return n, p, m

def get_results(filename):
	solving_time = None
	is_sat = None

	sat_log_file = filename.replace(".cnf", ".log", 1)
	try:
		f = open(file, "r")
		lines = f.read()
		print(lines)
		solving_time = 0
		is_sat = 0
		f.close()
	except:
		solving_time = None
		is_sat = None

	return solving_time, is_sat

def determine_threshold_cvrs(cnf_dir, n, p):
	class CNF_result:
		def update(self, solving_time, is_sat):
			if is_sat:
				self.num_sat += 1
				self.sat_time += solving_time
			else:
				self.num_unsat += 1
				self.unsat_time += solving_time

		def __init__(self, solving_time, is_sat):
			self.sat_time   = 0
			self.unsat_time = 0
			self.num_sat    = 0
			self.num_unsat  = 0
			self.update(solving_time, is_sat)
		
		def get_results(self):
			avg_time = (self.sat_time + self.unsat_time) / (self.num_sat, self.num_unsat)
			sat_time = self.sat_time / self.num_sat
			unsat_time = self.unsat_time / self.num_unsat

			return avg_time, sat_time, unsat_time, self.num_sat, self.num_unsat

	# Compute average solving times
	solving_times = {}
	for cnf in os.listdir(cnf_dir):
		if os.path.isfile(os.path.join(cnf_dir, cnf)):
			n, p, m = get_parameters_from_filename(cnf)
			key = "{},{}".format(n, p)
			solving_time, is_sat = get_results("{}/{}".format(cnf_dir, cnf))
			if solving_time == None:
				continue
			if not (key in solving_times):
				solving_times[key] = {}
			if m in solving_times[key]:
				solving_times[key][m].update(solving_time, is_sat)
			else:
				solving_times[key][m] = CNF_result(solving_time, is_sat)
	
	print("avg_time, sat_time, unsat_time, num_sat, num_unsat")
	for key, result_map in solving_times.items():
		max_solving_time = 0
		threshold_m = 0
		for m, result in solving_times[key].items():
			avg_time, sat_time, unsat_time, num_sat, num_unsat = result.get_results()
			if unsat_time >= max_solving_time:
				threshold_m = m

			print("[{},{}]: {}, {}, {}, {}, {}".format(key, m, avg_time, sat_time, unsat_time, num_sat, num_unsat))

		n, p = key.split(',')
		print("Threshold({}) = {}".format(p, n / threshold_m))

def main():
	delta_p = 0.1

	if len(sys.argv) != 5:
		print("Usage: {} <option> <cnf_dir> <n> <k>".format(sys.argv[0]))
		return

	option = sys.argv[1]
	cnf_dir = sys.argv[2]
	n = int(sys.argv[3])
	k = int(sys.argv[4])

	if option == "generate_cnfs":
		# Generate CNFs of interest
		for i in range(1, int(math.floor(1 / delta_p)) + 1):
			generate_cnfs(cnf_dir, n, delta_p * i, k, num_cvr = 1, num_cnf = 1)
	elif option == "find_thresholds":
		# Find threshold CVRs
		for i in range(1, int(math.floor(1 / delta_p)) + 1):
			determine_threshold_cvrs(cnf_dir, n, delta_p * i)
	else:
		print("Invalid option '{}'".format(option))

if __name__ == "__main__":
	main()