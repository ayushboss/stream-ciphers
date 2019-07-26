import mersenne_twister


def gen_mersenne_nums()
	generator = mersenne_twister.mersenne_rng(seed = 653)
	gen_nums = []
	for i in range(1029000):
		random_number = generator.get_random_number()
		gen_nums.append(random_number%2)

	return gen_nums