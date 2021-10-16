1. How would you perform a ping sweep on the 172.16.x.x network (Netmask: 255.255.0.0) using Nmap? (CIDR notation)

:right_arrow: nmap -sn 172.16.0.0/16

Answer will not be : ---> nmap -sn 172.16.x.x/16 because we are instructed to ping/ICMP/ARP scan the whole network...


