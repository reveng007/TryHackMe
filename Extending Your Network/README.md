We'll cover the two primary categories of firewalls in the table below:



Firewall Category

<ins>Stateful</ins>

This type of firewall uses the entire information from a connection; rather than inspecting an individual packet, this firewall determines the behaviour of a device based upon the entire connection.

This firewall type consumes many resources in comparison to stateless firewalls as the decision making is dynamic. For example, a firewall could allow the first parts of a TCP handshake that would later fail.

If a connection from a host is bad, it will block the entire device.

<ins>Stateless</ins>

This firewall type uses a static set of rules to determine whether or not individual packets are acceptable or not. For example, a device sending a bad packet will not necessarily mean that the entire device is then blocked.

Whilst these firewalls use much fewer resources than alternatives, they are much dumber. For example, these firewalls are only effective as the rules that are defined within them. If a rule is not exactly matched, it is effectively useless.

However, these firewalls are great when receiving large amounts of traffic from a set of hosts (such as a Distributed Denial-of-Service attack)




Answer the questions below

1. What layers of the OSI model do firewalls operate at?


--> layer 3,layer 7

2. What category of firewall inspects the entire connection?

--> stateful

3. What category of firewall inspects individual packets?

--> stateless



Task 4  VPN Basics
-----------------


1. What VPN technology only encrypts & provides the authentication of data?

--> ppp


2. What VPN technology uses the IP framework?

--> ipsec

