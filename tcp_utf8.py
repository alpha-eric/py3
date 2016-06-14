#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import socket
import errno

def recvall(sock):
    data = ''
    while True:
        try:
            more = sock.recv(1024)
        except socket.timeout as e:
            break
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                continue
            else:
                break
        else:
            if not more:
                break
        data += more.decode('utf-8')
    return data

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        client, sockname = sock.accept()
        client.settimeout(1)
        print('We have accepted a connection from {}'.format(sockname))
        print('  Socket name: {}'.format(client.getsockname()))
        print('  Socket peer: {}'.format(client.getpeername()))
        message = recvall(client)
        print('  Incoming message: {}'.format(repr(message)))
        client.sendall('你好，使用者'.encode('utf-8'))
        client.close()
        print('  Reply sent, socket closed')

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name {}'.format(sock.getsockname()))
    sock.sendall('你好，伺服器'.encode('utf-8'))
    reply = recvall(sock)
    print('The server said {}'.format(repr(reply)))
    sock.close()

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listen at; '
            'host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
            help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)

