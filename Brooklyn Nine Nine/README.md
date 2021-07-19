From nmap scan got:

port 80, 22,21 open

used ftp to login in port 21 via `ftp` username

Got a file showing `jake` as username

Then did bruteforce on ssh server with `jake`

Got the creds and loged in to jake account

Got the user flag: Then used sudo to escalate priv with `less` using ***GTFObin*** 

see : [For the 2nd method](https://m0ndzon3.medium.com/tryhackme-write-up-brooklyn-nine-nine-first-method-240daf9d0a01)

