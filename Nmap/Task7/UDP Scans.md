1. When a packet is sent to an ***open UDP port***, there should be no response. When this happens, Nmap refers to the port as being _open|filtered_. 
In other words, it suspects that the port is **open**, but it could be **firewalled**. If it gets a **UDP response** _(which is very unusual)_, then the port is marked as _open_.

More commonly there is _no response_, in which case the request is sent **a second time as a double-check**. If there is still no response then the port is marked **open|filtered** and Nmap moves on.

2. When a packet is sent to a ***closed UDP port***, the target should respond with an _ICMP (ping) packet containing a message that the port is unreachable_. This clearly identifies _closed ports_, which Nmap marks as such and moves on.

3. Due to this _difficulty_ in identifying whether a _UDP port_ is actually **open**, UDP scans tend to be _incredibly slow in comparison to the various TCP scans (in the region of 20 minutes to scan the first 1000 ports, with a good connection)_.

For this reason, it's usually good practice to run an Nmap scan with `--top-ports <number>` enabled.

For example:
Scanning with 
```
nmap -sU --top-ports 20 <target>
```
Will scan the top 20 most commonly used UDP ports, resulting in a much more acceptable scan time.

4. When scanning _UDP ports_, Nmap usually sends **completely empty requests -- just raw UDP packets**. That said, for ports which are usually occupied by well-known services, it will instead send a protocol-specific payload which is more likely to elicit a response from which a more accurate result can be drawn.


