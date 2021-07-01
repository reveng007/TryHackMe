
Add this:

`echo "10.10.170.88    overwrite.uploadvulns.thm shell.uploadvulns.thm java.uploadvulns.thm annex.uploadvulns.thm magic.uploadvulns.thm jewel.uploadvulns.thm" | sudo tee -a /etc/hosts`

For different virtual hosting...

Task2: Introduction
--------------------

The ability to upload files to a server has become an integral part of how we interact with web applications. Be it a profile picture for a social media website, a report being uploaded to cloud storage, or saving a project on Github; the applications for file upload features are limitless.

File uploads can also open up severe vulnerabilities in the server:

1. lead to anything from relatively minor, nuisance problems.

2. All the way up to full Remote Code Execution (RCE) if an attacker manages to upload and execute a shell.

With unrestricted upload access to a server (and the ability to retrieve data at will), an attacker could deface or otherwise alter existing content -- up to and including injecting malicious webpages, which lead to further vulnerabilities such as XSS or CSRF. By uploading arbitrary files, an attacker could potentially also use the server to host and/or serve illegal content, or to leak sensitive information. Realistically speaking, an attacker with the ability to upload a file of their choice to your server -- with no restrictions -- is very dangerous indeed.


The purpose of this room is to explore some of the vulnerabilities resulting from improper (or inadequate) handling of file uploads. Specifically, we will be looking at:

- Overwriting existing files on a server
- Uploading and Executing Shells on a server
- Bypassing Client-Side filtering
- Bypassing various kinds of Server-Side filtering
- Fooling content type validation checks



Task3: General Methodology
---------------------------

`So, we have a file upload point on a site. How would we go about exploiting it?`

--> As with any kind of hacking, enumeration is key.

- Looking at the source code for the page is good to see if any kind of client-side filtering is being applied.

- Scanning with a directory bruteforcer such as Gobuster is usually helpful in web attacks, and may reveal where files are being uploaded to.

- Intercepting upload requests with [Burpsuite](https://blog.tryhackme.com/setting-up-burp/) will also come in handy.

Browser extensions such as [Wappalyser](https://www.wappalyzer.com/download) can provide valuable information at a glance about the site you're targetting.


Task4: Overwriting Existing Files
----------------------------------

When files are uploaded to the server, a range of checks should be carried out to ensure that the file will not overwrite anything which already exists on the server. Common practice is to assign the file with a new name -- often either random, or with the date and time of upload added to the start or end of the original filename. Alternatively, checks may be applied to see if the filename already exists on the server; if a file with the same name already exists then the server will return an error message asking the user to pick a different file name. File permissions also come into play when protecting existing files from being overwritten. Web pages, for example, should not be writeable to the web user, thus preventing them from being overwritten with a malicious version uploaded by an attacker.


----------------
You may need to enumerate more than this for a real challenge; however, in this instance, let's just take a look at the source code of the page:

Inside the red box, we see the code that's responsible for displaying the image that we saw on the page. It's being sourced from a file called "spaniel.jpg", inside a directory called "images".

Now we know where the image is being pulled from -- can we overwrite it?

Let's download another image from the internet and call it `spaniel.jpg`. We'll then upload it to the site and see if we can overwrite the existing image:
-----------------

[Basically we have to upload another of same name to suffice the our job, here]


Open your web browser and navigate to `overwrite.uploadvulns.thm`. Your goal is to overwrite a file on the server with an upload of your own.


1. What is the name of the image file which can be overwritten?

--> mountains.jpg   [I have to see the name of the background image from source code of the page]

2. Overwrite the image. What is the flag you receive?

--> THM{OTBiODQ3YmNjYWZhM2UyMmYzZDNiZjI5}


Task5:  Remote Code Execution
-------------------------------

It's all well and good overwriting files that exist on the server. That's a nuisance to the person maintaining the site, and may lead to some vulnerabilities, but let's go further; let's go for RCE!

Remote Code Execution (as the name suggests) would allow us to execute code arbitrarily on the web server. Whilst this is likely to be as a low-privileged web user account (such as `www-data` on Linux servers), it's still an extremely serious vulnerability.

Remote code execution through a web application tends to be a result of uploading a program written in the **same language as the back-end of the website** (or another language which the **server understands and will execute**). Traditionally this would be **PHP**, however, in more recent times, other back-end languages have become more common (**Python Django** and **Javascript in the form of Node.js** being prime examples).


There are two basic ways to achieve RCE on a webserver:

1. webshells
2. reverse shells


S1 => Scan for directories in website

S2 => We'll try uploading a legitimate image file first. Here I am choosing our cute dog photo from the previous task. Now, if we go to http://demo.uploadvulns.thm/uploads we should see that the spaniel picture has been uploaded! Ok, we can upload images. Let's try a webshell now.

A simple webshell works by taking a parameter and executing it as a system command. In PHP, the syntax for this would be:

```php
<?php
    echo system($_GET["cmd"]);
?>
```
This code takes a GET parameter and executes it as a system command. It then echoes the output out to the screen.


S3 => Now, operate: `http:url/uploads/webshell.php?cmd=id;whoami;ls`

OR, 

Use good old reverse shell
and nc listener listening

S4 => Execute the php reverse shell


Navigate to shell.uploadvulns.thm and complete the questions for this task.


1. Run a Gobuster scan on the website using the syntax from the screenshot above. What directory looks like it might be used for uploads?

--> /resources

2. Get either a web shell or a reverse shell on the machine.
What's the flag in the /var/www/ directory of the server?

-->  THM{YWFhY2U3ZGI4N2QxNmQzZjk0YjgzZDZk}


Task6:  Filtering
-----------------

Up until now we have largely been ignoring the counter-defences employed by web developers to defend against file upload vulnerabilities. Every website that you've successfully attacked so far in this room has been completely insecure.

It's time that changed.

From here on out, we'll be looking at some of the defence mechanisms used to prevent malicious file uploads, and how to circumvent them.


#### 1. "Client-Side" (in the context of web applications)


It means that it is running in the user's browser as opposed to on the web server itself.

##### NOTE:
JavaScript is pretty much ubiquitous as the client-side scripting language, although alternatives do exist. 

Regardless of the language being used, a client-side script will be run in your web browser.

_In the context of file-uploads, this means that the filtering occurs before the file is even uploaded to the server_.


> Theoretically, this would seem like a good thing, right? In an ideal world, it would be; however, because the filtering is happening on our computer, it is _trivially easy to bypass_. As such client-side filtering by itself is a highly insecure method of verifying that an uploaded file is not malicious.


#### 2. "Server-Side" (in the context of web application)

A server-side script will be run on the server.

##### NOTE:
Traditionally PHP was the predominant server-side language (with Microsoft's ASP for IIS coming in close second).
However, in recent years, other options (C#, Node.js, Python, Ruby on Rails, and a variety of others) have become more widely used.


> Server-side filtering tends to be more difficult to bypass, as you don't have the code in front of you. As the code is executed on the server, in most cases it will also be `impossible to bypass the filter completely`; _instead we have to form a payload which conforms to the filters in place, but still allows us to execute our code_.



#### With that in mind, let's take a look at some different kinds of filtering.

Extension Validation:
----------------------

Filters that check for extensions work in one of two ways.

They either blacklist extensions (i.e. have a list of extensions which are not allowed) or they whitelist extensions (i.e. have a list of extensions which are allowed, and reject everything else).


File Type Filtering:
--------------------

Similar to Extension validation, but more intensive, file type filtering looks, once again, to verify that the contents of a file are acceptable to upload.

We'll be looking at two types of file type validation:


- MIME validation: MIME (`Multipurpose Internet Mail Extension`) types are used as an identifier for files -- originally when transfered as attachments over email, but now also when files are being transferred over HTTP(S).

The MIME type for a file upload is attached in the header of the request, and looks something like this:

![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/06.Upload%20Vulnerabilities/MIME.png?raw=true)


MIME types follow the format `<type>/<subtype>`.

In the request above, you can see that the image "spaniel.jpg" was uploaded to the server. As a legitimate JPEG image, the MIME type for this upload was "image/jpeg".
The MIME type for a file can be checked client-side and/or server-side; however, as MIME is based on the extension of the file, this is extremely easy to bypass.


- Magic Number validation


File Length Filtering:
-----------------------

> File length filters are used to prevent huge files from being uploaded to the server via an upload form (as this can potentially starve the server of resources). In most cases this will not cause us any issues when we upload shells; however, it's worth bearing in mind that if an upload form only expects a very small file to be uploaded, there may be a length filter in place to ensure that the file length requirement is adhered to. As an example, our fully fledged PHP reverse shell from the previous task is 5.4Kb big -- relatively tiny, but if the form expects a maximum of 2Kb then we would need to find an alternative shell to upload.


File Name Filtering:
---------------------

> As touched upon previously, files uploaded to a server should be unique. Usually this would mean adding a random aspect to the file name, however, an alternative strategy would be to check if a file with the same name already exists on the server, and give the user an error if so. Additionally, file names should be sanitised on upload to ensure that they don't contain any "bad characters", which could potentially cause problems on the file system when uploaded (e.g. null bytes or forward slashes on Linux, as well as control characters such as ; and potentially unicode characters).

What this means for us is that:

> On a well administered system, our uploaded files are unlikely to have the same name we gave them before uploading, so be aware that you may have to go hunting for your shell in the event that you manage to bypass the content filtering.


File Content Filtering:
-----------------------

More complicated filtering systems may scan the full contents of an uploaded file to ensure that it's not spoofing its extension, MIME type and Magic Number. This is a significantly more complex process than the majority of basic filtration systems employ, and thus will not be covered in this room.

##### NOTE:

It's worth noting that **none** of these filters are ***perfect*** by themselves -- they will usually be used in ***conjunction with each other***, providing a `multi-layered filter`, thus increasing the security of the upload significantly. Any of these filters can all be applied client-side, server-side, or both.


Similarly, different frameworks and languages come with their own inherent methods of filtering and validating uploaded files. As a result, it is possible for language specific exploits to appear; for example, until PHP major version five, it was possible to bypass an extension filter by appending a null byte, followed by a valid extension, to the malicious `.php` file. More recently it was also possible to inject PHP code into the exif data of an otherwise valid image file, then force the server to execute it. These are things that you are welcome to research further, should you be interested.


1. What is the traditionally predominant server-side scripting language?

--> php

2. When validating by file extension, what would you call a list of accepted extensions (whereby the server rejects any extension not in the list)?

--> whitelist

3. **[Research]** What MIME type would you expect to see when uploading a CSV file?

--> text/csv


Task7:  Bypassing Client-Side Filtering
----------------------------------------

We'll begin with the first (and weakest) line of defence: Client-Side Filtering.

As mentioned previously, client-side filtering tends to be extremely easy to bypass, as it occurs entirely on a machine that you control. When you have access to the code, it's very easy to alter it.

1. <ins>Turn off Javascript in your browser</ins>

This will work provided the site doesn't require Javascript in order to provide basic functionality. If turning off Javascript completely will prevent the site from working at all then one of the other methods would be more desirable; otherwise, this can be an effective way of completely bypassing the client-side filter.

2. <ins>Intercept and modify the incoming page</ins>

Using Burpsuite, we can intercept the incoming web page and strip out the Javascript filter before it has a chance to run. The process for this will be covered below.

3. <ins>Intercept and modify the file upload</ins>

Where the previous method works before the webpage is loaded, this method allows the web page to load as normal, but intercepts the file upload after it's already passed (and been accepted by the filter). Again, we will cover the process for using this method in the course of the task.

4. <ins>Send the file directly to the upload point</ins>

Why use the webpage with the filter, when you can send the file directly using a tool like `curl`? 
Posting the data directly to the page which contains the code for handling the file upload is another effective method for completely bypassing a client side filter.
`We will not be covering this method in any real depth in this tutorial`, however, the syntax for such a command would look something like this: 
`curl -X POST -F "submit:<value>" -F "<file-parameter>:@<path-to-file>" <site>`.

To use this method you would first aim to intercept a successful upload (using Burpsuite or the browser console) to see the parameters being used in the upload, which can then be slotted into the above command.


We will be covering methods two and three in depth below.
-------------------


Let's assume that, once again, we have found an upload page on a website:

As always, we'll take a look at the source code. Here we see a basic Javascript function checking for the MIME type of uploaded files:

![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/06.Upload%20Vulnerabilities/pic1.png?raw=true)

In this instance we can see that the filter is using a whitelist to exclude any MIME type that isn't `image/jpeg`.


Our next step is to attempt a file upload -- as expected, if we choose a JPEG, the function accepts it. Anything else and the upload is rejected.


let's start Burpsuite


![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/06.Upload%20Vulnerabilities/pic2.png?raw=true)

When we click the "Forward" button at the top of the window, we will then see the server's response to our request. Here we can delete, comment out, or otherwise break the Javascript function before it has a chance to load:

![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/06.Upload%20Vulnerabilities/pic3.png?raw=true)


Having deleted the function, we once again click "Forward" until the site has finished loading, and are now free to upload any kind of file to the website:


![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/06.Upload%20Vulnerabilities/pic4.png?raw=true)


It's worth noting here that Burpsuite will not, by default, intercept any external Javascript files that the web page is loading. If you need to edit a script which is not inside the main page being loaded, you'll need to go to the "Options" tab at the top of the Burpsuite window, then under the "Intercept Client Requests" section, edit the condition of the first line to remove `^js$|`:


![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/06.Upload%20Vulnerabilities/pic5.png?raw=true)


We've already bypassed this filter by intercepting and removing it prior to the page being loaded, but let's try doing it by uploading a file with a legitimate extension and MIME type, then intercepting and correcting the upload with Burpsuite.

Having reloaded the webpage to put the filter back in place, let's take the reverse shell that we used before and rename it to be called "shell.jpg". As the MIME type (based on the file extension) automatically checks out, the Client-Side filter lets our payload through without complaining:

![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/06.Upload%20Vulnerabilities/pic6.png?raw=true)


Once again we'll activate our Burpsuite intercept, then click "Upload" and catch the request:

![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/06.Upload%20Vulnerabilities/pic7.png?raw=true)


Observe that the MIME type of our PHP shell is currently `image/jpeg`. We'll change this to `text/x-php`, and the file extension from `.jpg` to `.php`, then forward the request to the server:


![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/06.Upload%20Vulnerabilities/pic8.png?raw=true)


Now, when we navigate to `http://demo.uploadvulns.thm/uploads/shell.php` having set up a netcat listener, we receive a connection from the shell!


![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/06.Upload%20Vulnerabilities/pic9.png?raw=true)


We've covered in detail two ways to bypass a Client-Side file upload filter. Now it's time for you to give it a shot for yourself! Navigate to `java.uploadvulns.thm` and bypass the filter to get a reverse shell. Remember that not all client-side scripts are inline! As mentioned previously, Gobuster would be a very good place to start here -- the upload directory name will be changing with every new challenge.


1. What is the flag in /var/www/?

--> THM{NDllZDQxNjJjOTE0YWNhZGY3YjljNmE2}


Task8:  Bypassing Server-Side Filtering: File Extensions
--------------------------------------------------------



