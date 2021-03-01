'''
This script does not solve our purpose 
to extract everything from a particular 
packet number. Abadoned script. 
'''

#!/usr/bin/python3

from scapy.all import *

pcap_file = input("Enter pcap file path: ")

#Reading pcap file
packets = rdpcap(pcap_file)

print("----"*20,"\n")

# simple stats
print(packets)


# Examining specific packets
spcfc_pkt = packets[79]

print(spcfc_pkt)

#type of packet
layer = type(spcfc_pkt)

print('''
Layer: ''', layer,"\r\n")

#dumping Hex
hexdump(spcfc_pkt)
print("\n")

ls(spcfc_pkt)

print("------")

spcfc_pkt.show()
