import os

for file_idx in range(0, 199):
	os.rename(r"/Users/ayushboss/Desktop/Coding/stream-ciphers/xoro_add/xoroshiro/xoroshiro_iteration_" + str(file_idx) + ".zip", r"/Users/ayushboss/Desktop/Coding/stream-ciphers/xoro_add/xoroshiro/xoroshiro_iteration_" + str(file_idx+799) + ".zip")