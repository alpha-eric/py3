#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

def geocode(address):
    parameters = {'address':address, 'sensor':'false'}
    url = 'http://maps.googleapis.com/maps/api/geocode/json'
    response = requests.get(url, params=parameters)
    #print(response.text)
    answer = response.json()
    print(answer['results'][0]['geometry']['location'])

if __name__ == '__main__':
    geocode('208 N. Defiance St, Archbold, OH')
    #geocode('No.8, Li-Shing Road VII Science-Based Industrial Park<br>Hsinchu, Taiwan, R.O.C.')
