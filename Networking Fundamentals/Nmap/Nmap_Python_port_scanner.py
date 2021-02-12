#!/usr/bin/python3

import nmap
import time
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
WHITE = '\033[97m'
ENDC = '\033[0m'

s_port = int(input("Enter Starting port: "))
e_port = int(input("Enter Ending port: "))

enquire = input("What do you want to scan? --> [ip/host]: ")

if(enquire == 'ip'):
    trgt_ip = input("Enter target: ")

if(enquire == 'host'):
    host = input("Enter hostname: ")
    trgt_ip = socket.gethostbyname(host)
    
print("Target ip: ", trgt_ip)

# input validation -> IP excludes only space from string
trgt_ip = trgt_ip.strip()

scanner = nmap.PortScanner()

#For loop for iteration

print("_"*30)

startTime = time.time()

for i in range(s_port, e_port+1):

    res = scanner.scan(trgt_ip, str(i))

    res = res['scan'][trgt_ip]['tcp'][i]['state']

    # to show the results, we are acessing only 2 values, port
    # and state of port

    if(res == 'closed'):
        print('| Port:',i,' | '+WHITE+f'State:'+ENDC, RED+f'{res}'+ENDC)
        continue

    if(res == 'filtered'):
        print('| Port:',i,' | '+WHITE+f'State:'+ENDC, YEL+f'{res}'+ENDC)
        continue
    
    res = res.upper()
    print('| Port:',i,' | '+WHITE+f'State:'+ENDC, GREEN+f'{res}'+ENDC)

totalTime = time.time() - startTime
totalTime ='%.3f'%totalTime
print(PURPLE+f"\n[+] Scan Completed\n[+] Time Taken : {totalTime}s\n")
