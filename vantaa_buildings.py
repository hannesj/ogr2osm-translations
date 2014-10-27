# -*- coding: utf-8 -*-

'''
Import translations for Finnish buildings
'''
import csv
import logging

BUILDING_TAGS = []

with open('translations/vantaa.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        BUILDING_TAGS.append((row[2].decode('utf-8'), row[0].strip(), row[1].strip()))

LOG = logging.getLogger("vantaa")

#LOG.info(BUILDING_TAGS)

def filterTags(attrs):
    if not attrs:
        return
    tags = {}

    if attrs[u'vir_rakenn']:
        tags.update({'ref:building_code':attrs[u'vir_rakenn']})

    if attrs['valmistumi']:
        d,m,y = attrs['valmistumi'].split('.')
        if y != "1900" or m != "1" or d != "1": 
            if (m != "12" or d != "31") and (m != "1" or d != "1"):
                datestr = '-'.join((y,m.zfill(2),d.zfill(2)))
            else:
                datestr = y    
            tags.update({'start_date':datestr})

    if attrs[u'käyttöta_1']:
        match = False
        for tag in BUILDING_TAGS:
            if tag[0] == attrs[u'käyttöta_1']:
                tags.update({tag[1]:tag[2]})
                match = True
        if match == False:
            tags.update({'building':'yes'})
            LOG.warning("No tags found for: " + attrs[u'käyttöta_1'])

    if not 'building' in tags:
        tags.update({'building':'yes'})

    if attrs['kerrostenl'] and attrs['kerrostenl'] != "0" and attrs['kerrostenl'] != "-9999":
        tags.update({'building:levels':attrs['kerrostenl']})

    if attrs['katuosoite'] and attrs['katuosoite'] != '0 0':
        street, number = attrs['katuosoite'].rsplit(" ", 1)
        tags.update({'addr:street':street})
        tags.update({'addr:housenumber':number.upper()})

    if attrs['postitoimi'] and attrs['postitoimi'] != '0':
        tags.update({'addr:postcode':attrs['postitoimi']})
        LOG.debug(attrs['postitoimi'])

    return tags
