#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import socket
import random
import argparse
from datetime import datetime

def server(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((hostname, port))
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(65536)
        if random.random() < 0.5:
            print('Pretending to drop packet from {}'.format(address))
            continue
        text = data.decode('utf-8')
        print('The client at {}, say {!r}'.format(address, text))
        text = 'Your data was {} bytes long'.format(len(data))
        sock.sendto(text.encode('utf-8'), address)

def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = '[{}] Hi, how are you?'.format(datetime.now())
    data = text.encode('utf-8')
    sock.connect((hostname, port))
    print('The OS assigned me the address {}'.format(sock.getsockname()))
    delay = 0.1
    while True:
        sock.send(data)
        print('Waiting up to {} seconds for a reply'.format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(65536)
        except socket.timeout:
            delay *= 2
            if delay > 2.0:
                raise RuntimeError('I think the server is down')
        else:
            break
    text = data.decode('utf-8')
    print('The server {} replied {!r}'.format(sock.getpeername(), text))

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role',
            choices=choices,
            help='which role to play')
    parser.add_argument('host',
            help='interface the server listen at;'
            'host the client sends to')
    parser.add_argument('-p',
            metavar='PORT',
            type=int,
            default=1060)
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
