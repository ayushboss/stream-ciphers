import os
import subprocess
import csv

def compress(csvname):
    directory = os.fsencode("bin_files")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".bin"): 
            # print("test: " + filename[:-4] + ".7z & " + filename)
            sCompressFiles = subprocess.check_call("cd bin_files; 7z a " + filename[:-4] + ".7z " + filename + "; cd ..", shell = True)
        continue

    iterationValue = -1

    with open("counter.txt", "r") as counterFile:
        iterationValue = counterFile.read()

    idx = 1

    print("Iteration Value: " + iterationValue)

    cwd = os.open("bin_files", os.O_RDONLY)  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory
    print("Files in %r: %s" % (cwd, files))

    while idx != int(iterationValue) + 1:
        # normalFileSize = os.path.getsize(os.path.join("bin_files/", "bin_list_" + iterationValue + ".bin"))
        # file_path = os.path.join("bin_files", "bin_list_" + str(idx) + ".bin")
        file_path=open("/Users/ayushboss/Desktop/Coding/Python/hsmc-stream-cipher-2019-git/11-3-19-2:03/stream-ciphers/bin_files/bit_list_" + str(idx) + ".bin")

        compressed_path = os.path.join("bin_files", "bin_list_" + str(idx) + ".7z")
        compressed_path = compressed_path.strip()

        
        compressed_file_path = open("/Users/ayushboss/Desktop/Coding/Python/hsmc-stream-cipher-2019-git/11-3-19-2:03/stream-ciphers/bin_files/bit_list_" + str(idx) + ".7z")

        file_path.seek(0, os.SEEK_END)
        compressed_file_path.seek(0, os.SEEK_END)

        normalFileSize = file_path.tell()
        compressedFileSize = compressed_file_path.tell()
        print ("Normal, Compressed: " + str(normalFileSize) + " " + str(compressedFileSize))
        ratio = compressedFileSize/normalFileSize
        row = [ratio]
        with open(csvname, "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)
        idx+=1

