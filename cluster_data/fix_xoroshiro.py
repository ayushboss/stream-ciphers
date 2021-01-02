from zipfile import ZipFile
import sys

sys.path.append('..')
sys.path.append('../python')

import sp800_22_tests

pathZ = "/Volumes/NO NAME/Tamir Research/raw_zip_files/MT/MT_iteration_"

for idx in range(948, 1000):
    print("Iteration " + str(idx))
    with ZipFile(str(pathZ) + str(idx) + ".zip", 'r') as zip:
        archiveList = zip.namelist()
        archivePath = archiveList[0]
    
        data = zip.read(archivePath)
        data = data[:-1]
        data = data.decode('utf-8')

        data_array = data.split(",")
        data_array_int = [int(numeric_string) for numeric_string in data_array]
        sp800_22_tests.test_func(data_array_int, "sp800_collected_cluster_data_xoroshiro_fix.csv", 'xoroshiro', idx, True)
