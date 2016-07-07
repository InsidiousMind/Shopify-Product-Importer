#!/usr/bin/env python

class Product:
    'class for all the products'

    variants = []


    def __init__ (self, title, rownum):
        self.title = title
        self.rownum = rownum

    def getRownum(self):
        return rownum


    def getTitle(self):
        return title


    #Product ID
    def getPID(self):
        return title[:4]


    def addVariant(self, variant):
        variants.append(variant)
