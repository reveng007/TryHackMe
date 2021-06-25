Task2: A Bit of Background on Linux:
--------------------------------------

1. Research: What year was the first release of a Linux operating system?

--> 1991

Task3: xxxxxx:
----------------



Task4: Running Your First few Commands:
-----------------------------------------

1. If we wanted to output the text "TryHackMe", what would our command be?

---> echo TryHackMe

2. What is the username of who you're logged in as on your deployed Linux machine?

--> tryhackme


Task5: Interacting With the Filesystem! :
------------------------------------------

1. On the Linux machine that you deploy, how many folders are there?

--> 4

2. Which directory contains a file? 

--> folder4

3.  Which directory contains a file? 

--> Hello World!

4. Use the cd command to navigate to this file and find out the new current working directory. What is the path?

--> /home/tryhackme/folder4


Task6: Searching for Files:
----------------------------

1. Use grep on "access.log" to find the flag that has a prefix of "THM". What is the flag? 

--> THM{ACCESS}


Task7: An Introduction to Shell Operators:
-------------------------------------------

1. If we wanted to run a command in the background, what operator would we want to use?

--> &

2. If I wanted to replace the contents of a file named "passwords" with the word "password123", what would my command be?

--> echo password123 > passwords

3. Now if I wanted to add "tryhackme" to this file named "passwords" but also keep "passwords123", what would my command be

--> echo tryhackme >> passwords

