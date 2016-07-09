import csv
import os
import re
import product
from time import sleep

# Constants

OPTION1_NAME = 7
OPTION1_VALUE = 8
OPTION2_NAME = 9
OPTION2_VALUE = 10
OPTION3_NAME = 11
OPTION3_VALUE = 12

headers = []


def getHeaders():
    headers = []
    with open('headers.txt') as f:
        headers = [x.strip('\n') for x in f.readlines()]
        headers.append('')
    return headers



# data[row][column]
def parseFile(cfile, ofile):
    # constant stuff

    csv_strings = ['Handle', 'Title', 'Type', 'Vendor', 'Option1 Value',
                   'Attribute', 'Variant Size']

    tagKey = ['Title', 'Variant Size', 'Type']

    replaceStr = ['SM', 'MED', 'LG', 'SMALL', 'MEDIUM', 'LARGE', '-LG',
                  'small', 'medium', 'large', 'M', 'XL', 'X-Large',
                  'S/P', 'DLX', 'X', 'T', 'GREEN', 'RED', 'BLACK',
                  'BLUE', 'MD']

    csv_i = open(cfile, 'r+')
    csv_o = open(ofile, 'w')

    try:
        lines = {}
        headers = getHeaders()
        reader = csv.DictReader(csv_i)

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
                    for item in replaceStr:
                        if item in strList:
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
    temp = re.sub(r"\(([^\)]+)\)", '', temp)
    temp = re.sub(r"[\d\-)(]*\d[\d\-)(]*", '', temp)
    return temp


def sortVariants(cfile, ofile):
    # cmd = 'cp ' + ofile + ' temp.csv'
    # os.system(cmd)
    # sleep(1)
    # temp = 'temp.csv'

    # inputCSV.csv
    csv_i = open(cfile, 'r')
    # output.csv
    csv_o = open(ofile, 'w')

    # for holding product objects
    productList = []
    # for hodling the variants we already touched
    variantList = []

    try:
        reader = csv.reader(csv_i)
        writer = csv.writer(csv_o)
        i = 0
        for row in reader:
            # get the variants and put them in a list of products
            # Product.variants is list of product variants per product
            if row[1][:6] not in variantList:
                variantList.append(row[1][:6])
                temp = product.Product(row[1], i)
                productList.append(temp)
                i += 1
            elif row[1][:6] in variantList:
                for item in productList:
                    if item.getPID() == row[1][:6]:
                        temp = product.Product(row[1], i)
                        item.addVariant(temp)
                i += 1
            else:
                # shouldn't happen
                pass
            writer.writerow(row)
        variantSizes = ['SM', 'MED', 'LG', 'SMALL', 'MEDIUM', 'LARGE',
                        'XLARGE', 'X-LARGE', 'X-Large', 'small', 'medium',
                        'large', 'M', 'XL', 'MD']
        variantColors = ['GREEN', 'RED', 'BLACK', 'BLUE']
    finally:
        csv_i.close()
        csv_o.close()
    headers = getHeaders()
    for item in productList:
        if len(item.getVariants()) > 0:
            variants = item.getVariants()
            for item in variants:
                pass
        elif item.getTitle() not in headers:
            parseItem(cfile, ofile, item, variantSizes, variantColors)

    # not sure how this would work
    randFileName = 'randFileGenDoNotNameFileThisKek8327239423.csv'

    cmd = 'cp ' + ofile + ' ' + randFileName
    os.system(cmd)
    return randFileName


def editCell(cfile, ofile, vrow, col, data):
    # inputCSV.csv
    csv_i = open(cfile, 'r')
    # output.csv
    csv_o = open(ofile, 'w')
    try:
        r = csv.reader(csv_i)
        w = csv.writer(csv_o)
        i = 0
        for row in r:
            lines = row
            if i == vrow:
                lines[col] = data
            w.writerow(lines)
            i += 1
    finally:
        csv_i.close()
        csv_o.close()
    cmd = 'cp ' + ofile + ' ' + cfile
    os.system(cmd)


# reader writer
def parseItem(cfile, ofile, product, sizes, colors):
    editCell(cfile, ofile, product.getRownum(), OPTION1_NAME, 'Size')
    editCell(cfile, ofile, product.getRownum(), OPTION1_VALUE, 'TEST THIS SHIT')
    # for size in sizes:
    # if size in product.getTitle():
    #   editCell(cfile, ofile, product.getRownum(), OPTION1_NAME, 'Size')
    #   editCell(cfile, ofile, product.getRownum(), OPTION1_VALUE, size)
    # else:
    #     editCell(cfile, ofile, product.getRownum(), OPTION1_NAME, 'Size')
    #     editCell(cfile, ofile, product.getRownum(), OPTION1_VALUE, 'TESTTHISSHIT')

    for color in colors:
        if color in product.getTitle():
            editCell(cfile, ofile, product.getRownum(), OPTION2_NAME, 'Color')
            editCell(cfile, ofile, product.getRownum(), OPTION2_VALUE, color)
        else:
            pass
