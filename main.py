#!/usr/bin/env python

import getopt
import sys
import os
import functions
from random import randint
csvfile = ''
outputfile = ''
randFilesList = []

def main(argv):
    global csvfile
    csvfile = ''
    global outputfile
    outputfile = ''

    if len(argv) < 1:
        print('must use at least "./import.py -h"')
        exit(0)
    try:
        opts, args = getopt.getopt(argv, "hc:o:", ["cfile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -c <csvfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('import.py -c <csvfile> -o <outputfile>')
            exit(0)
        elif opt in ("-c", "--cfile"):
            csvfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print("CSV file is:", csvfile)
    print("Output file is: ", outputfile)
    if outputfile == '':
        outputfile = 'a.csv'
    cmd = 'touch ' + outputfile
    os.system(cmd)

    new_cfile = newCFile()
    functions.writeNewHeaders(new_cfile, outputfile)
    new_i = cFileFromOutput()
    functions.sortVariants(new_i, outputfile)
    # CHANGE THIS TO NEW_F ONCE SORTVARIANTS FINISHED
    functions.parseFile(new_i, outputfile)
    new_i = cFileFromOutput()
    functions.parseVariants(new_i, outputfile)

    deleteFiles()


def newCFile():
    global csvfile
    global outputfile
    rand_num = randint(100000,9999999)
    new_cfile = 'randFileGen' + str(rand_num) + '.csv'
    cmd = 'cp ' + csvfile + ' ' + new_cfile
    os.system(cmd)

    randFilesList.append(new_cfile)
    return new_cfile

def cFileFromOutput():

    global csvfile
    global outputfile
    rand_num = randint(100000,9999999)
    new_cfile = 'randFileGen' + str(rand_num) + '.csv'
    cmd = 'cp ' + outputfile + ' ' + new_cfile
    os.system(cmd)

    randFilesList.append(new_cfile)
    return new_cfile

def deleteFiles():

    for item in randFilesList:
        cmd = 'rm ' + item
        os.system(cmd)

if __name__ == "__main__":
    main(sys.argv[1:])
