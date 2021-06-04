
## Task1:

1. Let's run nmap and check what ports are open.

```
nmap 10.10.132.218 -p- -vv

->
Reason: 65533 no-responses
PORT     STATE SERVICE       REASON
80/tcp   open  http          syn-ack
3389/tcp open  ms-wbt-server syn-ack
```

2. What port is for the web server?

```
80
```

3. What port is for remote desktop service?

```
3389
```

4. What is a possible password in one of the pages web crawlers check for?

```
UmbracoIsTheBest!
```
Process:
```
S1:
wget -r $IP

S2:
Then manually finding out in robot.txt
```
OR,
```
sudo gobuster dir -u $IP -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.atxt -x php,html,txt

->

/search               (Status: 200) [Size: 3422]
/rss                  (Status: 200) [Size: 1877]
/blog                 (Status: 200) [Size: 5399]
/sitemap              (Status: 200) [Size: 1047]
/archive              (Status: 301) [Size: 123] [--> /blog/]
/categories           (Status: 200) [Size: 3546]            
/authors              (Status: 200) [Size: 4120]            
/Search               (Status: 200) [Size: 3472]            
/tags                 (Status: 200) [Size: 3599]            
/install              (Status: 302) [Size: 126] [--> /umbraco/]
/RSS                  (Status: 200) [Size: 1877]               
/Blog                 (Status: 200) [Size: 5399]               
/SiteMap              (Status: 200) [Size: 1047]               
/Archive              (Status: 301) [Size: 123] [--> /blog/]   
/robots.txt           (Status: 200) [Size: 192]                
/siteMap              (Status: 200) [Size: 1047]               
/INSTALL              (Status: 302) [Size: 126] [--> /umbraco/]
/Sitemap              (Status: 200) [Size: 1047]               
/1073                 (Status: 200) [Size: 5399]               
/Rss                  (Status: 200) [Size: 1877]
...

Saw robot.txt ...
```
see: https://www.hackingarticles.in/5-ways-crawl-website/


5. What CMS is the website using? (CMS : Content Management 
```
I went to /umbraco/ => Got a login website --> then it was clear: CMS => umbraco
```

6. What is the domain of the website?
```
ANTHEM.COM 
```
Process: written on the 1st page of website

7. What's the name of the Administrator ?
```
Solomon Grundy
```
process:
```
S1: [saw hint to search in Oracle(hint: OSINT)
Opened all blogs and found verses in 2nd blog and googled it
```

8. Can we find find the email address of the administrator?

hint: There is another email address on the website that should help us
figuring out the email pattern used by the administrator.
```
mail addr: JD@anthem.com
admin name: Solomon Grundy
-> SG@anthem.com
```

## Task2:

Got with `wget -r`

>THM{G!T_G00D} --> IP/index.html        flag 2

>THM{L0L_WH0_US3S_M3T4} --> IP/a-cheers-to-our-it-department/index.html    flag 1

>THM{L0L_WH0_D15} --> IP/authors/jane-doe/index.html			   flag 3

>THM{AN0TH3R_M3TA} --> IP/archive/a-cheers-to-our-it-department/index.html flag 4


## Task3:

logged in via RDP:

user: sg	==> In many orgs., employees keep their username with the
		    name of their 1st name of email address.

password: UmbracoIsTheBest!      => No easy way, pure brute-force

1. Gain initial access to the machine, what is the contents of user.txt?
```
THM{N00T_NO0T}
```

2. Can we spot the admin password? [Hint: Hidden]
```
ChangeMeBaby1MoreTime
```

process:

Follow the snapshots:


3. Escalate your privileges to root, what is the contents of root.txt?
```
user: administrator
pass: ChangeMeBaby1MoreTime

root.txt: THM{Y0U_4R3_1337}
```

