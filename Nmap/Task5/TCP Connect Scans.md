_"... If the connection does not exist (CLOSED) then a reset-acknowledge(RST/ACK) packet is sent in response to any incoming segment except another reset. In particular, SYNs addressed to a non-existent connection are rejected by this means."_

In other words, if Nmap sends:

1. A TCP request with the _SYN flag set_ to a **closed port**, the target server will respond with a TCP packet with the _RST/ACK (Reset/Acknowledge) flag set_.

#### NOTE:
A Reset packet is simply one with ***no payload*** and with the RST bit set in the TCP header flags and ACK flag.

-----------

***payload*** in network packet 

- Actual transmitted data sent by communicating endpoints; network protocols also specify the maximum length allowed for packet payloads.

-----------

Both _ACK_ and _RST flags_ are within same packet, is sent to _acknowledge_ what ever packet was sent before to the receiver by the sender. By this response, Nmap can establish that the port is CLOSED.

2. If, however, the request is sent to an **open port**, the target will respond with a TCP packet with the _SYN/ACK flags set_. Nmap then marks this port as being open (and completes the handshake by sending back a TCP packet with _ACK set_).

#### This is all well and good, however, there is a third possibility.

1. What if the port is ***open***, but hidden behind a **firewall**?

:arrow_right:
1. Many firewalls are configured to _simply drop incoming packets_.
Nmap sends a _TCP SYN request_, and receives ***nothing back***. This indicates that the port is being ***protected by a firewall*** and thus the port is considered to be _filtered_.

That said, it is very easy to configure a firewall to respond with a RST TCP packet. For example, in IPtables for Linux, a simple version of the command would be as follows:
```
iptables -I INPUT -p tcp --dport <port> -j REJECT --reject-with tcp-reset
```

