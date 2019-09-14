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
sys.path.append('python')

import argparse
import sys
import random

import zipfile
import os

import time

# def get_compressed_ratio(a):
#     uncompressed = io.BytesIO()
#     compressed = io.BytesIO()
#     np.savez_compressed(compressed, a)
#     np.savez(uncompressed, a)

#     return uncompressed.getbuffer().nbytes/float(compressed.getbuffer().nbytes)

def get_compressed_ratio(bits):
    s = open("bits.txt", "w+")
    for ints in bits:
        s.write(str(ints) + ", ")
    precompress_size = os.path.getsize("bits.txt")
    bits_zip = zipfile.ZipFile("bits-compressed.zip", "w")
    bits_zip.write('bits.txt', compress_type=zipfile.ZIP_DEFLATED)
    bits_zip.close()
    postcompress_size = os.path.getsize("bits-compressed.zip")
    return precompress_size/postcompress_size

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

filename = "cluster_datapy.csv"
bnb = open(filename, "w+")
bnb.close()

name_row = ["Entropy", "Compression Ratio", "Monobit", "Frequency Within Block", "Runs",
            "Longest Runs in Ones", "Binary Matrix Rank", "DFT", 
            "Non-Overlapping Template", "Overlapping Template", "Maurer's Universal", 
            "Linear Complexity"]

with open("cluster_datapy.csv", "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(name_row)

def test_func(bits):
    start_time = time.time()

    get_compressed_ratio(bits)

    #for r in bits:
    #    print(r)

    additional_data = {}

    gotresult=False
    if args.testname:
        if args.testname in testlist:    
            m = __import__ ("sp800_22_"+args.testname)
            func = getattr(m,args.testname)
            print("TEST: %s" % args.testname)
            (success,p,plist,score) = func(bits)
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
        else:
            print("Test name (%s) not known" % args.ttestname)
            exit()
    else:
        results = list()
        
        for testname in testlist:
            print("TEST: %s" % testname)
            m = __import__ ("sp800_22_"+testname)
            func = getattr(m,testname)
            
            (success,p,plist, score) = func(bits)

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

            results.append((summary_name,summary_p, summary_result))
            
        print()
        for result in results:
            (summary_name,summary_p, summary_result) = result
            f.write(str(summary_name) + '\t\t' + str(summary_p) + '\t\t' + str(summary_result) + '\n')
            print(summary_name.ljust(40),summary_p.ljust(18),summary_result)

        
        # Calculate the entropy value of the data
        f.write("Entropy Value\t\t" + str(entropy(bits)) + "\n")

        # Calculate the compression ratio of the data
        s = np.asarray(bits);
        f.write(("Compression Value\t\t" + str(get_compressed_ratio(s)) + "\n"))    
        row = [str(entropy(bits)), str(get_compressed_ratio(s))]
        for idx in additional_data:
            print('yeet:' + str(idx))
            row.append(additional_data[idx])
        with open("cluster_datapy.csv", "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)
        end = time.time()
        print("Duration: " + str(end-start_time))

    f.close()
    csvfile.close()

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

