Task1: Intro
------------

Burp Suite, a framework of web application pentesting tools, is widely regarded as the de facto tool to use when performing web app testing. Throughout this room, we'll take a look at the basics of installing and using this tool as well as it's various major components. Reference links to the associated documentation per section have been provided at the bottom of most tasks throughout this room.

Task3: Gettin'[CA] Certified
-----------------------------

Before we can start using our new installation (or preinstalled) Burp Suite, we'll have to fix a certificate warning. We need to install a CA certificate as BurpSuite acts as a proxy between your browser and sending it through the internet - It allows the BurpSuite Application to read and send on HTTPS data.

A certificate warning that will appear unless we install Burp's CA Certificate.

**One quick note, in this lab I'll be using Firefox and Foxy Proxy** (which you can find here). I use Firefox in this instance as it's a little bit easier to work with when using Burp Suite. 


#### NOTE:

> Chromium web browser (which comes embedded with burp) are preconfigured, we don't have to make any further more settings to it. Just Nothing...!!


1. Launch Burp!

Once you've launched Burp, you'll be greeted with the following screen:

Once this pops-up, click 'Temporary project' and then 'Next'.

* Now as you likely noticed both 'New project on disk' and 'Open existing project' are both grayed out. As annotated at the top of this window saving projects is a feature associated with Burp Suite Professional as it's pretty common to save and come back to a multi-day web application test.

Next, we'll be prompted to ask for what configuration we'd like to use. For now, select 'Use Burp defaults'.

This option is included as it can be incredibly useful to create a custom configuration file for your proxy or other settings, especially depending on how your network configuration and/or if Burp Suite is being launched remotely such as via [x11 forwarding](https://www.youtube.com/watch?v=auePeI8vZA8).

Finally, let's go ahead and Start Burp! Click 'Start Burp' now!

Since we now have Burp Suite running, the proxy service will have started by default with it. In order to fully leverage this proxy, we'll have to install the CA certificate included with Burp Suite (otherwise we won't be able to load anything with SSL). To do this, let's launch Firefox now!

Now that we've started Burp, let's add an extension to our web browser to allow up to easily route or traffic through it! For this room, we'll be using 'FoxyProxy Standard' on Firefox.

Next, we'll move onto adding the certificate for Burp!

With Firefox, navigate to the following address: http://localhost:8080

Click on 'CA Certificate' in the top right to download and save the CA Certificate.

Now that we've downloaded the CA Certificate, move over to the settings menu in Firefox. Search for 'Certificates' in the search bar.

Click on 'View Certificates'

Next, in the Authorities tab click on 'Import'

Navigate to where you saved the CA Certificate we downloaded previously. Click 'OK' once you've selected this certificate.

Task4: Overview of Features
----------------------------

Here's a quick overview of each section covered:

1. **Proxy** - What allows us to funnel traffic through Burp Suite for further analysis
2. **Target** - How we _`set the scope of our project`_. We can also use this to effectively create a site map of the application we are testing.
3. **Intruder** - Incredibly powerful tool for everything from _`field fuzzing to credential stuffing and more`_.
4. **Repeater** - Allows us to _`'repeat'`_ requests that have previously been made with or without modification. Often used in a precursor step to fuzzing with the aforementioned Intruder.
5. **Sequencer** - Analyzes the _`'randomness'`_ present in parts of the web app which are intended to be unpredictable. This is commonly used for testing session cookies.
6. **Decoder** - As the name suggests, Decoder is a tool that allows us to perform various transforms on pieces of data. These transforms vary from decoding/encoding to various bases or URL encoding.
7. **Comparer** - Comparer as you might have guessed is a tool we can use to _`compare different responses or other pieces of data such as site maps or proxy histories`_ (awesome for access control issue testing). This is very similar to the Linux tool diff.
8. **Extender** - Similar to adding mods to a game like Minecraft, Extender allows us to _`add components such as tool integrations, additional scan definitions, and more`_!
9. **Scanner** - Automated web vulnerability scanner that can highlight areas of the application for further manual investigation or possible exploitation with another section of Burp. This feature, while not in the community edition of Burp Suite, is still a key facet of performing a web application test.


1. Which tool in Burp Suite can we use to perform a 'diff' on responses and other pieces of data?

--> comparer

2. What tool could we use to analyze randomness in different pieces of data such as password reset tokens?

--> sequencer

3. Which tool can we use to set the scope of our project?

--> target

4. While only available in the premium versions of Burp Suite, which tool can we use to automatically identify different vulnerabilities in the application we are examining?

--> scanner

5. Encoding or decoding data can be particularly useful when examining URL parameters or protections on a form, which tool allows us to do just that?

--> decoder

6. Which tool allows us to redirect our web traffic into Burp for further examination?

--> proxy

7. Simple in concept but powerful in execution, which tool allows us to reissue requests?

--> repeater

8. With four modes, which tool in Burp can we use for a variety of purposes such as field fuzzing?

--> intruder

9. Last but certainly not least, which tool allows us to modify Burp Suite via the addition of extensions?

--> extender


Task5: Engage Dark Mode
------------------------

Task6: Proxy
-------------

1. By default, the Burp Suite proxy listens on only one interface. What is it? Use the format of IP:PORT

--> 127.0.0.1:8080

2. Return to your web browser and navigate to the web application hosted on the VM we deployed just a bit ago. Note that the page appears to be continuously loading. Change back to Burp Suite, we now have a request that's waiting in our intercept tab. Take a look at the actions, which shortcut allows us to forward the request to Repeater?

--> ctrl-R

3. How about if we wanted to forward our request to Intruder?

--> ctrl-I

4. Burp Suite saves the history of requests sent through the proxy along with their varying details. This can be especially useful when we need to have proof of our actions throughout a penetration test or we want to modify and resend a request we sent a while back. What is the name of the first section wherein general web requests (GET/POST) are saved?

--> HTTP history

5. Defined in RFC 6455 as a low-latency communication protocol that doesn't require HTTP encapsulation, what is the name of the second section of our saved history in Burp Suite? These are commonly used in collaborate application which require real-time updates (Google Docs is an excellent example here).

--> WebSockets history

6. Before we move onto exploring our target definition, let's take a look at some of the advanced customization we can utilize in the Burp proxy. Move over to the Options section of the Proxy tab and scroll down to Intercept Client Requests. Here we can apply further fine-grained rules to define which requests we would like to intercept. Perhaps the most useful out of the default rules is our only AND rule. What is it's match type?

--> URL

7. How about it's 'Relationship'? In this situation, enabling this match rule can be incredibly useful following target definition as we can effectively leave intercept on permanently (unless we need to navigate without intercept) as it won't disturb sites which are outside of our scope - something which is particularly nice if we need to Google something in the same browser.

--> Is in target scope


Task7: Target Definition
-------------------------

Perhaps the most important feature in Burp Suite, we'll now be turning our focus to the Target tab!
------------------
When starting a web application test you'll very likely be provided a few things:

- The application URL (hopefully for dev/test and not prod)
- A list of the different user roles within the application
- Various test accounts and associated credentials for those accounts
- A list of pieces/forms in the application which are out-of-scope for testing and should be avoided

----------------

1. From this information, we can now start to build our scope within Burp, something which is incredibly important in the case we are planning on performing any automated testing.
2. Typically this is done in a `tiered approach` wherein we work our way up from 

	- the **lowest privileged account (this includes unauthenticated access)**, **browsing the site as a normal user would**. Browsing like this to discover the _full extent of the site_ is commonly referenced as the **'happy path'**.

-------------------

Following the creation of a site map via browsing the **`happy path`**, we can go through and start removing various items from the scope. These items typically fit one of these criteria:

- The item (page, form, etc) has been designated as out of scope in the provided documentation from the client
- **`Automated exploitation of the item (especially in a credentialed manner)`** would cause a **`huge mess`** (like sending hundreds of password reset emails - If you've done a web app professionally you've probably done this at one point)
- **`Automated exploitation of the item (especially in a credentialed manner)`** would lead to damaging and potentially crashing the web app

##### Once we've removed any restricted or otherwise potentially dangerous items from our scope, we can move onto other areas of testing with the various tools within Burp Suite.


1. Before leaving the Proxy tab, switch Intercept to disabled. We'll still see the pages we navigate to in our history and the target tab, just having Intercept constantly stopping our requests for this next bit will get old fast.

2. Navigate to the Target tab in Burp. In our last task, Proxy, we browsed to the website on our target machine (in this case OWASP Juice Shop). Find our target site in this list and right-click on it. Select 'Add to scope'. 

3. Clicking 'Add to scope' will trigger a pop-up. This will stop Burp from sending out-of-scope items to our site map.

4. Select 'Yes' to close the popup.

5. Browse around the rest of the application to build out our page structure in the target tab. Once you've visited most of the pages of the site return to Burp Suite and expand the various levels of the application directory. What do we call this representation of the collective web application?

--> site map

6. What is the term for browsing the application as a normal user prior to examining it further?

--> happy path

7. One last thing before moving on. Within the target tab, you may have noticed a sub-tab for issue definitions. Click into that now.

8. The issue definitions found here are how Burp Suite defines issues within reporting. While getting started, these issue definitions can be particularly helpful for understanding and categorizing various findings we might have. Which poisoning issue arises when an application behind a cache process input that is not included in the cache key?

--> web cache poisoning


Task8: Puttin' it on Repeat[er]
--------------------------------

As the name suggests, Repeater allows us to repeat requests we've already made. These requests can either be reissued as-is or with modifications. In contrast to Intruder, Repeater is typically used for the purposes of experimentation or more fine-tuned exploitation wherein automation may not be desired. We'll be checking out Repeater with the goal of finding a proof of concept demonstrating that Juice Shop is vulnerable to SQL injection.

1. To start, click 'Account' (this might be 'Login' depending on the version of Juice Shop) in the top right corner of Juice Shop in order to navigate to the login page.

2. Try logging in with invalid credentials. What error is generated when login fails?

--> Invalid email or password.

3. But wait, didn't we want to send that request to Repeater? Even though we didn't send it to Repeater initially via intercept, we can still find the request in our history. Switch over to the HTTP sub-tab of Proxy. Look through these requests until you find our failed login attempt. **`Right-click on this request and send it to Repeater and then send it to Intruder, too!`**

[Basically, We sent a **`POST request`** when we attempted to ***login***. There should only be a few post requests in your Burp history.]

4. Now that we've sent the request to Repeater, let's try adjusting the request such that we are sending a single quote (') as both the email and password. What error is generated from this request?

![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/03.Burp%20Suite/Burp_view_1.png?raw=true)

--> `SQLITE_ERROR`

5. Now that we've leveraged Repeater to gain proof of concept that Juice Shop's login is vulnerable to SQLi, let's try something a little more mischievous and attempt to leave a devastating zero-star review. First, click on the drawer button in the top-left of the application. **`If this isn't present for you, just skip to the next question`**.

6. Next, click on 'Customer Feedback' (depending on the version of Juice Shop this also might be along the top of the page next to 'Login' under 'Contact Us')

7. With the Burp proxy on submit feedback. Once this is done, find the POST request in your HTTP History in Burp and send it to Repeater.

8. What field do we have to modify in order to submit a zero-star review?

--> rating

9. Submit a zero-star review and complete this challenge in Juice Shop!


Task9: Help! There's an Intruder!
---------------------------------

Arguably the `most powerful tool in Burp Suite`, **`Intruder`** can be used for many things ranging from ***fuzzing to brute-forcing***.
At its core, Intruder serves one purpose: **automation**. 

####	**Repeater**	      |		**Intruder**
 			      |
While Repeater best handles   | Intruder is meant for _repeat_ testing
_experimentation or one-off_  | once a _proof of concept_ has been
_testing_.		      | established.


As per the [Burp Suite documentation](https://portswigger.net/burp/documentation/desktop/tools/intruder/using), some common uses are as follows:

- Enumerating identifiers such as `usernames`, `cycling through predictable session/password recovery tokens`, and `attempting simple password guessing`
- `Harvesting useful data` from `user profiles` or other pages of interest via grepping our responses
- `Fuzzing for vulnerabilities` such as `SQL injection`, `cross-site scripting (XSS)`, and `file path traversal`.

##### To accomplish these various use cases, Intruder has four different attack types:

1. Sniper:
The most popular attack type, this cycles through our selected positions, putting the next available payload (item from our wordlist) in each position in turn. This uses only one set of payloads (one wordlist).

2. Battering Ram:
Similar to Sniper, Battering Ram uses **`only one set of payloads`**. Unlike Sniper, Battering Ram puts every payload into every selected position. Think about how a battering ram makes contact across a large surface with a single surface, hence the name battering ram for this attack type.

3. Pitchfork:
The Pitchfork attack type allows us to use **`multiple payload sets (one per position selected) and iterate through both payload sets simultaneously`**. For example, if we selected two positions (say a username field and a password field), we can provide a username and password payload list. Intruder will then cycle through the combinations of usernames and passwords, resulting in a total number of combinations equalling the smallest payload set provided. 

4. Cluster Bomb:
The Cluster Bomb attack type allows us to use **`multiple payload sets (one per position selected) and iterate through all combinations of the payload lists we provide`**. For example, if we selected two positions (say a username field and a password field), we can provide a username and password payload list. Intruder will then cycle through the combinations of usernames and passwords, resulting in a total number of combinations equalling usernames x passwords. Do note, this can get pretty lengthy if you are using the community edition of Burp. 



1. Which attack type allows us to select multiple payload sets (one per position) and iterate through them simultaneously?

--> Pitchfork

2. How about the attack type which allows us to use one payload set in every single position we've selected simultaneously?

--> Battering Ram

3. Which attack type allows us to select multiple payload sets (one per position) and iterate through all possible combinations?

--> Cluster Bomb

4. Perhaps the most commonly used, which attack type allows us to cycle through our payload set, putting the next available payload in each position in turn?

--> Sniper

5. Download the wordlist attached to this room, this is a shortened version of the [fuzzdb SQLi platform detection list](https://github.com/fuzzdb-project/fuzzdb/blob/master/attack/sql-injection/detect/xplatform.txt)

Return to the Intruder in Burp. In our previous task, we passed our failed login attempt to both Repeater and Intruder for further examination. Open up the Positions sub-tab in the Intruder tab with this request now and verify that 'Sniper' is selected as our attack type.


Burp attempts to automatically highlight possible fields of interest for Intruder, however, it doesn't have it quite right for what we'll be looking at in this instance. Hit 'Clear' on the right-hand side to clear all selected fields.


Next, let's highlight the email field between the double quotes ("). This will be whatever you entered in the email field for our previous failed login attempt.

Now click 'Add' to select our email field as a position for our payloads.

Next, let's switch to the payloads sub-tab of Intruder. Once there, hit 'Load' and select the wordlist you previously downloaded in question five that is attached to this task.

Almost there! Scroll down and uncheck 'URL-encode these characters'. We don't want to have the characters sent in our payloads to be encoded as they otherwise won't be recognized by SQL.

6. Finally, click 'Start attack'. What is the first payload that returns a 200 status code, showing that we have successfully bypassed authentication?

--> a' or 1=1--


Task10: As it turns out the machines are better at math than us
----------------------------------------------------------------

While not as commonly used in a practice environment, Sequencer represents a core tool in a proper web application pentest. Burp's Sequencer, per the Burp documentation, is a tool for analyzing the quality of randomness in an application's sessions tokens and other important data items that are otherwise intended to be unpredictable.

Some commonly analyzed items include:

- Session tokens
- Anti-CSRF (Cross-Site Request Forgery) tokens
- Password reset tokens (sent with password resets that in theory uniquely tie users with their password reset requests)


1. Switch over to the HTTP history sub-tab of Proxy. 

2. We're going to dig for a response which issues a cookie. Parse through the various responses we've received from Juice Shop until you find one that includes a 'Set-Cookie' header. 

3. Once you've found a request response that issues a cookie, right-click on the request and select 'Send to Sequencer'.

4. Change over Sequencer and select 'Start live capture'

5. Let Sequencer run and collect ~10,000 requests. Once it hits roughly that amount hit 'Pause' and then 'Analyze now'

6. Parse through the results. What is the effective estimated entropy measured in?

--> bits

7. In order to find the usable bits of entropy we often have to make some adjustments to have a normalized dataset. What item is converted in this process?

--> token

Read through the remaining results of the token analysis


Task11: Decoder and Comparer
-----------------------------


Decoder and Comparer, while lesser tools within Burp Suite, are still essential to understand and leverage as part of being a proficient web app tester. 

As the name suggests, Decoder is a tool that allows us to perform various transforms on pieces of data. These transforms vary from decoding/encoding to various bases or URL encoding. We chain these transforms together and Decoder will automatically spawn an additional tier each time we select a decoder, encoder, or hash.

This tool ultimately functions very similarly to CyberChef, albeit slightly less powerful.

Similarly, Comparer, as you might have guessed is a tool we can use to compare different responses or other pieces of data such as site maps or proxy histories (awesome for access control issue testing). This is very similar to the Linux tool diff.

------------------------
- When looking for username enumeration conditions, you can compare responses to failed logins using valid and invalid usernames, looking for subtle differences in responses. This is also sometimes useful for when enumerating password recovery forms or another similar recovery/account access mechanism. 

- When an Intruder attack has resulted in some very large responses with different lengths than the base response, you can compare these to quickly see where the differences lie.

- When comparing the site maps or Proxy history entries generated by different types of users, you can compare pairs of similar requests to see where the differences lie that give rise to different application behavior. This may reveal possible access control issues in the application wherein lower privileged users can access pages they really shouldn't be able to.

- When testing for blind SQL injection bugs using Boolean condition injection and other similar tests, you can compare two responses to see whether injecting different conditions has resulted in a relevant difference in responses.


1. Let's first take a look at decoder by revisiting an old friend. Previously we discovered the scoreboard within the site JavaScript. Return to our target tab and find the API endpoint highlighted in the following request:

![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/03.Burp%20Suite/Burp_view_2.png?raw=true)

2. Copy the first line of that request and paste it into Decoder. Next, select 'Decode as ...' URL

![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/03.Burp%20Suite/Burp_view_3.png?raw=true)

3. What character does the %20 in the request we copied into Decoder decode as?

--> space

4. Similar to CyberChef, Decoder also has a 'Magic' mode where it will automatically attempt to decode the input it is provided. What is this mode called? 

--> Smart decode

5. What can we load into Comparer to see differences in what various user roles can access? This is very useful to check for access control issues.

--> site maps

6. 
Comparer can perform a diff against two different metrics, which one allows us to examine the data loaded in as-is rather than breaking it down into bytes?

--> Words


Task12: Installing some Mods [Extender]
----------------------------------------

 Here are some of the most popular extensions I suggest checking out (not all of these are free but I suggest looking into them all the same):

- [Logger++](https://portswigger.net/bappstore/470b7057b86f41c396a97903377f3d81) - Adds enhanced logging to all requests and responses from all Burp Suite tools, enable this one before you need it ;)

- [Request Smuggler](https://portswigger.net/bappstore/aaaa60ef945341e8a450217a54a11646) - A relatively new extension, this allows you to attempt to smuggle requests to backend servers. See this talk by James Kettle for more details: [Link](https://www.youtube.com/watch?v=_A04msdplXs)

- [Autorize](https://portswigger.net/bappstore/f9bbac8c4acf4aefa4d7dc92a991af2f) - Useful for authentication testing in web app tests. These tests typically revolve around navigating to restricted pages or issuing restricted GET requests with the session cookies of low-privileged users

- [Burp Teams Server](https://github.com/Static-Flow/BurpSuite-Team-Extension) - Allows for collaboration on a Burp project amongst team members. Project details are shared in a chatroom-like format

- [Retire.js](https://portswigger.net/bappstore/36238b534a78494db9bf2d03f112265c) - Adds scanner checks for outdated JavaScript libraries that contain vulnerabilities, this is a premium extension

- [J2EEScan](https://portswigger.net/bappstore/7ec6d429fed04cdcb6243d8ba7358880) - Adds scanner test coverage for J2EE (java platform for web development) applications, this is a premium extension

- [Request Timer](https://portswigger.net/bappstore/56675bcf2a804d3096465b2868ec1d65) - Captures response times for requests made by all Burp tools, useful for discovering timing attack vectors 

A prerequisite for many of the extensions offered for Burp, we'll walk through the installation of Jython, the Java implementation of Python.

Article on some of the top extensions for Burp Suite: [Link](https://portswigger.net/testers/penetration-testing-tools)


Task13: But Wait, there's more!
-------------------------------

Before we conclude, let's take a quick look into the features that Burp Suite Professional offers: The Burp Suite Scanner and Collaborator Client!

1. Download the report attached to this task. What is the only critical issue?

--> Cross-origin resource sharing: arbitrary origin trusted

2. How many 'Certain' low issues did Burp find?

--> 12


For MORE: [portswigger](https://portswigger.net/web-security)


