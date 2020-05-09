from zipfile import ZipFile
import sys
import time
import csv
sys.path.append('../python')

def redo(prng_name):
    path = "/Users/ayushboss/Desktop/Coding/stream-ciphers/raw_text/xoroshiro/xoroshiro/xoroshiro_iteration_";

    # /Users/ayushboss/Desktop/Coding/stream-ciphers/cluster_data

    for idx in range(799,1000):
        with ZipFile(str(path) + str(idx) + ".zip", 'r') as zip:
            idx2 = idx - 799
            # idx2 = 0
            zip.printdir()
            data = zip.read('raw_text/xoroshiro/xoroshiro_iteration_' + str(idx2) + '.txt')
            data = data[:-1]
            data = data.decode('utf-8')

            data_array = data.split(",")
            data_array_int = [int(numeric_string) for numeric_string in data_array]

            testname = 'maurers_universal_test'

            print("TEST: %s" % testname)
            m = __import__ ("sp800_22_maurers_universal_test")
            func = getattr(m,testname)
            
            (success,p,plist, score, testmax) = func(data_array_int)

            summary_name = testname
            summary_result = ''
            summary_p = None
            if success:
                print("  PASS")
                summary_result = "PASS"
            else:
                print("  FAIL")
                summary_result = "FAIL"
            
            if p != None:
                print("  P="+str(p))
                summary_p = str(p)
                
            if plist != None:
                for pval in plist:
                    print("P="+str(pval))
                    summary_p = str(min(plist))
            
            row = [score]
            with open("maurers_data/" + str(prng_name) + ".csv", "a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)
        
        


def main():
    redo("xoroshiro")


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Duration: " + str(end-start))
