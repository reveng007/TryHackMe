There are two ways to search for installed scripts. 

✓ using the /usr/share/nmap/scripts/script.db file. 
  
  Despite the extension i.e. .db, this isn't actually a database so much as a formatted text file containing filenames and          categories for each available script.

  use : file script.db
	---->    script.db: ASCII text

  use like this: head script.db

  we can also grep through it to look for scripts. For example: 
  
  grep "ftp" /usr/share/nmap/scripts/script.db


✓  The second way to search for scripts is quite simply to use the ls command. For example, we could get the same results as in      the previous screenshot by using:

   ls -l /usr/share/nmap/scripts/*ftp*
 
   Note the use of asterisks (*) on either side of the search term.

   
   The same techniques can also be used to search for categories of script.
   
   For example:

   grep "safe" /usr/share/nmap/scripts/script.db


INSTALLING NEW SCRIPTS:

sudo apt update && sudo apt install nmap

OR,
Step1:
From Nmap: sudo wget -O /usr/share/nmap/scripts/<script-name>.nse https://svn.nmap.org/nmap/scripts/<script-name>.nse

Step2:
This must then be followed up with :        nmap --script-updatedb

which updates script.db file (SCRIPT DATABASE) to contain the newly downloaded script.



Read through this script : smb-os-discovery.nse . What does it depend on?

----> Open Script to see in: dependecies = { ..... }

