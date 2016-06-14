#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPDigestAuth

def dump(url, user, passwd, parameters):
    response = requests.get(url, params=parameters)
    if response.status_code == 401:
        response = requests.get(url,
                auth=(user, passwd),
                params=parameters)
    if response.status_code == 401:
        response = requests.get(url,
                auth=HTTPDigestAuth(user, passwd),
                params=parameters)
    print(response.text)

if __name__ == '__main__':
    dump('http://192.168.0.102/config/twt.cgi', 'admin', 'admin', {})
