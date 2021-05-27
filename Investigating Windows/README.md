
1. Whats the version and year of the windows machine?

> Windows server 2016

process:
```
cmd.exe --> winver
```

2. Which user logged in last?

> Administrator

process:
```
s1: open : eventvwr.msc --> s2: Windows logs --> Security (Upper table)
```

3. When did John log onto the system last?

Answer format: MM/DD/YYYY H:MM:SS AM/PM

> 03/02/2019 5:48:32 PM

```
s1: open: cmd.exe 

> net user john

	x ---snip --X

Last logon                   3/2/2019 5:48:32 PM 
```

OR, to be specific

```
> net user john | findstr /B /C:"Last logon"                                     

Last logon                   3/2/2019 5:48:32 PM
```
OR, powershell
```powershell
ForEach ($user in Get-LocalUser) {echo $user.Name $user.Lastlogon}
```
4. What IP does the system connect to when it first starts?

> 10.34.2.3
```
win key ---> regedit --> HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
--> Here
```
**HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run**
_This registry key can control the programs to run each time that a user logged on. This key is also used by malware to become persistence on the system._

5. What two accounts had administrative privileges (other than the Administrator user)?

Answer format: username1, username2

> Guest, Jenny

```
windows key -->  Computer management --> Local Users and Groups --> 
Users --> Click on users --> Properties --> Member Of
```

see: Other techniques: [link](https://www.isumsoft.com/windows-10/how-to-view-a-list-of-all-user-accounts-windows-10.html)

6. Whats the name of the scheduled task that is malicous.

> Clean file system

> `Windows Task Scheduler` is a inbuilt tool that enables you to create and execute a automatically schedule any task on your system. Most of the time malware use this features to do it’s bad things on your system. 

```
Win key --> Task scheduler --> Task sceduler library --> then play with those names
```
7. What file was the task trying to run daily?

> nc.ps1
```
Follow the above mentioned rule
```
8. What port did this file listen locally for?

> 1348

9. When did Jenny last logon?

> Never
```
>net user jenny |  findstr /B /C:"Last logon"
Last logon                   Never

10. At what date did the compromise take place?
Answer format: MM/DD/YYYY

> 03/02/2019
```
Just same: Viewing Task scheduler
```

11. At what time did Windows first assign special privileges to a new logon?
Answer format: MM/DD/YYYY HH:MM:SS AM/PM

> 03/02/2019 4:04:49 PM
```
Just same: Viewing Task scheduler
```

12. What tool was used to get Windows passwords?

> mimikatz
```
Saw a name "GameOver" in Task Scheduler --> it executes a .exe file present in a 
C:\TMP directory with named as:
##### ***C:\TMP\mim.exe sekurlsa::LogonPasswords > C:\TMP\o.txt***
Seeing this we can say that it is mimikatz, but then also I went to that folder to cross check.

13. What was the attackers external control and command servers IP?

> 76.32.97.132

##### Windows hosts file is used for maps the server or hostname to IP addresses.
In windows the location of the hosts file is ***C:\Windows\System32\drivers\etc\hosts***

14. Check for DNS poisoning, what site was targeted?

> google.com

15. What was the last port the attacker opened?

> 1337

From: **Windows firewall’s Inbound Rules**

16. What was the extension name of the shell uploaded via the servers website?

> .jsp

**Explanation:**
Microsoft uses IIS (Internet Informaion Services) as a default web server on the Windows. inetpub is the default folder situated under C:\inetpub. It contains the webserver’s content. wwwroot is a subfolder placed under the inetpub (C:\inetpub\wwwroot) holds all the content like of a webpages.
