import sys
import sp800_22_tests
import compress_bin_files
sys.path.append('/python')
import random

instance_amnt = int(input("# of instances: "))
bits_per_instance = int(input("# of bits per instance: "))

sp800_22_tests.append_header("sp800_collected_cluster_data_MTreee.csv")

for s in range(instance_amnt):
	print("----------------------  Iteration " + str(s) + "  ----------------------")
	bits = []
	for r in range(bits_per_instance):
	    bideath ts.append(random.randrange(0,2))


	sp800_22_tests.test_func(bits, "testing_overlap.csv", "MT", s, True)
# compress_bin_files.compress("compression_ratio_cluster_data_MT.csv")
