# -*- coding: utf-8 -*-

# Description: retrieves the date (year or century) of items
# Example usage:
#   python get_dates.py ../data/src/pd_items.json ../data/dates.json ../data/item_dates.json year
#   python get_dates.py ../data/src/pd_items.json ../data/centuries.json ../data/item_centuries.json century

from collections import Counter
import json
import math
from pprint import pprint
import re
import sys
from SPARQLWrapper import SPARQLWrapper
import urllib.request

OUTPUT_FILE = "../data/src/pd_items_all.json"

page = 0
d = 10000
flg = True

arr = []

dd = []

while flg:

    print("page="+str(page+1))

    query = """                                                                                                                              
        select distinct ?s ?image ?type ?label ?t ?c_label ?c_url where {                                                                                                                                                                
            ?s schema:image ?image .
            ?s rdf:type ?type . 
            ?s rdfs:label ?label .
            optional { ?s schema:temporal ?t . } 
            ?s jps:sourceInfo ?sourceInfo .
            ?sourceInfo schema:provider ?pro;
            schema:relatedLink ?link . 
            ?pro schema:url ?c_url;
            rdfs:label ?c_label.
        } limit """+str(d)+""" offset """+str(page * d)+"""                                                                                                   
    """

    sparql = SPARQLWrapper(
        endpoint='https://jpsearch.go.jp/rdf/sparql', returnFormat='json')
    sparql.setQuery(query)


    results = sparql.query().convert()
    results = results["results"]["bindings"]

    if len(results) > 0:

        for i in range(len(results)):
            if i % 20 == 0:
                print("i="+str(i+page * d))

            obj = results[i]
            s = obj["s"]["value"]

            if s not in dd:

                obj2 = {}
                for key in obj:
                    obj2[key] = obj[key]["value"]

                arr.append(obj2)
                dd.append(s)

        # flg = False
    else:
        flg = False

    page += 1

with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(arr, outfile, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
