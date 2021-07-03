Task1: Key Terms
-----------------

We'll expand on some of them later in the room.

1. <ins>Plaintext</ins>
Data before encryption or hashing, often text but not always as it could be a photograph or other file instead.

2. <ins>Encoding</ins>
This is NOT a form of encryption, just a form of data representation like base64 or hexadecimal. Immediately reversible.

3. <ins>Hash</ins>
A hash is the output of a hash function. Hashing can also be used as a verb, "to hash", meaning to produce the hash value of some data.

4. <ins>Brute force</ins>
Attacking cryptography by trying every different password or every different key

5. <ins>Cryptanalysis</ins>
Attacking cryptography by finding a weakness in the underlying maths

1. Attacking cryptography by finding a weakness in the underlying maths

--> encoding


Task2: What is a hash function?
-------------------------------

Hash functions are quite different from encryption. There is no key, and it’s meant to be impossible (or very very difficult) to go from the output back to the input.


1. What is the output size in bytes of the MD5 hash function?

--> 16

2. Can you avoid hash collisions? (Yea/Nay)

--> Nay

3. If you have an 8 bit hash output, how many possible hashes are there?

--> 256 (=2^(no. of bits of hash) = 2^8)


Task3:  Uses for hashing
-------------------------

A rainbow table is a lookup table of hashes to plaintexts, so you can quickly find out what password a user had just from the hash. A rainbow table trades time taken to crack a hash for hard disk space, but they do take time to create.

Websites like Crackstation internally use HUGE rainbow tables to provide fast password cracking for hashes without salts. Doing a lookup in a sorted list of hashes is really quite fast, much much faster than trying to crack the hash.

##### Protecting against rainbow tables

To protect against rainbow tables, we add a salt to the passwords. The salt is randomly generated and stored in the database, unique to each user. In theory, you could use the same salt for all users but that means that duplicate passwords would still have the same hash, and a rainbow table could still be created specific passwords with that salt.

> The salt is added to either the start or the end of the password before it’s hashed, and this means that every user will have a different password hash even if they have the same password. Hash functions like bcrypt and sha512crypt handle this automatically. Salts don’t need to be kept private.

1. Crack the hash "d0199f51d2728db6011945145a1b607a" using the rainbow table

--> basketball

2. Crack the hash "5b31f93c09ad1d065c0491b764d04933" using online tools

--> tryhackme

3. Should you encrypt passwords? Yea/Nay

--> Nay


Task4:  Recognising password hashes
------------------------------------

Automated hash recognition tools such as [https://pypi.org/project/hashID/](https://pypi.org/project/hashID/) exist, but they are unreliable for many formats. For hashes that have a prefix, the tools are reliable. Use a healthy combination of context and tools.


Unix style password hashes are very easy to recognise, as they have a prefix.
The prefix tells you the hashing algorithm used to generate the hash.

The standard format is`$format$rounds$salt$hash`.

------------

Windows passwords are hashed using ***NTLM***, which is a variant of _md4_. They're visually identical to md4 and md5 hashes, so it's very important to use context to work out the hash type.

On **Linux**, password hashes are stored in _/etc/shadow_. This file is normally only readable by root. They used to be stored in /etc/passwd, and were readable by everyone.


On **Windows**, password hashes are stored in the _SAM_. Windows tries to prevent normal users from dumping them, but tools like _mimikatz_ exist for this. Importantly, the hashes found there are _split into NT hashes and LM hashes_.


Here's a quick table of the most Unix style password prefixes that you'll see.

Prefix			       Algorithm
$1$   			    --> md5crypt, used in Cisco stuff and older Linux/Unix systems

$2$, $2a$, $2b$, $2x$, $2y$ --> Bcrypt (Popular for web applications)

$6$	    -------->          sha512crypt (Default for most Linux/Unix systems)



A great place to find more hash formats and password prefixes is the hashcat example page, available here: [https://hashcat.net/wiki/doku.php?id=example_hashes](https://hashcat.net/wiki/doku.php?id=example_hashes)


1. How many rounds does sha512crypt ($6$) use by default?

--> 5000

2. What's the hashcat example hash (from the website) for Citrix Netscaler hashes?

--> 1765058016a22f1b4e076dccd1c3df4e8e5c0839ccded98ea   [From website]

3. How long is a Windows NTLM hash, in characters?

--> 32


Task5:  Password Cracking
-------------------------


We've already mentioned rainbow tables as a method to crack hashes that don't have a salt, but what if there's a salt involved?

You can't "decrypt" password hashes. They're not encrypted. You have to crack the hashes by hashing a large number of different inputs (often rockyou, these are the possible passwords), potentially adding the salt if there is one and comparing it to the target hash. Once it matches, you know what the password was. Tools like Hashcat and John the Ripper are normally used for this.


#### Why crack on GPUs?

Graphics cards have thousands of cores. Although they can’t do the same sort of work that a CPU can, they are very good at some of the maths involved in hash functions. This means you can use a graphics card to crack most hash types much more quickly. Some hashing algorithms, notably bcrypt, are designed so that hashing on a GPU is about the same speed as hashing on a CPU which helps them resist cracking.


<ins>NEVER (I repeat, NEVER!) use --force for hashcat</ins>. It can lead to false positives (wrong passwords being given to you) and false negatives (skips over the correct hash).

1. Crack this hash: $2a$06$7yoU3Ng8dHTXphAg913cyO6Bjs3K5lBnwq5FJyA6d01pMSrddr1ZG

1st identify the type of hash by talling against `hashcat --help`
```
$ hashcat -m 3200 hash.txt /usr/share/wordlists/rockyou.txt
```

-->  85208520

2. Crack this hash: 9eb7ee7f551d2f0ac684981bd1f1e2fa4a37590199636753efe614d4db30e8e1

1. using:`https://hashes.com/en/decrypt/hash`
2. using: crackstation
3. using: `hashcat -m 1400 hash.txt /usr/share/wordlists/rockyou.txt`

--> halloween

3. Crack this hash: $6$GQXVvW4EuM$ehD6jWiMsfNorxy5SINsgdlxmAEl3.yif0/c3NqzGLa0P.S7KRDYjycw5bnYkF5ZtB8wQy8KnskuWQS3Yr1wQ0

```
$ hashcat -m 1800 hash.txt /usr/share/wordlists/rockyou.txt -O
```

--> spaceman

4. Bored of this yet? Crack this hash: b6b0d451bbf6fed658659a9e7e5598fe

1. used: `https://hashes.com/en/decrypt/hash`
2. used: `https://crackstation.net/`

--> funforyou


Task6: Hashing for integrity checking
--------------------------------------

#### Integrity Checking

Hashing can be used to check that files haven't been changed. If you put the same data in, you always get the same data out. If even a single bit changes, the hash will change a lot. This means you can use it to check that files haven't been modified or to make sure that they have downloaded correctly. You can also use hashing to find duplicate files, if two pictures have the same hash then they are the same picture.

#### HAMCs

HMAC is a method of using a cryptographic hashing function to verify the authenticity and integrity of data. The TryHackMe VPN uses HMAC-SHA512 for message authentication, which you can see in the terminal output. A HMAC can be used to ensure that the person who created the HMAC is who they say they are (authenticity), and that the message hasn’t been modified or corrupted (integrity). They use a secret key, and a hashing algorithm in order to produce a hash.#### Integrity Checking

Hashing can be used to check that files haven't been changed. If you put the same data in, you always get the same data out. If even a single bit changes, the hash will change a lot. This means you can use it to check that files haven't been modified or to make sure that they have downloaded correctly. You can also use hashing to find duplicate files, if two pictures have the same hash then they are the same picture.

#### HAMCs

HMAC is a method of using a cryptographic hashing function to verify the authenticity and integrity of data. The TryHackMe VPN uses HMAC-SHA512 for message authentication, which you can see in the terminal output. A HMAC can be used to ensure that the person who created the HMAC is who they say they are (authenticity), and that the message hasn’t been modified or corrupted (integrity). They use a secret key, and a hashing algorithm in order to produce a hash.


1. What's the SHA1 sum for the amd64 Kali 2019.4 ISO? [http://old.kali.org/kali-images/kali-2019.4/](http://old.kali.org/kali-images/kali-2019.4/)

HINT: `You don't have to download the ISO, Offensive Security give you the checksums to make sure your download didn't get corrupted`

--> 186c5227e24ceb60deb711f1bdc34ad9f4718ff9

2. What's the hashcat mode number for HMAC-SHA512 (key = $pass)?

--> 1750


