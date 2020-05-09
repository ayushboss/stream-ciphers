#Originally, due to some issues, two of the monobit values were messed up 
#and simply said the total S as opposed to s/sqrt(n)

#This program fixed that issue

import numpy as np
import pandas as pd
import sys

def fix(prng_name):
    df = pd.read_csv('sp800_collected_cluster_data_' + str(prng_name) + '.csv')
    df.Monobit = df.Monobit/np.sqrt(1029000)
    df.to_csv('sp800_collected_cluster_data_' + str(prng_name) + '2.csv', index=False, sep=',')
    print("Correction complete.")

def main():
    if len(sys.argv) != 2:
        print("Incorrect Function Usage: python3 correct_monobit.py [PRNG_NAME]")
        return
    fix(sys.argv[1])

if __name__ == '__main__':
    main()

