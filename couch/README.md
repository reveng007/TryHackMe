```
$nmap 10.10.2.10 -p- -T5 -vv

Discovered open port 22/tcp on 10.10.2.10

Discovered open port 5984/tcp on 10.10.2.10

```

```
$ nmap 10.10.2.10 -p5984 -sV -A -vv

PORT     STATE SERVICE REASON  VERSION
5984/tcp open  http    syn-ack CouchDB httpd 1.6.1 (Erlang OTP/18)
|_http-favicon: Unknown favicon MD5: 2AB2AAE806E8393B70970B2EAACE82E0
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-server-header: CouchDB/1.6.1 (Erlang OTP/18)
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).

```


see: [github-writeup](https://phannguyenlong.github.io/2021-07-04-couchDB/)

