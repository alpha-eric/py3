#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import argparse

def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    print('Server is listening to', host, 'at port', port)
    while True:
        client, addr = sock.accept()
        client.shutdown(socket.SHUT_WR)
        print('We have a client from', client.getsockname())
        msg = b''
        while True:
            more = client.recv(4096)
            if not more:
                print('Client close connection')
                break
            print('Recvived {} bytes'.format(len(more)))
            msg += more
        print('Message from client:')
        print(msg.decode('ascii'))
        client.close()
    sock.close()

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.shutdown(socket.SHUT_RD)
    sock.sendall(b'Beautiful is better than ugly.\n')
    sock.sendall(b'Explicit is better than implicit.\n')
    sock.sendall(b'Simple is better than complex.\n')
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transmit & receive a data stream')
    parser.add_argument('hostname', nargs='?', default='127.0.0.1',
                        help='IP address or hostname (default: %(default)s)')
    parser.add_argument('-p', type=int, default=1060,
                        help='TCP port number (default: %(default)s)')
    parser.add_argument('-c', action='store_true',
                        help='run as the client')
    args = parser.parse_args()
    function = client if args.c else server
    function(args.hostname, args.p)
