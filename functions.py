import csv
import os
import re

import product
from time import sleep

# /\/\/\/\/\/\/\/\/\\\/\/\/\/\/\/\/\\//\/\/\/\/\/\/\/\/\/\/\/\\/\/\\//\/\/\/\/\/\
# GLOBALS
# /\/\/\/\/\/\/\/\/\\\/\/\/\/\/\/\/\\//\/\/\/\/\/\/\/\/\/\/\/\\/\/\\//\/\/\/\/\/\

# Headers as dictionary
# makes a dictionary of shopify original shopify headers
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
headers = []
with open('oHeaders.txt') as f:
    headers = [x.strip('\n') for x in f.readlines()]
    headers.append('')

# array to hold csv file while it's being heavily modified
array = list(list())

# /\/\/\/\/\/\/\/\/\\\/\/\/\/\/\/\/\\//\/\/\/\/\/\/\/\/\/\/\/\\/\/\\//\/\/\/\/\/\
# GLOBALS
# /\/\/\/\/\/\/\/\/\\\/\/\/\/\/\/\/\\//\/\/\/\/\/\/\/\/\/\/\/\\/\/\\//\/\/\/\/\/\

# /\/\/\/\/\/\/\/\/\\\/\/\/\/\/\/\/\\//\/\/\/\/\/\/\/\/\/\/\/\\/\/\\//\/\/\/\/\/\
# CSV Editing Methods
# /\/\/\/\/\/\/\/\/\\\/\/\/\/\/\/\/\\//\/\/\/\/\/\/\/\/\/\/\/\\/\/\\//\/\/\/\/\/\
def make2dArray(cfile):
    csv_i = open(cfile, 'r')

    try:
        r = csv.reader(csv_i)

        data = list(r)
    finally:
        csv_i.close()

    return data

def editCell(vrow, col, data):
    global array
    array[vrow][col] = data

def writeCells(ofile):
    global array
    csv_o = open(ofile, 'w')
    try:
        w = csv.writer(csv_o)
        w.writerows(array)
    finally:
        csv_o.close()

# /\/\/\/\/\/\/\/\/\\\/\/\/\/\/\/\/\\//\/\/\/\/\/\/\/\/\/\/\/\\/\/\\//\/\/\/\/\/\
# CSV Editing Methods
# /\/\/\/\/\/\/\/\/\\\/\/\/\/\/\/\/\\//\/\/\/\/\/\/\/\/\/\/\/\\/\/\\//\/\/\/\/\/\


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


def modifyHeaders(cfile, ofile):
    global headers
    global array
    array = make2dArray(cfile)
    print


#regex to remove unwanted things from the title
def parseTitle(s):
    temp = ''
    temp = s.title()
    temp = re.sub(r"(?<=')[A-Z]", lambda m: m.group().lower(), temp)
    # look for anything in parenthesis
    temp = re.sub(r"\(([^\)]+)\)", '', temp)
    temp = re.sub(r"[\d\-)(]*\d[\d\-)(]*", '', temp)
    return temp


# data[row][column]
def parseFile(cfile, ofile):
    global headers
    # strings for .title()
    csv_strings = ['Title', 'Type', 'Vendor', 'Option1 Value',
                   'Attribute', 'Variant Size']

    #keys to be used for tags
    tagKey = ['Title', 'Variant Size', 'Type']

    csv_i = open(cfile, 'r+')
    csv_o = open(ofile, 'w')

    try:
        lines = {}

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

            # if first 6 characters of title not in variant list, make new variant
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
    global headers
    global array
    array = make2dArray(cfile)
    for item in productList:
        # if item has variants, parse it
        if len(item.getVariants()) > 0:
            parseItem(cfile, ofile, item, isVariant=False)
            variants = item.getVariants()
            for item in variants:
                parseItem(cfile, ofile, item, isVariant=True)
            # just to avoid header row
        elif item.getTitle() not in headers:
            parseItem(cfile, ofile, item, isVariant=False)
        else:
            pass
    writeCells(ofile)

    randFileName = 'randFileGenDoNotNameFileThisKek8327239423.csv'

    cmd = 'cp ' + ofile + ' ' + randFileName
    os.system(cmd)
    return randFileName


def parseItem(product, isVariant):

    if isVariant:
        addHandle(product)
        editSize(product)
        editColor(product)
        editVariant(product)
    else:
        addHandle(product)
        editSize(product)
        editColor(product)


def addHandle(product):
    title = parseTitleStr(product.getTitle())
    title = title.lower()
    title = title.replace(' ', '-')

    editCell(product.getRownum(), 0, title)

def editSize(product):
    global headersDict
    sizes = ['SM', 'MED', 'LG', 'SMALL', 'MEDIUM', 'LARGE',
             'XLARGE', 'X-LARGE', 'X-Large', 'small', 'medium',
             'large', 'M', 'XL', 'MD', 'TEEN', 'CHILD']

    m = re.search(r"\(([^\)]+)\)", product.getTitle())
    if m:
        editCell(product.getRownum(), headersDict['Option1 Name'], 'Size')
        editCell(product.getRownum(), headersDict['Option1 Value'], m.group(1))
    else:
        for size in sizes:
            if size in product.getTitle():
                editCell(product.getRownum(), headersDict['Option1 Name'], 'Size')
                editCell(product.getRownum(), headersDict['Option1 Value'], size)
                break


def editVariant(product):
    global headersDict

    editCell(product.getRownum(), headersDict['Title'], '')
    editCell(product.getRownum(), headersDict['Vendor'], '')
    editCell(product.getRownum(), headersDict['Type'], '')
    editCell(product.getRownum(), headersDict['Tags'], '')
    editCell(product.getRownum(), headersDict['Option1 Name'], '')
    editCell(product.getRownum(), headersDict['Option2 Name'], '')
    editCell(product.getRownum(), headersDict['Option3 Name'], '')


def editColor(product):

    colors = ['GREEN', 'RED', 'BLACK', 'BLUE']

    for color in colors:
        if color in product.getTitle():
            editCell(product.getRownum(), headersDict['Option2 Name'], 'Color')
            editCell(product.getRownum(), headersDict['Option2 Value'], color)
            break

