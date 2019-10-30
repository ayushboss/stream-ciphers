import sp800_22_tests
from randomgen import RandomGenerator, Philox
instance_amnt = int(input("# of instances: "))
bits_per_instance = int(input("# of bits per instance: "))

sp800_22_tests.append_header("cluster_data_philox.csv")

rnd = RandomGenerator(Philox());

for s in range(instance_amnt):
	print("----------------------  Iteration " + str(s) + "  ----------------------")
	bits = list(rnd.randint(low=0, high=2, size=bits_per_instance))
	sp800_22_tests.test_func(bits, "cluster_data_philox.csv")
