import sp800_22_tests
import compress_bin_files
from randomgen import RandomGenerator
instance_amnt = int(input("# of instances: "))
bits_per_instance = int(input("# of bits per instance: "))

sp800_22_tests.append_header("sp800_collected_cluster_data_xoroshiro.csv")

rnd = RandomGenerator();

for s in range(instance_amnt):
	print("----------------------  Iteration " + str(s) + "  ----------------------")
	bits = list(rnd.randint(low=0, high=2, size=bits_per_instance))
	sp800_22_tests.test_func(bits, "sp800_collected_cluster_data_xoroshiro.csv")
compress_bin_files.compress("compression_ratio_cluster_data_xoroshiro.csv")
