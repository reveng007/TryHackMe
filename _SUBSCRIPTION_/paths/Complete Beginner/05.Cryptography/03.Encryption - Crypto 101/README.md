
Only inportant things will ne noted here, rest see from the room 

Task2: Key terms
-----------------

1. Are SSH keys protected with a passphrase or a password?

--> passphrase


Task3: Why is Encryption important?
------------------------------------

1. What does SSH stand for?

--> secure shell

2. How do webservers prove their identity?

--> certificates

3. What is the main set of standards you need to comply with if you store or process payment card details?

--> PCI-DSS

PCI-DSS => Payment Card Industry Data Security Standard

> Whenever sensitive user data needs to be stored, it should be encrypted. Standards like PCI-DSS state that the data should be encrypted both at rest (in storage) AND while being transmitted. If you’re handling payment card details, you need to comply with these PCI regulations. Medical data has similar standards. With legislation like GDPR and California’s data protection, data breaches are extremely costly and dangerous to you as either a consumer or a business.


Task4: Crucial Crypto Maths
---------------------------

1. What's 30 % 5?

--> 0

2. What's 25 % 7

--> 4

3. What's 118613842 % 9091

--> 3565


Task5: Types of Encryption
---------------------------


Task5: Types of Encryption
---------------------------

1. Should you trust DES? Yea/Nay

--> Nay

2. What was the result of the attempt to make DES more secure so that it could be used for longer?

--> Triple DES

3. Is it ok to share your public key? Yea/Nay

--> Yea


Task6: RSA - Rivest Shamir Adleman
-----------------------------------

There are some excellent tools for defeating RSA challenges in CTFs, and my personal favorite is:

1. [https://github.com/Ganapati/RsaCtfTool](https://github.com/Ganapati/RsaCtfTool) which has worked very well for me. 

2. I’ve also had some success with [https://github.com/ius/rsatool](https://github.com/ius/rsatool)


1. p = 4391, q = 6659. What is n?

--> 29239669

Task7: Establishing Keys Using Asymmetric Cryptography
-------------------------------------------------------

A lot more detail on how HTTPS (one example where you need to exchange keys) really works from this excellent blog post:
[https://robertheaton.com/2014/03/27/how-does-https-actually-work/](https://robertheaton.com/2014/03/27/how-does-https-actually-work/)


Task8: Digital signatures and Certificates
-------------------------------------------

1. What company is TryHackMe's certificate issued to?

--> cloudflare


Task9: SSH Authentication
--------------------------

<ins>File for this Task: idrsa.id_rsa</ins>

1. What algorithm does the key use?

--> rsa

2. Crack the password with John The Ripper and rockyou, what's the passphrase for the key?

--> delicious



Task10: Explaining Diffie Hellman Key Exchange
----------------------------------------------


<ins>File for this task: gpg.zip</ins>


1. You have the private key, and a file encrypted with the public key. Decrypt the file. What's the secret word?

--> Pineapple


Steps:
```
unzip gpg.zip

sudo gpg --import tryhackme.key

sudo gpg message.gpg

ls

cat message
```

Task12: The Future - Quantum Computers and Encryption
------------------------------------------------------



