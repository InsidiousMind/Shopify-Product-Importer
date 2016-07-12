import csv
import os
import re

import itertools

import product
from time import sleep

# Headers as dictionary
# makes a dictionary of shopify headers
# glob var
headersDict = {}
with open('oHeaders.txt') as f:
    headers = [x.strip('\n') for x in f.readlines()]
    d = dict()
    i = 0
    for item in headers:
        d.update({item:i})
        i += 1
    headersDict = d

# Headers as List
# get shopify headers as a list
def getHeaders():
    headers = []
    with open('oHeaders.txt') as f:
        headers = [x.strip('\n') for x in f.readlines()]
        headers.append('')
    return headers
# need to consolidate parseTitleStr and parseTitle -> the goal for both methods is the same
def parseTitleStr(s):
    replaceStr = ['SM', 'MED', 'LG', 'SMALL', 'MEDIUM', 'LARGE', '-LG',
              'small', 'medium', 'large', 'M', 'XL', 'X-Large',
              'S/P', 'DLX', 'X', 'T', 'GREEN', 'RED', 'BLACK',
              'BLUE', 'MD']

    strList = s.split()
    for item in replaceStr:
        if item in strList:
            strList.remove(item)
    title = ' '.join(strList).title()
    return parseTitle(title)

# data[row][column]
def parseFile(cfile, ofile):
    # constant stuff
    # strings for .title()
    csv_strings = ['Title', 'Type', 'Vendor', 'Option1 Value',
                   'Attribute', 'Variant Size']

    tagKey = ['Title', 'Variant Size', 'Type']

    csv_i = open(cfile, 'r+')
    csv_o = open(ofile, 'w')

    try:
        lines = {}
        headers = getHeaders()
        reader = csv.DictReader(csv_i)

        w = csv.DictWriter(csv_o, headers, '', 'ignore')
        w.writeheader()
        for row in reader:
            tags = ''
            title = ''
            oTitle = ''
            # a hack just to get rid of tags for variants. fix this
            if(row['Title'] == ''):
                oTitle = ''
            else:
                oTitle = 'Thing'
            # capitalize, create tags and title. these methods are mostly A.OK
            for key, value in row.items():
                if key in csv_strings:
                    lines[key] = parseTitle(value)
                else:
                    lines[key] = value
                if key == 'Title':
                    title = parseTitleStr(value)
                if key in tagKey and oTitle != '':
                    theseTags = value.replace(" ", ", ")
                    tags += theseTags.lower()
                    tags += ', '
            lines['Tags'] += tags
            lines['Title'] = title
            w.writerow(lines)

    finally:
        csv_i.close()
        csv_o.close()

# use regex to remove unwanted things from title
def parseTitle(s):
    temp = ''
    temp = s.title()
    temp = re.sub(r"(?<=')[A-Z]", lambda m: m.group().lower(), temp)
    # look for anything in parenthesis
    temp = re.sub(r"\(([^\)]+)\)", '', temp)
    temp = re.sub(r"[\d\-)(]*\d[\d\-)(]*", '', temp)
    return temp

# puts variants in a list. does this by first 6 characters of the title.
# if the first 6 chars is the same as another title it's classified as a variant
def sortVariants(cfile, ofile):

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

    finally:
        csv_i.close()
        csv_o.close()
# makes variants
    headers = getHeaders()
    for item in productList:
        if len(item.getVariants()) > 0:
            parseItem(cfile, ofile, item, isVariant=False)
            variants = item.getVariants()
            for item in variants:
                parseItem(cfile, ofile, item, isVariant=True)
        elif item.getTitle() not in headers:
            parseItem(cfile, ofile, item, isVariant=False)
        else:
            pass

    randFileName = 'randFileGenDoNotNameFileThisKek8327239423.csv'

    cmd = 'cp ' + ofile + ' ' + randFileName
    os.system(cmd)
    return randFileName
# methods below are horribly un optimized and need to be fixed
# one option is putting the entire CSV into a 2D list and editing values based upon that
# http://stackoverflow.com/questions/24606650/reading-csv-file-and-inserting-it-into-2d-list-in-python
def editCell(cfile, ofile, vrow, col, data):
    # inputCSV.csv
    csv_i = open(cfile, 'r')
    # output.csv
    csv_o = open(ofile, 'w')
    try:
        r = csv.reader(csv_i)
        w = csv.writer(csv_o)

        lines = [l for l in r]
        lines[vrow][col] = data
        w.writerows(lines)

    finally:
        csv_i.close()
        csv_o.close()
    cmd = 'cp ' + ofile + ' ' + cfile
    os.system(cmd)


# reader writer
def parseItem(cfile, ofile, product, isVariant):

    if isVariant:
        addHandle(cfile, ofile, product)
        editSize(cfile, ofile, product)
        editColor(cfile, ofile, product)
        editVariant(cfile, ofile, product)
    else:
        addHandle(cfile, ofile, product)
        editSize(cfile, ofile, product)
        editColor(cfile, ofile, product)


def addHandle(cfile, ofile, product):
    title = parseTitleStr(product.getTitle())
    title = title.lower()
    title = title.replace(' ', '-')

    editCell(cfile, ofile, product.getRownum(), 0, title)

def editSize(cfile, ofile, product):

    sizes = ['SM', 'MED', 'LG', 'SMALL', 'MEDIUM', 'LARGE',
             'XLARGE', 'X-LARGE', 'X-Large', 'small', 'medium',
             'large', 'M', 'XL', 'MD', 'TEEN', 'CHILD']

    m = re.search(r"\(([^\)]+)\)", product.getTitle())
    if m:
        editCell(cfile, ofile, product.getRownum(), headersDict['Option1 Name'], 'Size')
        editCell(cfile, ofile, product.getRownum(), headersDict['Option1 Value'], m.group(1))
    else:
        for size in sizes:
            if size in product.getTitle():
                editCell(cfile, ofile, product.getRownum(), headersDict['Option1 Name'], 'Size')
                editCell(cfile, ofile, product.getRownum(), headersDict['Option1 Value'], size)
                break


def editVariant(cfile, ofile, product):

    editCell(cfile, ofile, product.getRownum(), headersDict['Title'], '')
    editCell(cfile, ofile, product.getRownum(), headersDict['Vendor'], '')
    editCell(cfile, ofile, product.getRownum(), headersDict['Type'], '')
    editCell(cfile, ofile, product.getRownum(), headersDict['Tags'], '')
    editCell(cfile, ofile, product.getRownum(), headersDict['Option1 Name'], '')
    editCell(cfile, ofile, product.getRownum(), headersDict['Option2 Name'], '')
    editCell(cfile, ofile, product.getRownum(), headersDict['Option3 Name'], '')


def editColor(cfile, ofile, product):

    colors = ['GREEN', 'RED', 'BLACK', 'BLUE']

    for color in colors:
        if color in product.getTitle():
            editCell(cfile, ofile, product.getRownum(), headersDict['Option2 Name'], 'Color')
            editCell(cfile, ofile, product.getRownum(), headersDict['Option2 Value'], color)
            break

