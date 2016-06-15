#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import argparse

def connect_to(host_or_ip, port):
    try:
        #getaddrinfo(addr, port, family, type, proto)
        infolist = socket.getaddrinfo(host_or_ip, port,
                0, socket.SOCK_STREAM, 0,
                socket.AI_ADDRCONFIG | socket.AI_V4MAPPED | socket.AI_CANONNAME)
    except socket.gaierror as e:
        print('Name service failure:', repr(e))
        return

    info = infolist[0]
    socket_args = info[0:3]
    address = info[4]
    s = socket.socket(*socket_args)
    try:
        s.connect(address)
    except socket.error as e:
        print('Network failure:', repr(e))
    else:
        print('Success: host', info[3], 'is listening on port ', port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Try connecting to host')
    parser.add_argument('hostname',
            help='hostname that you want to contact')
    parser.add_argument('-p',
            help='port that you want to contact(default 80)',
            type=int,
            default=80)
    args = parser.parse_args()
    connect_to(args.hostname, args.p)
