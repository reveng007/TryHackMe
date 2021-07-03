TAsk1: John who?
----------------

#### What makes Hashes secure?

Hashing algorithms are designed so that they only operate one way. This means that a calculated hash cannot be reversed using just the output given. This ties back to a fundamental mathematical problem known as the [P vs NP relationship](https://en.wikipedia.org/wiki/P_versus_NP_problem)

While this is an extremely interesting mathematical concept that proves fundamental to computing and cryptography I am in no way qualified to try and explain it in detail here; but abstractly it means that the algorithm to hash the value will be "NP" and can therefore be calculated reasonably. However an un-hashing algorithm would be "P" and intractable to solve- meaning that it cannot be computed in a reasonable time using standard computers.


1. What is the most popular extended version of John the Ripper?

--> jumbo john


Task3: Wordlists
----------------

1. What website was the rockyou.txt wordlist created from a breach on?

--> rockyou.com



Task4: Cracking Basic Hashes
----------------------------


#### Automatic Cracking

`john --wordlist=/usr/share/wordlists/rockyou.txt hash_to_crack.txt`


#### Identifying Hashes

`python3 hash-id.py`



#### Format-Specific Cracking

`john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash_to_crack.txt`


<ins>A Note on Formats</ins>:

When you are telling john to use formats, if you're dealing with a standard hash type, e.g. md5 as in the example above, you have to prefix it with `raw-` to tell john you're just dealing with a standard hash type, though this doesn't always apply. To check if you need to add the prefix or not, you can list all of John's formats using `john --list=formats` and either check manually, or grep for your hash type using something like `john --list=formats | grep -iF "md5"`

#### <ins>All hashes are present here: in this folder `first_task_hashes`</ins>


1. What type of hash is hash1.txt?

--> md5

2. What is the cracked value of hash1.txt?

--> biscuit

3. What type of hash is hash2.txt?

--> sha1

4. What is the cracked value of hash2.txt

--> kangeroo

5. What type of hash is hash3.txt?

--> sha256

6. What is the cracked value of hash3.txt

--> microphone

7. What type of hash is hash4.txt?

--> whirlpool

8. What is the cracked value of hash4.txt

`john --format=whirlpool --wordlist=/usr/share/wordlists/rockyou.txt hash4.txt`

--> colossal


Task5: Cracking Windows Authentication Hashes
----------------------------------------------

#### NTHash / NTLM

NThash is the hash format that modern Windows Operating System machines will store user and service passwords in. It's also commonly referred to as "NTLM" which references the previous version of Windows format for hashing passwords known as "LM", thus "NT/LM".

A little bit of history, the NT designation for Windows products originally meant "New Technology", and was used- starting with [Windows NT](https://en.wikipedia.org/wiki/Windows_NT), to denote products that were not built up from the MS-DOS Operating System. Eventually, the "NT" line became the standard Operating System type to be released by Microsoft and the name was dropped, but it still lives on in the names of some Microsoft technologies. 

You can acquire NTHash/NTLM hashes by dumping the SAM database on a Windows machine, by using a tool like Mimikatz or from the Active Directory database: NTDS.dit. You may not have to crack the hash to continue privilege escalation- as you can often conduct a "pass the hash" attack instead, but sometimes hash cracking is a viable option if there is a weak password policy.


1. What do we need to set the "format" flag to, in order to crack this?

--> nt

2. What is the cracked value of this password?

`john --format=nt --wordlist=/usr/share/wordlists/rockyou.txt ntlm.txt`

--> mushroom



Task6: Cracking /etc/shadow Hashes
------------------------------------

This file is usually only accessible by the root user so in order to get your hands on the hashes you must have sufficient privileges, but if you do there is a chance that you will be able to crack some of the hashes.

#### Unshadowing

John can be very particular about the formats it needs data in to be able to work with it, for this reason- in order to crack /etc/shadow passwords, you must combine it with the /etc/passwd file in order for John to understand the data it's being given.
To do this, we use a tool built into the John suite of tools called _`unshadow`_. The basic syntax of unshadow is as follows:

`unshadow [path to passwd] [path to shadow]`

Example Usage:

`unshadow [local_passwd] [local_shadow] > unshadowed.txt`

<ins>Demo txt file: etchashes.txt</ins>


1. What is the root password? (--format = sha512crypt)

--> 1234


Task7: Single Crack Mode
--------------------------

<ins>File for this: hash7.txt</ins>

#### Single Crack Mode

So far we've been using John's wordlist mode to deal with brute forcing simple., and not so simple hashes.
But John also has another mode, called Single Crack mode.
In this mode, John uses only the information provided in the username, to try and work out possible passwords heuristically, by slightly changing the letters and numbers contained within the username.


#### Word Mangling

The best way to show what Single Crack mode is,  and what word mangling is, is to actually go through an example:

If we take the username: `Markus`

Some possible passwords could be:

- Markus1, Markus2, Markus3 (etc.)
- MArkus, MARkus, MARKus (etc.)
- Markus!, Markus$, Markus\* (etc.)


#### GECOS

John's implementation of word mangling also features compatibility with the Gecos fields of the UNIX operating system, and other UNIX-like operating systems such as Linux. 

So what are Gecos?

Remember in the last task where we were looking at the entries of both _/etc/shadow_ and _/etc/passwd_? Well if you look closely You can see that each field is seperated by a colon `":"`

> Each one of the fields that these records are split into are called ***Gecos*** fields.


##### NOTE:

1. John can take information stored in those records:
	- full name
	- home directory

to add in to the wordlist it generates when cracking /etc/shadow hashes with single crack mode.


#### Using Single Crack Mode

`john --single --format=[format] [path to file]`


##### A Note on File Formats in Single Crack Mode:

- If you're cracking hashes in single crack mode, you need to _change_ the **file format** that you're _feeding john_ for it to understand what data to create a wordlist from. 
- You do this by ***prepending the hash with the username that the hash belongs to***, so according to the above example- we would change the file hashes.txt.

**From**:
```
1efee03cdcb96d90ad48ccc7b8666033
```

**To**:
```
mike:1efee03cdcb96d90ad48ccc7b8666033
```

Now you're familiar with the Syntax for John's single crack mode, download the attached hash and crack it, assuming that the user it belongs to is called "Joker".


S1: Add "Joker:" in front of hash in hash7.txt file

S2: `john --single --format=Raw-MD5 hash7.txt`


1. What is Joker's password?

--> Jok3r


Task8: Custom Rules
--------------------

#### What are Custom Rules?

As we journeyed through our exploration of what John can do in Single Crack Mode- you may have some ideas about what some good mangling patterns would be, or what patterns your passwords often use- that could be replicated with a certain mangling pattern.

The good news is you can define your ***own sets of rules***, which John will use to dynamically create passwords. This is especially useful when you know more information about the password structure of whatever your target is.


#### Common Custom Rules

Many organisations will require a certain level of password complexity to try and combat dictionary attacks, meaning that if you create an account somewhere, go to create a password and enter:

`polopassword`

You may receive a prompt telling you that passwords have to contain at least one of the following:

- Capital letter
- Number
- Symbol

This is good!
However, we can exploit the fact that most users will be predictable in the location of these symbols.

For the above criteria, many users will use something like the following:

Polopassword1!

This pattern can let us exploit ***password complexity predictability***.

**Now this does meet the password complexity requirements, however as an attacker we can exploit the fact we know the likely position of these added elements to create dynamic passwords from our wordlists**.


#### How to create Custom Rules

Custom rules are defined in the `john.conf` file, usually located in `/etc/john/john.conf` if you have installed John using a package manager or built from source with `make`.

To get a full view of the types of modifiers: [openwall](https://www.openwall.com/john/doc/RULES.shtml)


Let's go over the syntax of these custom rules, using the example above as our target pattern.

<ins>1st line:</ins>

1. `[List.Rules:THMRules]` - Is used to define the name of your rule, this is what you will use to call your custom rule as a John argument.


2. We will then use a _regex pattern match_ to define where in the word will be modified:

`Az` - Takes the word and **appends** it with the characters you define

`A0` - Takes the word and **prepends** it with the characters you define

`c` - **Capitalises the character positionally**

_These can be used in combination to define where and what in the word you want to modify_.


3. Lastly, we then need to define what characters should be appended, prepended or otherwise included

we do this by adding character sets in square brackets `[ ]` in the order they should be used. These directly follow the modifier patterns inside of double quotes `" "`

Some examples:

`[0-9]` - Will include numbers 0-9

`[0]` - Will include only the number 0

`[A-z]` - Will include both upper and lowercase

`[A-Z]` - Will include only uppercase letters

`[a-z]` - Will include only lowercase letters

`[a]` - Will include only a

`[!£$%@]` - Will include the symbols !£$%@


#### Hands-On:

Putting this all together, in order to generate a wordlist from the rules that would match the example password _"Polopassword1!"_ (assuming the word polopassword was in our wordlist) we would create a rule entry that looks like this:

`[List.Rules:PoloPassword]`

`cAz"[0-9] [!£$%@]"`


In order to:

Capitalise the first  letter - `c`

Append to the end of the word - `Az`

A number in the range 0-9 - `[0-9]`

Followed by a symbol that is one of `[!£$%@]`


#### Using Custom Rules

We could then call this custom rule as a John argument using the `--rule=PoloPassword` flag.

Full cmd:
```
john --wordlist=[path to wordlist] --rule=PoloPassword [path to file]
```


1. What do custom rules allow us to exploit?

--> password complexity predictability

2. What rule would we use to add all capital letters to the end of the word?

--> cAz"[a-z]"

3. What flag would we use to call a custom rule called "THMRules"

--> --rule=THMRules



Task9:  Cracking Password Protected Zip Files
---------------------------------------------

<ins>Folder for this task: secure folder</ins>


#### Zip2John

Similarly to the `unshadow tool` that we used previously, we're going to be using the **zip2john** tool to _convert the zip file into a hash format_ that John is able to understand, and hopefully crack.

`zip2john [options] [zip file] > [output file]`


`[options]` - Allows you to pass specific checksum options to zip2john, this shouldn't often be necessary

**Example Usage**
`zip2john zipfile.zip > zip_hash.txt`


#### Cracking

`john --wordlist=/usr/share/wordlists/rockyou.txt zip_hash.txt`



#### Practical

1. What is the password for the secure.zip file?

--> pass123

2. What is the contents of the flag inside the zip file?

--> `THM{w3ll_d0n3_h4sh_r0y4l}`




Task10:  Cracking Password Protected RAR Archives
-------------------------------------------------

<ins>File for this Task: secure.rar</ins>

#### Rar2John

Almost identical to the _zip2john tool_ that we just used, we're going to use the **rar2john tool** to convert the _rar file into a hash format_ that John is able to understand.


The basic syntax is as follows:

`rar2john [rar file] > [output file]`


**Example Usage**
`rar2john rarfile.rar > rar_hash.txt`



#### Cracking

`john --wordlist=/usr/share/wordlists/rockyou.txt rar_hash.txt`


1. What is the password for the secure.rar file?

--> password


2. What is the contents of the flag inside the zip file? [Using _unrar_ tool]

`unrar e secure.rar`

--> `THM{r4r_4rch1ve5_th15_t1m3}`




Task11:  Cracking SSH Keys with John
-------------------------------------


<ins>File for this task: idrsa.id_rsa</ins>

#### SSH2John

As the name suggests ssh2john converts the `id_rsa private key` that you use to login to the SSH session into hash format that john can work with.

On Kali, `python /usr/share/john/ssh2john.py`


For my machine: `python /usr/share/john/ssh2john`


#### Syntax

`ssh2john [id_rsa private key file] > [output file]`


**Example Usage**

`ssh2john id_rsa > id_rsa_hash.txt`



#### Cracking

`john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa_hash.txt`


1. What is the SSH private key password?

--> mango



For further reading: [openwall](https://www.openwall.com/john/)
