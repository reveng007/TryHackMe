port: 22, 80 open


port 80: 1. main page source contains name `john` in comments
	 2. gobuster discovered: `uploads` and `secret` directory which contains `passwd wordlist` and `rsa priv key` respectively.

Then used `ssh2john.py` to find out the _hash_ of the `rsa priv key` to use john along with the discovered wordlist against the hash of `id_rsa` priv key.

got the passwd: letmein
We already got the user name: `john`


used ssh to login and found out the user flag


I saw when I used `id`: john user is present in `lxd` group

I used lxd privilege escalation (hacking article) to escalate and got the flag(root)


