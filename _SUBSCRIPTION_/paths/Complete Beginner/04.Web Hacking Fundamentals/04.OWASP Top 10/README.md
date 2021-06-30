
#### I will only write those points which are important to me now...


See from room...

Task5: [Severity 1] Command Injection Practical
------------------------------------------------

What is Active Command Injection?

- **`Blind command injection`** occurs when the system command made to the server does not return the response to the user in the HTML document.

- **`Active command injection`** will return the response to the user. It can be made visible through several HTML elements. 

Let's consider a scenario: 
**`EvilCorp`** has started development on a web based shell but has accidentally left it exposed to the Internet.  It's nowhere near finished but contains the same command injection vulnerability as before!  But this time, the response from the system call can be seen on the page! They'll never learn!

Just like before, let's look at the sample code from evilshell.php and go over what it's doing and why it makes it active command injection.  See if you can figure it out.  I'll go over it below just as before.

3. What user is this app running as?

```
ps -aux | grep evilshell.php

Result:

www-data 1541 0.0 0.0 4628 808 ? S 16:40 0:00 sh -c ps -aux | grep evilshell.php www-data 1543 0.0 0.1 11464 1048 ? S 16:40 0:00 grep evilshell.php
```
---> www-data


Task6:  [Severity 2] Broken Authentication
--------------------------------------------


If an attacker is able to find flaws in an authentication mechanism, they would then successfully gain access to other users’ accounts. This would allow the attacker to access sensitive data (depending on the purpose of the application).

Some common flaws in authentication mechanisms include:

- **`Brute force attacks`**: If a web application uses usernames and passwords, an attacker is able to launch brute force attacks that allow them to guess the username and passwords using multiple authentication attempts. 

- **`Use of weak credentials`**: web applications should set strong password policies. If applications allow users to set passwords such as ‘password1’ or common passwords, then an attacker is able to easily guess them and access user accounts. They can do this without brute forcing and without multiple attempts.

- **`Weak Session Cookies`**: Session cookies are how the server keeps track of users. If session cookies contain predictable values, an attacker can set their own session cookies and access users’ accounts. 


There can be various mitigation for broken authentication mechanisms depending on the exact flaw:

- To avoid **`password guessing attacks`**, ensure the application enforces a `strong password policy`.

- To avoid **`brute force attacks`**, ensure that the application enforces an `automatic lockout` after a certain number of attempts.
This would prevent an attacker from launching more brute force attacks.

- Implement **`Multi Factor Authentication`** - If a user has multiple methods of authentication, for example, using username and passwords and receiving a code on their mobile device, then it would be difficult for an attacker to get access to both credentials to get access to their account.



Task9: [Severity 3] Sensitive Data Exposure (Supporting Material 1)
--------------------------------------------------------------------

**Databases** can also be stored as files, these databases are referred to as **`"flat-file" databases`**, as they are stored as a single file on the computer.

As mentioned previously, flat-file databases are stored as a file on the disk of a computer. Usually this would not be a problem for a webapp, but what happens if the `database is stored underneath the root directory of the website (i.e. one of the files that a user connecting to the website is able to access)?`
Well, we can `download` it and `query` it on our own machine, with `full access` to everything in the database. ***Sensitive Data Exposure*** indeed!


The most common (and simplest) format of `flat-file database` is an `sqlite database`.

This client is called `"sqlite3"`, and is installed by default on Kali.


Task12:  [Severity 4] XML External Entity
-------------------------------------------

An **`XML External Entity (XXE) attack`** is a vulnerability that **abuses** `features of XML parsers/data`.It often allows an attacker to interact with any `backend` or `external systems` that the application itself can access and can allow the attacker to `read the file on that system`. They can also cause `Denial of Service (DoS) attack` or could use `XXE` to perform `Server-Side Request Forgery (SSRF)` inducing the `web application to make requests to other applications`. XXE may even `enable port scanning` and lead to `remote code execution`.


There are two types of XXE attacks:

1. `in-band`
2. `out-of-band (OOB-XXE) or Blind XXE`

1) An **`in-band XXE attack`** is the one in which the attacker can **`receive an immediate response to the XXE payload`**.

2) An **`out-of-band XXE attacks (also called blind XXE)`** is the one which produces **`no immediate response from the web application`** and attacker `has to reflect the output of their XXE payload to some other file or their own server`.


Task13:  [Severity 4 XML External Entity - eXtensible Markup Language
----------------------------------------------------------------------

##### What is XML?
XML (eXtensible Markup Language) is a markup language that defines a set of rules for encoding documents in a format that is both human-readable and machine-readable. It is a markup language used for `storing and transporting data`.


##### Why we use XML?

1. XML is platform-independent and programming language independent, thus it can be used on **`any system and supports the technology change when that happens`**.

2. The data stored and transported using XML can be changed at any point in time without affecting the data presentation.

3. XML allows validation using **DTD** and **Schema**. This validation ensures that the XML document is _free from any syntax error_.

4. XML simplifies data sharing between various systems because of its platform-independent nature. XML data doesn’t require any conversion when transferred between different systems.


Starting XML line: XML Prolog => `<?xml version="1.0" encoding="UTF-8"?>`



Task17: [Severity 5] Broken Access Control
-------------------------------------------

A regular visitor being able to access protected pages, can lead to the following:
	- Being able to view sensitive information
	- Accessing unauthorized functionality



Task19:  [Severity 6] Security Misconfiguration
-------------------------------------------------


- Poorly configured permissions on cloud services, like S3 buckets
- Having unnecessary features enabled, like services, pages, accounts or privileges
- Default accounts with unchanged passwords
- Error messages that are overly detailed and allow an attacker to find out more about the system
- Not using HTTP security headers, or revealing too much detail in the Server: HTTP header


Task20:  [Severity 7] Cross-site Scripting
------------------------------------------

A web application is vulnerable to XSS if it uses `unsanitized user input`. XSS is possible in _Javascript_, _VBScript_, _Flash_ and _CSS_.

There are _three main types_ of cross-site scripting:

1. **Stored XSS**

- The most dangerous type of XSS.
- This is where a _malicious string originates_ from the website’s database. This often happens when a website allows user input that is _not sanitised_ (remove the "bad parts" of a users input) when inserted into the database.

2. **Reflected XSS**

- The malicious payload is part of the victims request to the website.
- The website includes this payload in response back to the user.
- To summarise, an attacker needs to trick a victim into clicking a URL to execute their malicious payload.

3. **DOM-Based XSS**

- DOM stands for `Document Object Model` and is a _programming interface for HTML and XML documents_.
- It represents the page so that programs can change the document structure, style and content.
- A web page is a document and this document can be either displayed in the browser window or as the HTML source.

- For more XSS explanations and exercises, check out the XSS room - **Cross-site Scripting** (`Present in this directory`).


1. Navigate to http://10.10.60.85/ in your browser and click on the "Reflected XSS" tab on the navbar; craft a reflected XSS payload that will cause a popup saying "Hello".

```javascript
<script>alert("Hello")</script>
```

--> ThereIsMoreToXSSThanYouThink

2. On the same reflective page, craft a reflected XSS payload that will cause a popup with your machines IP address.

```javascript
<script>alert(window.location.hostname)</script>
```

--> ReflectiveXss4TheWin



Task21:  [Severity 8] Insecure Deserialization
------------------------------------------------

**Insecure Deserialization** is a vulnerability which occurs when _untrusted data is used to abuse the logic of an application_.

Simply put, _insecure deserialization_ is `replacing data processed by an application with malicious code`

=> Allowing anything from `DoS (Denial of Service)` to `RCE (Remote Code Execution)` that the attacker can use to gain a foothold in a pentesting scenario.



Task25:  [Severity 8] Insecure Deserialization - Cookies Practical
-------------------------------------------------------------------

1. 1st flag (cookie value)

sessionid = cookie
```
gAN9cQAoWAkAAABzZXNzaW9uSWRxAVggAAAAN2MzZjdlMzVhYzJjNDgwNmFmNTc4OGQ0YzBjMzQ5Y2RxAlgLAAAAZW5jb2RlZGZsYWdxA1gYAAAAVEhNe2dvb2Rfb2xkX2Jhc2U2NF9odWh9cQR1Lg==

$ echo gAN9cQAoWAkAAABzZXNzaW9uSWRxAVggAAAAN2MzZjdlMzVhYzJjNDgwNmFmNTc4OGQ0YzBjMzQ5Y2RxAlgLAAAAZW5jb2RlZGZsYWdxA1gYAAAAVEhNe2dvb2Rfb2xkX2Jhc2U2NF9odWh9cQR1Lg== | base64 -d
```

--> `THM{good_old_base64_huh}`


Task27:  [Severity 9] Components With Known Vulnerabilities - Intro
--------------------------------------------------------------------

let's say that a company hasn't updated their version of WordPress for a few years, and using a tool such as wpscan, you find that it's version 4.6. Some quick research will reveal that WordPress 4.6 is vulnerable to an unauthenticated remote code execution(RCE) exploit, and even better you can find an exploit already made on exploit-db.



Task30:  [Severity 10] Insufficient Logging and Monitoring
-----------------------------------------------------------



