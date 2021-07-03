Task2:  Walkthrough Hash identification
----------------------------------------

1. Launch Haiti on this hash:

`741ebf5166b9ece4cca88a3868c44871e8370707cf19af3ceaa4a6fba006f224ae03f39153492853`
What kind of hash it is?

```
$ haiti 741ebf5166b9ece4cca88a3868c44871e8370707cf19af3ceaa4a6fba006f224ae03f39153492853

RIPEMD-320 [JtR: dynamic_150]
```
--> RIPEMD-320

2. Launch Haiti on this hash:

`1aec7a56aa08b25b596057e1ccbcb6d768b770eaa0f355ccbd56aee5040e02ee`

```
$ haiti 1aec7a56aa08b25b596057e1ccbcb6d768b770eaa0f355ccbd56aee5040e02ee

SHA-256 [HC: 1400] [JtR: raw-sha256]
GOST R 34.11-94 [HC: 6900] [JtR: gost]
SHA3-256 [HC: 17400] [JtR: dynamic_380]
Keccak-256 [HC: 17800] [JtR: raw-keccak-256]
Snefru-256 [JtR: snefru-256]
RIPEMD-256 [JtR: dynamic_140]
Haval-256 (3 rounds) [JtR: haval-256-3]
Haval-256 (4 rounds) [JtR: dynamic_290]
Haval-256 (5 rounds) [JtR: dynamic_300]
GOST CryptoPro S-Box
Skein-256 [JtR: skein-256]
Skein-512(256)
PANAMA [JtR: dynamic_320]
BLAKE2-256
```

3. What is Keccak-256 Hashcat code?

--> 17800

4. What is Keccak-256 John the Ripper code?

--> raw-keccak-256


Task3:  Walkthrough Wordlists
-----------------------------

[SecLists](https://github.com/danielmiessler/SecLists) is a collection of multiple types of lists used during security assessments, collected in one place. List types include usernames, passwords, URLs, sensitive data patterns, fuzzing payloads, web shells, and many more.

[wordlistctl](https://github.com/BlackArch/wordlistctl) is a script to `fetch`, `install`, `update` and `search wordlist archives` from _websites_ offering wordlists with more than 6300 wordlists available.

[Rawsec's CyberSecurity Inventory](https://inventory.raw.pm/overview.html) is an inventory of tools and resources about CyberSecurity. The Cracking category will be especially useful to find wordlist generator tools.

1. To search for this wordlist with wordlistclt run:

`wordlistctl search rockyou`

2. Which option do you need to add to the previous command to search into local archives instead of remote ones?

--> -l

3. Download and install rockyou wordlist by running this command: 
`wordlistctl fetch -l rockyou`

4. Now search again for rockyou on your local archive with `wordlistctl search -l rockyou`

You should see that the wordlist is deployed at `/usr/share/wordlists/passwords/rockyou.txt.tar.gz`

But the wordlist is compressed in a tar.gz archive, to decompress it run `wordlistctl fetch -l rockyou -d`.
If you run wordlistctl search -l rockyou one more time, what is the path where is stored the wordlist? 

--> /usr/share/wordlists/passwords/rockyou.txt


5. You can search for a wordlist about a specific subject (eg. facebook) `wordlistctl search facebook` or list all wordlists from a category (eg. fuzzing) `wordlistctl list -g fuzzing`.

What is the name of the first wordlist in the usernames category?

`python3 wordlistctl.py list -g usernames`

--> CommonAdminBase64


Task4:  Walkthrough Cracking tools, modes & rules
-------------------------------------------------

Finally you'll need a cracking tool, the 2 very common ones are:

1. Hashcat
2. John the Ripper

There are several modes of cracking you can use:

- **Wordlist mode**, which consist in trying all words contained in a dictionary. For example, a list of common passwords, a list of usernames, etc.
- **Incremental mode**, which consist in trying all possible character combinations as passwords. This is powerful but much more longer especially if the password is long.
- **Rule mode**, which consist in using the wordlist mode by adding it some pattern or mangle the string. For example adding the current year, or appending a common special character.

There are 2 ways of performing a rule based bruteforce:

1. Generating a custom wordlist and using the classic wordlist mode with it.
2. Using a common wordlist and tell the cracking tool to apply some custom mangling rules on it.


The second option is much more powerful as you wont waste gigabytes by storing tons of wordlists and waste time generating ones you will use only one time. Rather having a few interesting lists and apply various mangling rules that you can re-use over different wordlist.


John the Ripper already include various mangling rules but you can create your owns and apply them the wordlist when cracking:

`$ john hash.txt --wordlist=/usr/share/wordlists/passwords/rockyou.txt rules=norajCommon02`


You can consult John the Ripper [Wordlist rules syntax](https://www.openwall.com/john/doc/RULES.shtml) for creating your own rules.

I'll give you the main ideas of mutation rules, of course several can be combined together.


- `Border mutation` - commonly used combinations of digits and special symbols can be added at the end or at the beginning, or both
- `Freak mutation` - letters are replaced with similarly looking special symbols
- `Case mutation` - the program checks all variations of uppercase/lowercase letters for any character
- `Order mutation` - character order is reversed
- `Repetition mutation` - the same group of characters are repeated several times
- `Vowels mutation` - vowels are omitted or capitalized
- `Strip mutation` - one or several characters are removed
- `Swap mutation` - some characters are swapped and change places
- `Duplicate mutation` - some characters are duplicated
- `Delimiter mutation` - delimiters are added between characters


1. Depending of your distribution, the John configuration may be located at `/etc/john/john.conf` and/or `/usr/share/john/john.conf`. To locate the JtR install directory run locate `john.conf`, then create `john-local.conf` in the same directory (in my case `/usr/share/john/john-local.conf`) and create our rules in here.

--> In my case, /usr/share/john/john-local.conf

2. Let's use the top 10 000 most used password list from SecLists (`/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt`) and generate a simple border mutation by appending all 2 digits combinations at the end of each password.
Let's edit `/usr/share/john/john-local.conf` and add a new rule:
```
[List.Rules:THM01]
$[0-9]$[0-9]
```

3. Now let's crack the SHA1 hash `2d5c517a4f7a14dcb38329d228a7d18a3b78ce83`, we just have to write the hash in a text file and to specify the hash type, the wordlist and our rule name. `john hash.txt --format=raw-sha1 --wordlist=/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt --rules=THM01`

What was the password?

--> moonligh56


Task5:  Walkthrough Custom wordlist generation
-----------------------------------------------

As I said in the previous task mangling rules avoid to waste storage space and time but there are some cases where generating a custom wordlist could be a better idea:

- You will often re-use the wordlist, generating one will save computation power rather than using a mangling rule
- You want to use the wordlist with several tools
- You want to use a tool that support wordlists but not mangling rules
- You find the custom rule syntax of John too complex

see: [Null Byte Mentalist](https://www.youtube.com/watch?v=01-Dcz1hFw8&t=18s)


