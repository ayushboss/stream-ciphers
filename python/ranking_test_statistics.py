import numpy as np
import pandas as pd
import seaborn as sns
import os
import sys
import matplotlib.pyplot as plt

def rankPRNGS():
	testNames = ['Monobit','Frequency Within Block','Runs','Longest Runs in Ones','Binary Matrix Rank','Non-Overlapping Template','Overlapping Template','Maurers','Linear Complexity']
	pcg64 =  [0.824594284956469, 98.09783152105992, 514180.753, 6.1113646125295, 2.02563402609132, 0.0054206902843592, 4.815184600427562, 6.196340842226006, 5.856802961199646]
	xoroshiro = [0.8374000507876624, 98.50515760082004, 514197.358, 5.991404312881293, 1.9099706904627682, 0.005539286088624, 5.100019254524196, 6.196106918898001, 5.929129507630305]
	philox =  [0.7939732592139962, 98.81408375834997, 514166.232, 5.936612790489213, 2.1119970074166803, 0.005121788032790702, 4.958095272507207, 6.196348617954997, 6.095089264687799]
	threefry = [0.8038186901213252, 99.08989005488, 514188.12, 6.1748422207246, 1.9932676556447135, 0.005031441064197807, 4.962335798072149, 6.196213221188994, 5.955664629227703]
	MT = [0.8194763175620344, 98.42496505222014, 514188.819, 6.0493080706744955, 1.9766095577817013, 0.005466293463878797, 5.144822189885696, 6.196109897427002, 5.984391469364999]
	for i in range(0, len(testNames)):
		print('----------------' + str(testNames[i]) + '--------------------')
		testValues = [pcg64[i], xoroshiro[i], philox[i], threefry[i], MT[i]]
		testValues.sort()
		for val in testValues:
			if (val == pcg64[i]):
				print("PCG64")
			elif (val == xoroshiro[i]):
				print("Xoroshiro")
			elif (val == philox[i]):
				print("Philox")
			elif (val == threefry[i]):
				print("ThreeFry")
			elif (val == MT[i]):
				print("MT")
def main():
	if len(sys.argv) > 2:
		print("Error: too many arguments.")
		return
	rankPRNGS()

if __name__ == '__main__':
	main()

