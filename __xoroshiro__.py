import sp800_22_tests
from randomgen import RandomGenerator
instance_amnt = int(input("# of instances: "))
bits_per_instance = int(input("# of bits per instance: "))

rnd = RandomGenerator();

for s in range(instance_amnt):
	bits = list(rnd.randint(low=0, high=2, size=bits_per_instance))
	sp800_22_tests.test_func(bits)
