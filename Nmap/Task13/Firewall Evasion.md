1. We have already seen some techniques for bypassing firewalls like:
stealth scans, along with NULL, FIN and Xmas scans.

2. However, there is another very common firewall configuration which it's imperative we know how to bypass.

3. Your typical Windows host will, with its default firewall, block all _ICMP packets_.

This presents a problem: 
Not only do we often use ping to manually establish the activity of a target.

4. Nmap does the same thing by default. This means that Nmap will register a host with this firewall configuration as dead and not bother scanning it at all.

So, use: -Pn [ which tells Nmap to not bother pinging the host before scanning it.]

This means that Nmap will always treat the target host(s) as being alive, effectively bypassing the ICMP block.

However, it comes at the price of potentially taking a very long time to complete the scan (if the host really is dead then Nmap will still be checking and double checking every specified port).

NOTE:

It's worth noting that if you're already directly on the local network, Nmap can also use ARP requests to determine host activity. 

There are a variety of other switches which Nmap considers useful for firewall evasion. We will not go through these in detail, however, they can be found 

here:
https://nmap.org/book/man-bypass-firewalls-ids.html

The following switches are of particular note:

-f:- Used to fragment the packets (i.e. split them into smaller pieces) making it less likely that the         packets will be detected by a firewall or IDS.
    
An alternative to -f, but providing more control over the size of the packets: --mtu <number>, accepts    a maximum transmission unit size to use for the packets sent. This must be a multiple of 8.
    
--scan-delay <time>ms:- used to add a delay between packets sent. This is very useful if the network is unstable, but also for evading any time-based firewall/IDS triggers which may be in place.
    
--badsum:-Used to generate in invalid checksum for packets. Any real TCP/IP stack would drop this packet, however, firewalls may potentially respond automatically, without bothering to check the checksum of the packet. As such, this switch can be used to determine the presence of a firewall/IDS.


Which Nmap switch allows you to append an arbitrary length of random data to the end of packets?

---> --data-length

