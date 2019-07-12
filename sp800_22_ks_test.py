import numpy as np
import scipy.stats as stats
from scipy.stats import norm, kstest

def ks_test(bits):
	loc, scale = norm.fit(bits)
	n = norm(loc=loc, scale=scale)

	s = stats.kstest(bits, n.cdf)
	print("S YEETTTT: " + str(s[0]) + ", " + str(s[1]))
	p=s[1]
	return (p >= 0.1, p, None)