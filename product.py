#!/usr/bin/env python


class Product:
    'class for all the products'

    def __init__(self, title, rownum):
        self.title = title
        self.rownum = rownum
        self.variants = []

    def getRownum(self):
        return self.rownum

    def getTitle(self):
        return self.title

    # Product ID
    def getPID(self):
        return self.title[:6]

    def getVariants(self):
        return self.variants

    def addVariant(self, variant):
        self.variants.append(variant)
