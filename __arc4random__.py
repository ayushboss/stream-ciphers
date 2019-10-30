import sp800_22_tests
import arc4random

instance_amnt = int(input("# of instances: "))
bits_per_instance = int(input("# of bits per instance: "))

sp800_22_tests.append_header("cluster_data_arc4random.csv")

for s in range(instance_amnt):
	print("----------------------  Iteration " + str(s) + "  ----------------------")
	bits = arc4random.randsample(0,1,bits_per_instance)
	print("check")
	sp800_22_tests.test_func(bits, "cluster_data_arc4random.csv")
