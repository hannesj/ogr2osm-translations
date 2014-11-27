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

materials = {
    "Betoni":"concrete",
    "Kivi":"stone",
    "Lasi":"glass",
    "Metallilevy":"metal",
    "Puu":"wood",
    "Tiili":"brick"}

LOG = logging.getLogger("vantaa")

#LOG.info(BUILDING_TAGS)

def filterTags(attrs):
    if not attrs:
        return
    tags = {}

    if attrs['vir_rakennustunnus']:
        tags.update({'building:fi:id':attrs['vir_rakennustunnus']})

    if attrs['valmistumispvm']:
        d,m,y = attrs['valmistumispvm'].split('.')
        if y != "1900": 
            if (m != "12" or d != "31") and (m != "1" or d != "1"):
                datestr = '-'.join((y,m.zfill(2),d.zfill(2)))
            else:
                datestr = y    
            tags.update({'start_date':datestr})

    if attrs[u'käyttötarkoitus']:
        match = False
        for tag in BUILDING_TAGS:
            if tag[0] == attrs[u'käyttötarkoitus']:
                tags.update({tag[1]:tag[2]})
                match = True
        if match == False:
            tags.update({'building':'yes'})
            LOG.warning("No tags found for: " + attrs[u'käyttötarkoitus'])

    if not 'building' in tags:
        tags.update({'building':'yes'})

    if attrs['julkisivumateriaali'] and attrs['julkisivumateriaali'] in materials:
        tags.update({'building:material':materials[attrs['julkisivumateriaali']]})

    if attrs['kerrostenlkm'] and attrs['kerrostenlkm'] != "0" and attrs['kerrostenlkm'] != "-9999":
        tags.update({'building:levels':attrs['kerrostenlkm']})

    if attrs['asuntoja'] and attrs['asuntoja'] != "-9999" and attrs['asuntoja'] != "0":
        tags.update({'flats':attrs['asuntoja']})

    if attrs['katuosoite_suomeksi'] and attrs['katuosoite_suomeksi'] != '0 0':
        street, number = attrs['katuosoite_suomeksi'].rsplit(" ", 1)
        if street not in ('0', 'Ei osoitetta'):
            tags.update({'addr:street':street})
        if number != '0' and number != '900':
            tags.update({'addr:housenumber':number})

    if attrs['postitoimipaikka'] and attrs['postitoimipaikka'] != '0':
        tags.update({'addr:postcode':attrs['postitoimipaikka']})

    return tags
