from zipfile import ZipFile
import sys

sys.path.append('..')
sys.path.append('../python')

import sp800_22_tests

pathZ = "/Users/ayushboss/Desktop/Coding/stream-ciphers/files/threefry/threefry_iteration_"

for idx in range(0, 1000):
    with ZipFile(str(pathZ) + str(idx) + ".zip", 'r') as zip:
        archiveList = zip.namelist()
        archivePath = archiveList[0]
    
        data = zip.read(archivePath)
        data = data[:-1]
        data = data.decode('utf-8')

        data_array = data.split(",")
        data_array_int = [int(numeric_string) for numeric_string in data_array]
        sp800_22_tests.test_func(data_array_int, "sp800_collected_cluster_data_threefry_fix.csv", 'threefry', idx, True)
