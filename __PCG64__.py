import sp800_22_tests
from randomgen import PCG64

instance_amnt = int(input("# of instances: "))
bits_per_instance = int(input("# of bits per instance: "))

sp800_22_tests.append_header("cluster_data_PCG64.csv")

for s in range(instance_amnt):
    print("----------------------  Iteration " + str(s) + "  ----------------------")
    bits = []
    for i in range(bits_per_instance):
        bits[i] = PCG64(i)

    sp800_22_tests.test_func(bits, "cluster_data_PCG64.csv")
