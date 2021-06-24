Task3: Terminal Text Editors:
-----------------------------

1. Edit "task3" located in "tryhackme"'s home directory using Nano. What is the flag?

--> THM{TEXT_EDITORS}


Task4: General/Useful Utilities:
---------------------------------

1. Now, use Python 3's "HTTPServer" module to start a web server in the home directory of the "tryhackme" user on the deployed instance.

Download the file http://10.10.253.126:8000/.flag.txt onto the TryHackMe AttackBox

2. What are the contents?

--> THM{WGET_WEBSERVER}

Task5: Processes 101:
----------------------

see this portion AGAIN...


1. If we were to launch a process where the previous ID was "300", what would the ID of this new process be?

--> 301

2. If we wanted to cleanly kill a process, what signal would we send it?

--> SIGTERM

#### NOTE:

Though both of these signals are used for killing a process, there are some differences between the two: SIGTERM gracefully kills the process whereas SIGKILL kills the process immediately. SIGTERM signal can be handled, ignored and blocked but SIGKILL cannot be handled or blocked.

see: https://linuxhandbook.com/sigterm-vs-sigkill/


3. Locate the process that is running on the deployed instance (10.10.253.126). What flag is given?

--> THM{PROCESSES} 

4. What command would we use to stop the service "myservice"?

--> systemctl stop myservice

5. What command would we use to start the same service on the boot-up of the system?

--> systemctl enable myservice 

6. What command would we use to bring a previously backgrounded process back to the foreground?

--> fg

Task6: Maintaining Your System: Automation :-
------------------------------------------------

see: YT --> crontab Corey Schafer

1. When will the crontab on the deployed instance (10.10.133.15) run?

--> @reboot


Task7: Maintaining Your System: Package Management :-
-------------------------------------------------------

Removing packages:

1. add-apt-repository --remove ppa:PPA_Name/ppa
2. apt remove [software-name]


Task8: Maintaining Your System: Logs :-
-----------------------------------------

1. What is the IP address of the user who visited the site?

--> 10.9.232.111

2. What file did they access?

--> catsanddogs.jpg


