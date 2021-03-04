Walkthrough:
-----------------
-----------------

```
PORT   STATE SERVICE REASON  VERSION
21/tcp open  ftp     syn-ack vsftpd 3.0.3
22/tcp open  ssh     syn-ack OpenSSH 8.0 (protocol 2.0)
80/tcp open  http    syn-ack Apache httpd 2.4.37 ((centos))
Service Info: OS: Unix
```
#### Moved to:  http://ip/backup directory (used gobuster)

#### Downloaded backup.zip 
#### we would get: 
```
priv.key
CustomerDetails.xlsx.gpg
```
```
$ gpg --import priv.key

$ gpg --decrypt CustomerDetails.xlsx.gpg > CustomerDetails.xlsx
```
#### Now, we got the password in excel spread sheet 

### Unfortunatly these are not ssh creds ( realised after using it against ssh authn)

### Then I used it to enumerate FTP, where it worked

#### I uploaded revshell (using put utility) and executed it to get a shell as apache. Then elivated privilege to paradox with creds we got but the shell we got is not stable.

#### So, lets login via ssh, We did it via key-based auth... We will copy our .pub key to trgt machine's authorised_keys file

#### Then: ssh paradox@ip

#### Found nothing, uploaded linpeas ---> wget was not installed, so I used curl to download

#### Saw that nfs was running and linpeas reposted a vuln ----> no_root_squash

See: https://blog.hydrashead.net/posts/thm-overpass3/

### So, what is no_root_squash ??

```
This option basically gives authority to the root user on the client to access files on the NFS server as root. And this can lead to serious security implication.
```
### See this link: https://www.hackingarticles.in/linux-privilege-escalation-using-misconfigured-nfs/ 
