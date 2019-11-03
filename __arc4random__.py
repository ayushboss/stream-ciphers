import sp800_22_tests
import arc4random
import time

instance_amnt = int(input("# of instances: "))
bits_per_instance = int(input("# of bits per instance: "))

sp800_22_tests.append_header("cluster_data_arc4random.csv")

for s in range(instance_amnt):
	print("----------------------  Iteration " + str(s) + "  ----------------------")
	bits=[]
	start_time = time.time()
	for x in range(100):	
		bits.append(arc4random.randsample(0,1,int(bits_per_instance/100)))
		print("Generating Bits: " + str(x))
	end = time.time()
	print("Duration: " + str(end-start_time))
	sp800_22_tests.test_func(bits, "cluster_data_arc4random.csv")
