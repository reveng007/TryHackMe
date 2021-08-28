***NULL scans (-sN)***:
- Are when the TCP request is sent with _no flags set at all_.
As per the RFC, the target host should respond with a _RST/ACK_ if the port is **closed**.

https://i.imgur.com/ABCxAwf.png

***FIN scans (-sF)***:
- Work in an almost identical fashion; however, instead of sending a completely empty packet, a request is sent with the FIN flag (usually used to gracefully close an active connection).

- Once again, Nmap expects a RST/ACK if the port is closed.

https://i.imgur.com/gIzKbEk.png

As with the other two scans in this class, 

***Xmas scans (-sX)***:
- Send a _malformed TCP packet_ and expects a _RST response_ for **closed ports**. It's referred to as an xmas scan as the flags that it sets (PSH, URG and FIN) give it the appearance of a blinking christmas tree when viewed as a packet capture in Wireshark.

https://i.imgur.com/gKVkGug.png

    SYN - Initiates a connection
    ACK - Acknowledges received data
    FIN - Closes a connection
    RST - Aborts a connection in response to an error , which is actually a packet with no payload.

The other two flags, PSH (push) and URG (urgent), aren't as well-known.

See: https://packetlife.net/blog/2011/mar/2/tcp-flags-psh-and-urg/
     https://www.geeksforgeeks.org/tcp-flags/



Why are NULL, FIN and Xmas scans generally used?

That said, the goal here is, of course, firewall evasion. Many firewalls are configured to drop incoming TCP packets to blocked ports which have the SYN flag set (thus blocking new connection initiation requests). By sending requests which do not contain the SYN flag, we effectively bypass this kind of firewall. Whilst this is good in theory, most modern IDS solutions are savvy to these scan types, so don't rely on them to be 100% effective when dealing with modern systems.

Which common OS may respond to a NULL, FIN or Xmas scan with a RST for every port?

It's also worth noting that while RFC 793 mandates that network hosts respond to malformed packets with a RST TCP packet for closed ports, and don't respond at all for open ports; this is not always the case in practice.

In particular ***Microsoft Windows (and a lot of Cisco network devices)*** are known to respond with a _RST_ to _any malformed TCP packet_ -- _regardless_ of whether the port is actually _open or not_.

`This results in all ports showing up as being closed.`

***Non-windows Servers*** are _only vulnerable_ to these `3 scans`, NULL, FIN and Xmas scan.

