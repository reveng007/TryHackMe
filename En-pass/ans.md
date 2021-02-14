

# THM: En-pass
-----------------
-----------------

## Task 1  Enpass:

> Think-out-of-the-box

## 1.

### At 1st let us ping the target ip,
```
$~> ping 10.10.17.128

PING 10.10.17.128 (10.10.17.128) 56(84) bytes of data.
64 bytes from 10.10.17.128: icmp_seq=1 ttl=63 time=232 ms
64 bytes from 10.10.17.128: icmp_seq=2 ttl=63 time=251 ms
64 bytes from 10.10.17.128: icmp_seq=3 ttl=63 time=241 ms
^C
--- 10.10.17.128 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 231.758/241.246/250.534/7.666 ms

```
### Pinging results in giving us ttl value of 63 (nearly equal to 64), as we know that by default Linux machine is set to have a ttl value of 64 and windows as 128.

### So, it is Linux, Ok...

### Now,
```
 $~> sudo nmap 10.10.17.128 --open -sV -vv

             -- snip --

PORT     STATE SERVICE REASON         VERSION
22/tcp   open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
8001/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```
### lets visit the site,

### Assuming that being a password and enpass as user, lets login via ssh,
```
$~> ssh enpass@10.10.17.128

enpass@10.10.17.128: Permission denied (publickey).
```
### We were unable, but we know that we can't just login to ssh via "***password***", we will be needing "_publickey_"

### Now, lets use gobuster for directory bruteforcing,
 ```
  ~> gobuster dir -e -u http://10.10.112.97:8001 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt

                        -- snip --

===============================================================
2021/02/14 03:26:35 Starting gobuster
===============================================================
http://10.10.112.97:8001/index.html (Status: 200)
http://10.10.112.97:8001/web (Status: 301)
http://10.10.112.97:8001/reg.php (Status: 200)
http://10.10.112.97:8001/403.php (Status: 403)
http://10.10.112.97:8001/zip (Status: 301)
===============================================================
2021/02/11 20:39:09 Finished
===============================================================

```
### Lets again, do the same with /web, later we will do reg.php and 403.php
```
$~> gobuster dir -u http://10.10.17.128:8001/web -w /usr/share/wordlists/
dirbuster/directory-list-2.3-small.txt

===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.17.128:8001/web
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2021/02/11 20:48:53 Starting gobuster
===============================================================
/resources (Status: 301)
                      -- snip --

```
### Again, the same,
```
$~> gobuster dir -u http://10.10.17.128:8001/web/resources -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt

===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.17.128:8001/web/resources
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2021/02/11 21:16:55 Starting gobuster
===============================================================
/infoseek (Status: 301)
                       -- snip --

```
### You know what I'm going to say :sunglasses:,
```
$~> gobuster dir -u http://10.10.17.128:8001/web/resources/infoseek -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt

===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.17.128:8001/web/resources/infoseek
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2021/02/11 21:30:50 Starting gobuster
===============================================================
/configure (Status: 301)
                         -- snip --

```
### You know :sunglasses:. Actually we will do this until something different happens.

```
$~> gobuster dir -u http://10.10.17.128:8001/web/resources/infoseek/configure -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.17.128:8001/web/resources/infoseek/configure
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2021/02/11 21:34:46 Starting gobuster
===============================================================
/key (Status: 200)
                     -- snip --

```
### Yupp!! We got a "__Status code__" of **200**...
 
 * [x] 1st one done...

## 2.

### Now I traversed:

![alt text] (http://https://github.com/Soumyanil-Biswas/TryHackMe/blob/main/En-pass/images/1.ssh_passwd_assumed.png/zip) and extracted a.zip file to get the username.

### I used this script to extract all:

```
#!/bin/bash

for i in `seq 1 100`;
do
	wget -q http://10.10.112.97:8001/zip/a$i.zip;
	unzip a$i.zip;
	cat a;
	rm a;
 	rm a$i.zip;

done
```
### All the files resulted in one name,
```
$~> ./download_unzip.sh

Archive:  a1.zip
 extracting: a                       
sadman
Archive:  a2.zip
 extracting: a                       
sadman
Archive:  a3.zip
 extracting: a                       
sadman
Archive:  a4.zip
 extracting: a                       
sadman
Archive:  a5.zip
 extracting: a                       
sadman
Archive:  a6.zip
 extracting: a                       
sadman
Archive:  a7.zip
 extracting: a                       
sadman
Archive:  a8.zip
 extracting: a                       
sadman
Archive:  a9.zip
 extracting: a                       
sadman
                      --- snip ---
```
### Every single one resulted in 'sadman'

### As we got to know that we have to use public key to access ssh, we have to make a file with the content we got from the website .

```
$~> ssh -i priv_key <username>@<ip>
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for 'priv_key' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "priv_key": bad permissions
<username>@10.10.17.128: Permission denied (publickey).

```
### Now we will change the permission of the file to least priv. as per the instruction.
```
$~> chmod 400 priv_key

$~> ll priv_key

-r-------- 1 kali kali 1.8K Feb 11 23:00 priv_key

$~> ssh -i priv_key enpass@10.10.17.128

Load key "priv_key": invalid format
<username>@10.10.17.128: Permission denied (publickey).

```
### Now also it didn't work...We actually need public key not private key.

### I searched :https://serverfault.com/questions/52285/create-a-public-ssh-key-from-the-private-key

```
$~> ssh-keygen -y -f id_rsa > id_rsa.pub

Load key "id_rsa": invalid format
```
### Didn't get till now...

### I was totally carried away with this...

## Now, lets go to reg.php page,

### We got a submition page, here we can submit a php script to get a connection from target server.

### We didn't get any.

### see: https://shishirsubedi.com.np/thm/enpass/   

### and see: https://apjone.uk/tryhackme-en-pass/

### and also see: https://shamsher-khan.medium.com en-pass-tryhackme-writeup-a4a56e084569

### From the php code portion.

### Password: cimihan_are_you_here?

### For Openssl refer : 

### 1. https://www.geeksforgeeks.org/practical-uses-of-openssl-command-in-linux/

### 2. https://www.freecodecamp.org/news/openssl-command-cheatsheet-b441be1e8c4a/#4fe9

### user flag: 1c5ccb6ce6f3561e302e0e516c633da9

### root flag: 5d45f08ee939521d59247233d3f8faf

 
