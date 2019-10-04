import sp800_22_tests
from randomgen import RandomGenerator, ThreeFry
instance_amnt = int(input("# of instances: "))
bits_per_instance = int(input("# of bits per instance: "))

sp800_22_tests.append_header("cluster_data_threefry.csv")

rnd = RandomGenerator(ThreeFry());

for s in range(instance_amnt):
	print("----------------------  Iteration " + str(s) + "  ----------------------")
	bits = list(rnd.randint(low=0, high=2, size=bits_per_instance))
	sp800_22_tests.test_func(bits, "cluster_data_threefry.csv")
