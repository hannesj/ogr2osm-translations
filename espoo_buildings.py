# -*- coding: utf-8 -*-

'''
Import translations for Finnish buildings
'''
import unicodecsv as csv
import logging

BUILDING_TAGS = []

with open('translations/finland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        BUILDING_TAGS.append((int(row[0]), row[3].strip(), row[4].strip()))

LOG = logging.getLogger("espoo")

#LOG.info(BUILDING_TAGS)

def filterTags(attrs):
    if not attrs:
        return
    tags = {}

    if attrs['teksti']:
        tags.update({'building:fi:id':attrs['teksti']})

    if attrs['valmistumispaivamaara']:
        y = attrs['valmistumispaivamaara'][:4]
        m = attrs['valmistumispaivamaara'][4:6]
        d = attrs['valmistumispaivamaara'][6:8]
        if y != "1900" or m != "01" or d != "01":
            if m != "12" or d != "31":
                datestr = '-'.join((y,m.zfill(2),d.zfill(2)))
            else:
                datestr = y    
            tags.update({'start_date':datestr})

    if attrs[u'kayttotarkoitusnumero']:
        match = False
        for tag in BUILDING_TAGS:
            if tag[0] == int(attrs[u'kayttotarkoitusnumero']):
                tags.update({tag[1]:tag[2]})
                match = True
        if match == False:
            tags.update({'building':'yes'})
            LOG.warning("No tags found for: " + attrs[u'kayttotarkoitus'])

    if not 'building' in tags:
        tags.update({'building':'yes'})

    if attrs['kerrosluku'] and attrs['kerrosluku'] != "0":
        tags.update({'building:levels':attrs['kerrosluku']})

    if attrs['katunimi']:
        tags.update({'addr:street':attrs['katunimi']})

    numero = ""

    if attrs['osoitenumero'] and attrs['osoitenumero'] != "0":
        numero += attrs['osoitenumero']

    if attrs['osoitenumero2']:
        numero += "-" + attrs['osoitenumero2']

    if attrs['osoitekirjain']:
        numero += attrs['osoitekirjain']

    if numero != "":
        tags.update({'addr:housenumber':numero})

    return tags
