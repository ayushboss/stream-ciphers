#!/usr/bin/env python

# sp800_22_tests.py
# 
# Copyright (C) 2017 David Johnston
# This program is distributed under the terms of the GNU General Public License.
# 
# This file is part of sp800_22_tests.
# 
# sp800_22_tests is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# sp800_22_tests is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with sp800_22_tests.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
from scipy.stats import entropy
import io
import numpy as np
import csv
import sys
import get_byte_entropy_bits as ByteEntropyBits
import compress_bin_files as CompressBinFiles
import zipfile

sys.path.append('python')

import argparse
import sys
import random
import math

import zipfile
import os

import time

import pandas as pd
import subprocess

# def get_compressed_ratio(a):
#     uncompressed = io.BytesIO()
#     compressed = io.BytesIO()
#     np.savez_compressed(compressed, a)
#     np.savez(uncompressed, a)

#     return uncompressed.getbuffer().nbytes/float(compressed.getbuffer().nbytes)

# def get_compressed_ratio(bits):
#     s = open("bits.txt", "w+")
#     for ints in bits:
#         s.write(str(ints) + ", ")
#     precompress_size = os.path.getsize("bits.txt")
#     bits_zip = zipfile.ZipFile("bits-compressed.zip", "w")
#     bits_zip.write('bits.txt', compress_type=zipfile.ZIP_DEFLATED)
#     bits_zip.close()
#     postcompress_size = os.path.getsize("bits-compressed.zip")
#     return precompress_size/postcompress_size

def get_binary_entropy_bits(bits):
    p0 = ( (float(bits.count(0)))/len(bits) )
    p1 = ( (float(bits.count(1)))/len(bits) )
    entropy = -1.0 * (p0*math.log(p0) + p1*math.log(p1))
    return entropy

def get_compressed_ratio(bits):
    s = open("bits.bin", "wb")
    bitsList = []
    print(len(bits)/8)
    for intIndex in range(int(float(len(bits)/8))):
        #0...7
        out = bits[8*intIndex]*(128)+bits[8*intIndex+1]*(64)+bits[8*intIndex+2]*(32)+bits[8*intIndex+3]*(16) + bits[8*intIndex+4]*(8)+bits[8*intIndex+5]*(4) + bits[8*intIndex+6]*2 + bits[8*intIndex+7]
        #print("Compression Ratio: " + str(out))
        bitsList.append(out)
    byteArrayBitsList = bytearray(bitsList)
        
    s.write(byteArrayBitsList)
    precompress_size = os.path.getsize("bits.bin")
    bits_zip = zipfile.ZipFile("bitscompressed.zip", "w")
    bits_zip.write('bits.bin', compress_type=zipfile.ZIP_DEFLATED)
    bits_zip.close()
    postcompress_size = os.path.getsize("bitscompressed.zip")

    d = open("bitsRaw.txt", "w+")
    for ints in bits:
        d.write(str(ints) + ", ")
    return precompress_size/postcompress_size

def transfer_bits(bits):
    bitsList = []
    for intIndex in range(int(float(len(bits)/8))):
        #0...7

        compressString=str(bits[8*intIndex]) + str(bits[8*intIndex+1]) + str(bits[8*intIndex+2]) + str(bits[8*intIndex+3]) + str(bits[8*intIndex+4]) + str(bits[8*intIndex+5]) + str(bits[8*intIndex+6]) + str(bits[8*intIndex+7])
        out = bits[8*intIndex]*(128)+bits[8*intIndex+1]*(64)+bits[8*intIndex+2]*(32)+bits[8*intIndex+3]*(16) + bits[8*intIndex+4]*(8)+bits[8*intIndex+5]*(4) + bits[8*intIndex+6]*2 + bits[8*intIndex+7]
        # print(str(bits[8*intIndex]) + " " + str(bits[8*intIndex+1]) + " " + str(bits[8*intIndex+2]) + " " + str(bits[8*intIndex+3]) + " " + str(bits[8*intIndex+4]) + " " + str(bits[8*intIndex+5]) + " " + str(bits[8*intIndex+6]) + " " + str(bits[8*intIndex+7]) + " " + str(out))
        #print("Compression Ratio: " + str(out))
        bitsList.append(out)
    
    s = open("bit_transfer.txt", "w+")
    for ints in bitsList:
        s.write(str(ints) + '\n')

    return bitsList

def print_to_text_file(bits, iteration, prng_name):
    d = open("raw_text/" + str(prng_name) + "_iteration_" + str(iteration) + ".txt", "w+")
    for ints in bits:
        d.write(str(ints) + ",")
    zipfile.ZipFile("raw_text/" + str(prng_name)+'_iteration_' + str(iteration) + '.zip', mode='w').write("raw_text/" + str(prng_name) + "_iteration_" + str(iteration) + ".txt")
    os.remove("raw_text/" + str(prng_name) + "_iteration_" + str(iteration) + ".txt")


def read_bits_from_file(filename,bigendian):
    bitlist = list()
    if filename == None:
        f = sys.stdin
    else:
        f = open(filename, "rb")
    while True:
        bytes = f.read(16384)
        if bytes:
            for bytech in bytes:
                if sys.version_info > (3,0):
                    byte = bytech
                else:
                    byte = ord(bytech) 
                for i in range(8):
                    if bigendian:
                        bit = (byte & 0x80) >> 7
                        byte = byte << 1
                    else:
                        bit = (byte >> i) & 1
                    bitlist.append(bit)    
        else:
            break
    f.close()
    return bitlist

import argparse
import sys
parser = argparse.ArgumentParser(description='Test data for distinguishability form random, using NIST SP800-22Rev1a algorithms.')
parser.add_argument('filename', type=str, nargs='?', help='Filename of binary file to test')
parser.add_argument('--be', action='store_false',help='Treat data as big endian bits within bytes. Defaults to little endian')
parser.add_argument('-t', '--testname', default=None,help='Select the test to run. Defaults to running all tests. Use --list_tests to see the list')
parser.add_argument('--list_tests', action='store_true',help='Display the list of tests')

args = parser.parse_args()

bigendian = args.be
filename = args.filename

# X 3.-1 Chi Squared Test
# X 3.0  KS-Test (STILL NEED TO FIX)
# X 3.1  Frequency (Monobits) Test
# X 3.2  Frequency Test within a Block
# X 3.3  Runs Test
# X 3.4  Test for the Longest Run of Ones in a Block
# X 3.5  Binary Matrix Rank Test
# X 3.6  Discrete Fourier Transform (Specral) Test
# X 3.7  Non-Overlapping Template Matching Test
# X 3.8  Overlapping Template Matching Test
# X 3.9  Maurers Universal Statistical Test
# X 3.10 Linear Complexity Test
# X 3.11 Serial Test
# X 3.12 Approximate Entropy Test
# X 3.13 Cumulative Sums Test
# X 3.14 Random Excursions Test
# X 3.15 Random Excursions Variant Test 

testlist = [
        'chi_squared_test',
        'ks_test',
        'monobit_test',
        'frequency_within_block_test',
        'runs_test',
        'longest_run_ones_in_a_block_test',
        'binary_matrix_rank_test',
        'dft_test',
        'non_overlapping_template_matching_test',
        'overlapping_template_matching_test',
        'maurers_universal_test',
        'linear_complexity_test',
        'serial_test',
        'approximate_entropy_test',
        'cumulative_sums_test',
        'random_excursion_test',
        'random_excursion_variant_test',
        ]

print("Tests of Distinguishability from Random")
if args.list_tests:
    for i,testname in zip(range(len(testlist)),testlist):
        print(str(i+1).ljust(4)+": "+testname)
    exit()

#bits = read_bits_from_file(filename,bigendian) 
f = open("feature_test_summary.txt", "w+")

x = 1

name_row = ["Binary Entropy", "Byte Entropy", "Monobit", "Frequency Within Block", "Runs",
            "Longest Runs in Ones", "Binary Matrix Rank", "DFT", 
            "Non-Overlapping Template", "Overlapping Template", "Maurer's Universal", 
            "Linear Complexity", "Compression Ratio"]

df = pd.read_csv("cluster_data/cluster_datapy.csv")

def append_header(file):
    with open("cluster_data/"+str(file), "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(name_row)


def test_func(bits, csv_name, prng_name, iteration):
    start_time = time.time()

    print_to_text_file(bits, iteration, prng_name)

    get_compressed_ratio(bits)

    additional_data = {}
    max_list = {}

    gotresult=False
    if args.testname:
        if args.testname in testlist:    
            m = __import__ ("sp800_22_"+args.testname)
            func = getattr(m,args.testname)
            print("TEST: %s" % args.testname)
            (success,p,plist,score, testmax) = func(bits)
            gotresult = True

            print("-------------- SCORE -------------------\t" + str(score))
            if success:
                print("PASS")
            else:
                print("FAIL")
     
            if p:
                print("P="+str(p))

            if plist:
                for pval in plist:
                    print("P="+str(pval))
            if score != -1 and testname != 'approximate_entropy_test':
                print(testname)
                additional_data[testname] = score
            if testmax != -1:
                max_list[testname] = testmax
        else:
            print("Test name (%s) not known" % args.ttestname)
            exit()
    else:
        results = list()
        
        for testname in testlist:
            print("TEST: %s" % testname)
            m = __import__ ("sp800_22_"+testname)
            func = getattr(m,testname)
            
            (success,p,plist, score, testmax) = func(bits)

            summary_name = testname
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
            
            if score != -1 and testname != 'approximate_entropy_test':
                additional_data[testname] = score

            if testmax != -1:
                max_list[testname] = testmax

            results.append((summary_name,summary_p, summary_result, summary_p, testmax))
            
        print()
        for result in results:
            print("REEEEZULT: " + str(result))
            (summary_name,summary_p, summary_result, summary_score, summary_max) = result
            f.write(str(summary_name) + '\t\t' + str(summary_p) + '\t\t' + str(summary_result) + '\n')
            print(summary_name.ljust(40),summary_p.ljust(18),summary_result)

        
        # Calculate the entropy value of the data
        f.write("Entropy Value\t\t" + str(get_binary_entropy_bits(bits)) + "\n")
        get_binary_entropy_bits(bits)

        # Calculate the compression ratio of the data
        s = np.asarray(bits);
        f.write(("Compression Value\t\t" + str(get_compressed_ratio(s)) + "\n"))    

        testHexTrans = transfer_bits(s)
        #run the cpp file which generates "bit_list" file for value calculation
        sCreateCompFiles = subprocess.check_call("g++ compression_ratio.cpp -o out1;./out1", shell = True)

        iterationValue = -1

        with open("counter.txt", "r") as counterFile:
            iterationValue = counterFile.read()

        row = [str(get_binary_entropy_bits(bits)), str(ByteEntropyBits.get_byte_entropy_bits_func(iterationValue))]
        for idx in additional_data:
            print('yeet:' + str(idx))
            row.append(additional_data[idx])

        max_row = [1.0, 0.1]
        for idx in max_list:
            print(str(idx) + " " + str(max_list[idx]))
            max_row.append(max_list[idx])

        #need to manipulate "csv_name" so that we can get information from different files
        with open("cluster_data/" + str(csv_name), "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)

        with open("cluster_data/max.csv", "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(max_row)

        

        end = time.time()
        print("Duration: " + str(end-start_time))



"""
    look at the different things for entropy
    cluster with entropy and the compression_ratio
    consider the quantification

    2problems
        1) can we find a suboptimal subset of large list of tests
        2) How can we quantify the quality of PRNGs
            perhaps quality of clustering (density and how far apart)

    Study how do we quantify the quality of feature space partitioning 
        in our case the fs is a 2D one with compression ratio and entropy 
        Within - how dense are the clusters
        Between - what is the distance between cluster centers

        both of the above are matricies
        quality would be a function of within and between

        Within and between dispersion matricies
"""

