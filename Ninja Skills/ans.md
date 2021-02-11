
# THM: Ninja Skills
  -------------------
  -------------------

```
Answer the questions about the following files:

8V2L
bny0
c4ZX
D8B3
FHl1
oiMO
PFbD
rmfX
SRSq
uqyw
v2Vb
X1Uy

```
### The aim is to answer the questions as efficiently as possible.


## I have actually completed this challenge in this order, in this order you all can follow easily

### 1. Which of the above files are owned by the best-group group(enter the answer separated by spaces in alphabetical order)

```diff
+ new-user@ip-10-10-88-51 ~]$ find / -group best-group 2> /dev/null

```
### 6. Which file is executable by everyone?

```diff

+ #!/bin/bash

file_names='8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy'

for name in $file_names
do
	find / -type f -executable -name $name 2> /dev/null
	
done

```

### 5. Which file's owner has an ID of 502?

```diff
+ [new-user@ip-10-10-88-51 home]$ grep '502' /etc/passwd

:arrow_right_hook:

+ [new-user@ip-10-10-88-51 home]$ find / -user newer-user 2> /dev/null

:arrow_right_hook:

```

### 4. Which file contains 230 lines?

```diff
+ #!/bin/bash

file_names='8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy'

for name in $file_names
do
        direc=$(find / -type f -name $name 2>/dev/null)
        echo $direc
done

```

### But for some reason "_bny0_" didn't show up...


```diff

+ #!/bin/bash
file_names='8V2L bny0 c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy'
for name in $file_names
do
        direc=$(find / -type f -name $name 2>/dev/null)
        value=$(wc -l $direc | cut -d " " -f 1)
        if [[ $value -gt 230 ]]
        then
        	echo $direc
        fi
        #grep -E -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' $direc
        #printf -- '-%.0s' {1..100}; echo
        # find / 
done

```

### Even when I tried this script, it didn't show up anything.

## So I made another (aiming for inverting the logic ) ---> Which will not be shown are to be considered as the answer and also transferred "_bny0_" to last in list to avoid confusion.


```diff

+ #!/bin/bash

file_names='8V2L c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy bny0'

for name in $file_names
do
        direc=$(find / -type f -name $name 2>/dev/null)
        wc -l $direc
        #grep -E -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' $direc
        #printf -- '-%.0s' {1..100}; echo
        # find / 
done

```
### OUTPUT:

```diff

+ [new-user@ip-10-10-88-51 ~]$ bash pattern_matching.sh 

209 /etc/8V2L
209 /mnt/c4ZX
209 /mnt/D8B3
209 /var/FHl1
209 /opt/oiMO
209 /opt/PFbD
209 /media/rmfX
209 /etc/ssh/SRSq
209 /var/log/uqyw
209 /home/v2Vb
209 /X1Uy
^C
[new-user@ip-10-10-88-51 ~]$

```

### 2. Which of these files contain an IP address?

```diff
+ #!/bin/bash

file_names='8V2L c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy bny0'

for name in $file_names
do
        direc=$(find / -type f -name $name 2>/dev/null)
        #wc -l $direc
        grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" $direc && echo $direc
        #           |____________________________|               
        #                         |_________________ ip  extraction

        #printf -- '-%.0s' {1..100}; echo
        # find / 
done

```

### 3. Which file has the SHA1 hash of 9d54da7584015647ba052173b84d45e8007eba94

```diff
+ #!/bin/bash

file_names='8V2L c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy bny0'

hash=9d54da7584015647ba052173b84d45e8007eba94

COUNTER=0

for name in $file_names
do
        direc=$(find / -type f -name $name 2>/dev/null)
        #wc -l $direc
        Grepped=$(grep $hash $direc)

        if [[ ${10#Grepped} -gt ${10#hash} ]]
        then
                echo $direc
        else
                COUNTER=$[COUNTER + 1]
                echo Nope$COUNTER
                continue
        fi
        #printf -- '-%.0s' {1..100}; echo
        # find / 
done

```
### This gave me no result .... :confused:

```diff
+[new-user@ip-10-10-88-51 ~]$ bash pattern_matching.sh 
Nope1
Nope2
Nope3
Nope4
Nope5
Nope6
Nope7
Nope8
Nope9
Nope10
Nope11
^C
+[new-user@ip-10-10-88-51 ~]$
```
### I researched a bit on google, that how to pick sha1sum from files along with find command.

```
+ #!/bin/bash

hash=9d54da7584015647ba052173b84d45e8007eba94

file_names='8V2L c4ZX D8B3 FHl1 oiMO PFbD rmfX SRSq uqyw v2Vb X1Uy bny0'

COUNTER=0
for name in $file_names
do
        value=$(find / -type f -name $name -exec sha1sum {} \; 2>>/dev/null)

        hashes=$(echo $value | cut -d " " -f 1)
        COUNTER=$[COUNTER + 1]

        if [[ $hashes == $hash ]]
        then
                echo $value
        else
                echo Nope$COUNTER
        fi

done

```
### Now Got the result..... :100:

```
+ [new-user@ip-10-10-76-223 ~]$ bash pat.sh 

Nope1
9d54da7584015647ba052173b84d45e8007eba94 /mnt/c4ZX
Nope3
Nope4
Nope5
Nope6
Nope7
Nope8
Nope9
Nope10
Nope11
Nope12

+ [new-user@ip-10-10-76-223 ~]$
```
