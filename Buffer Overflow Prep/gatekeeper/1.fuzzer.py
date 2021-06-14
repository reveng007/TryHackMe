#!/usr/bin/env python3

import socket
import sys
ip = "10.0.2.45"
port = 31337
string = b"\x41" * 10
s = socket.socket()
s.connect((ip, port))
timeout = 5 
s.settimeout(timeout)
while True:
        try:
            print("Fuzzing with {} bytes".format(len(string)))
            s.send(string + b"\x0a\x0d")
            string += b"\x41" * 10
            s.recv(1024)

        except:
            print("Fuzzer crashed at {} bytes".format(len(string)))
            sys.exit(0)

s.close()