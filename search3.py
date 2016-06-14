#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http
import json
from urllib.parse import quote_plus

uri = '/maps/api/geocode/json'

def geocode(address):
    path = '{}?address={}&sensor=false'.format(uri, address)
    connection = http.client.HTTPConnection('maps.google.com')
    connection.request('GET', path)
    rawreply = connection.getresponse().read()
    reply = json.loads(rawreply.decode('utf-8'))
    print(reply['results'][0]['geometry']['location'])

if __name__ == '__main__':
    geocode('207 N. Defiance St, Archbold, OH')
