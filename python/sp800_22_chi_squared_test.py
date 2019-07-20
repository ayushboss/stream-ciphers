from __future__ import print_function
from scipy.stats import chisquare

import math
import copy
import gf2matrix

def chi_squared_test(bits):

	observed = [0,0]
	for r in bits:
		if r == 0:
			observed[0] = observed[0] + 1
		elif r == 1:
			observed[1] = observed[1] + 1
	cs = chisquare(observed, [math.floor(len(bits)/2), len(bits) - math.floor(len(bits)/2)])
	p = cs[1]
	return (p >= 0.1, p, None, -1)

	# observed frequencies
	# {0, 1, 2, ..., n}
	# {0, 1, 0, } 