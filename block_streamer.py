#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import argparse
import struct

header_struct = struct.Struct('!I') # !->network byte, I->unsigned int

def recvall(sock, length):
    data = b''
    while length > 0:
        more = sock.recv(length)
        if not more:
            break
        length -= len(more)
        data += more
    return data

def get_block(sock):
    data = recvall(sock, header_struct.size)
    if not data:
        return data
    else :
        (length,) = header_struct.unpack(data)
        return recvall(sock, length)

def put_block(sock, msg):
    length = len(msg)
    sock.send(header_struct.pack(length))
    sock.send(msg)

def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    print('Server is listening at', sock.getsockname())
    while True:
        client, addr = sock.accept()
        client.shutdown(socket.SHUT_WR)
        print('We have a client from', addr)
        msg = b''
        while True:
            more = get_block(client)
            if not more:
                print('Client close the connection')
                break
            print('Received {} bytes from {}'.format(len(more), addr))
            msg += more
        print("Message:")
        print(msg.decode('utf-8'))
        client.close()
    sock.close()

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.shutdown(socket.SHUT_RD)
    put_block(sock, '華盛頓：「友情像一棵樹木,要慢慢的栽培,才能成長真的友誼,要經過困難考驗,才可友誼永固」\n'.encode('utf-8'))
    put_block(sock, '愛因斯坦：「世間最美好的東西，莫過於有幾個頭腦和心地都很正直的嚴正的朋友。」\n'.encode('utf-8'))
    put_block(sock, '達爾文：「談到名聲、榮譽、快樂、財富這些東西，如果同友情相比，它們都是塵土。」\n'.encode('utf-8'))
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transmit & receive blocks over TCP')
    parser.add_argument('hostname', nargs='?', default='127.0.0.1',
                        help='IP address or hostname (default: %(default)s)')
    parser.add_argument('-c', action='store_true', help='run as the client')
    parser.add_argument('-p', type=int, metavar='port', default=1060,
                        help='TCP port number (default: %(default)s)')
    args = parser.parse_args()
    function = client if args.c else server
    function(args.hostname, args.p)
