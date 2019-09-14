import sp800_22_tests
import random

instance_amnt = int(input("# of instances: "))
bits_per_instance = int(input("# of bits per instance: "))

bits = []
for r in range(bits_per_instance):
    # if len(bits) >= bits_per_instance:
    #     break
    # bitstring = '{0:08b}'.format(random.randrange(0,2))
    # for i in range(0, len(bitstring)):
    #     bits.append(ord(bitstring[i])-ord('0'))
    bits.append(random.randrange(0,2))


sp800_22_tests.test_func(bits)
