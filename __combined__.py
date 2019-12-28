import sp800_22_tests
import random
from randomgen import RandomGenerator, Philox, ThreeFry


instance_amnt = int(input("# of instances for each: "))
bits_per_instance = int(input("# of bits per instance: "))

sp800_22_tests.append_header("cluster_data_combined_2.csv")

rndP = RandomGenerator(Philox())
rndX = RandomGenerator()
rndT = RandomGenerator(ThreeFry())

for s in range(instance_amnt):
	print("----------------------  Iteration " + str(s) + "  ----------------------")
	
	#Generating Random Numbers with each of the different PRNGs
	bitsP = list(rndP.randint(low=0, high=2, size=bits_per_instance))
	bitsX = list(rndX.randint(low=0, high=2, size=bits_per_instance))
	bitsT = list(rndT.randint(low=0, high=2, size=bits_per_instance))
	bitsM = []
	for r in range(bits_per_instance):
	    bitsM.append(random.randrange(0,2))
    
	#Running NIST suite tests on the generated data
	#IMPORTANT: the data in the csv is not organized in blocks: Instead, 
	#if x=entryNum%4, then x = 1 is Philox, x = 2 is Xorishiro,
	#x = 3 is ThreeFry, and x=4 is Mersenne Twister
    print("--------  Philox " + str(s) +" --------")
	sp800_22_tests.test_func(bitsP, "cluster_data_combined_2.csv")
	print("--------  Xoroshiro " + str(s) +" --------")
	sp800_22_tests.test_func(bitsX, "cluster_data_combined_2.csv")
	print("--------  ThreeFry " + str(s) +" --------")
	sp800_22_tests.test_func(bitsT, "cluster_data_combined_2.csv")
	print("--------  Mersenne Twister " + str(s) +" --------")
	sp800_22_tests.test_func(bitsM, "cluster_data_combined_2.csv")
