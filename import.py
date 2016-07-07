#!/usr/bin/env python

import csv
import sys
import getopt
import os
import re
import product

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))


csv_strings = ['Handle', 'Title', 'Type', 'Vendor', 'Option1 Value',
               'Attribute', 'Variant Size']

tagKey = ['Title', 'Variant Size', 'Type']

replaceStr = ['Sm', 'Med', 'Lg', 'Medium', 'SM', 'MED', 'LG', 'MED', 'MEDIUM',
              'Large', 'LARGE', ' M']


def main(argv):
    csvfile = ''
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
    parseFile(csvfile, outputfile)
    sortVariants(csvfile, outputfile)


# data[row][column]
def parseFile(cfile, ofile):
    cmd = 'touch ' + ofile
    os.system(cmd)
    csv_i = open(cfile, 'r+')
    csv_o = open(ofile, 'w')

    try:
        lines = {}
        headers = []
        reader = csv.DictReader(csv_i)
        with open('headers.txt') as f:
            headers = [x.strip('\n') for x in f.readlines()]
            headers.append('')

        w = csv.DictWriter(csv_o, headers, '', 'raise')
        w.writeheader()
        for row in reader:
            tags = ''
            title = ''
            for key, value in row.items():
                if key in csv_strings:
                    lines[key] = parseTitle(value)
                else:
                    lines[key] = value
                if key in tagKey:
                    theseTags = value.replace(" ", ", ")
                    tags += theseTags.lower()
                    tags += ', '
                if key == 'Title':
                    strList = value.split()
                    for item in strList:
                        if item in replaceStr:
                            strList.remove(item)
                    title = ' '.join(strList).title()
                    title = parseTitle(title)
            lines['Tags'] += tags
            lines['Title'] = title
            w.writerow(lines)

    finally:
        csv_i.close()
        csv_o.close()


def parseTitle(s):
    temp = ''
    temp = s.title()
    temp = re.sub(r"(?<=')[A-Z]", lambda m: m.group().lower(), temp)
    return temp


def sortVariants(cfile, ofile):
    csv_i = open(cfile, 'r')
    csv_o = open(ofile, 'w')

    # for holding product objects
    productList = []
    # for hodling the variants we already touched
    variantList = []

    try:
        reader = csv.reader(csv_i)
        writer = csv.writer(csv_o)
        count = 0
        i = 0
        for row in reader:
            if row[1][:4] not in variantList:
                variantList.append(row[1][:4])
                temp = product.Product(row[1], i)
                productList.append(temp)
                i += 1
            elif row[1][:4] in variantList:
                for item in productList:
                    if item.getPID() == row[1][:4]:
                        temp = product.Product(row[1], i)
                        item.addVariant(temp)
                i += 1
            else:
                # shouldn't happen
                pass

    finally:
        csv_i.close()
        csv_o.close()


def createVariants(reader, writer, count):
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
