import sp800_22_tests
import time

def LCG(limits=[0,1], size=1, int_param=1):
    """
    Returns: A series of pseudorandom numbers of range *limits* and size
    *size*. Default: 1 number with range between 0 and 1.
    ===========
    Description
    ===========
    Linear Congruential Generator (Basic)
    A standard technique for generating pseudorandom numbers is known as
    he linear congruential generator (LCG). This class of PRNG has:
                            *A modulus -> m
                            *A multiplier -> a
                            *An increment -> c
                            *A random seed -> Z
    Our values were chosen trough careful, scientific, face-to-keyboard
    smashing. 
    Then, given a random seed Z, we generate the first pseudorandom number.
                            X_0 = (aZ + c) mod m
    Afterwords, the remaining numbers are generated recursively such that:
                            X_n+1 = (aX_n + c) mod m
    This is good enough for most applications, but for serious cryptographic
    applications by companies and professionals, more complex random number
    generators are used. 
    """
    #Initialize: empty list, seed, modulus, multiplier, and increment.
    series = []
    seed = time.clock()
    modulus = 12387409          
    multiplier = 11234345 
    increment = 7569
    #Generate the first pseudorandom number and add it to the empty list.
    next = (seed * multiplier + increment) % modulus
    series = series + [next]
    #Then generate the remaining pseudorandom numbers with LCG. 
    for n in range(0, size-1):
        next = (series[n] * multiplier + increment) % modulus
        series = series + [next]
    #Adjust the numbers to account for the range specified.
    limit_divisor = modulus/limits[1]
    for i in range(0, len(series)):
        series[i] = series[i]/limit_divisor
    #Check the integer parameter
    if int_param:
        if size == 1:
            return int(series[0])
        intify = lambda a: int(a)
        return map(intify, series)
    else:
        if size == 1:
            return series[0]
        return series


instance_amnt = int(input("# of instances: "))
bits_per_instance = int(input("# of bits per instance: "))

sp800_22_tests.append_header("cluster_data_LCG.csv")

for s in range(instance_amnt):
	bits = LCG(size = bits_per_instance)
	sp800_22_tests.test_func(bits, "cluster_data_LCG.csv")
