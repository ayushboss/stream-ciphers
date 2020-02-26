import os
import subprocess
def compress(csvname):
    directory = os.fsencode("bin_files")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".bin"): 
            sCompressFiles = subprocess.check_call("7z a " + filename[:4] + " " + filename, shell = True)
        continue

    iterationValue = -1

    with open("counter.txt", "r") as counterFile:
        iterationValue = counterFile.read()

    idx = 1

    while idx != iterationvalue + 1:
        normalFileSize = os.path.getsize("bin_files/bin_list_" + str(idx) + ".bin")
        compressedFileSize = os.path.getsize("bin_files/bin_list_" + str(idx) + ".7z")
        ratio = compressedFileSize/normalFileSize
        row = [ratio]
        with open(csvname, "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)
        idx+=1

