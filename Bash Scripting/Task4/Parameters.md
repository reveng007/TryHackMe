
### We will now look at one of the main features of bash and that's using parameters.

#### 1. We will firstly  look at parameters specified using the command line when running the file.

> These come in many forms but often have the ```$```  prefix because a parameter is still a variable.

```
name=$1
echo $name
```
```
$~> bash script1.sh Reveng

Reveng
```
```
$~> bash script1.sh Reveng reveng

Reveng
```
### In this case, only ```Reveng``` got printed, "reveng" not... But to do so,

```
name=$2
echo $name
```
```
$~> bash script1.sh Reveng reveng

reveng
```
### To print both,

```
#!/usr/bin/bash

name1=$1
name2=$2

echo $name1 $name2

```
```
$~> bash para3.sh Reveng reveng

Reveng reveng
```
### To print uncountable names:
```
#!/usr/bin/bash

name=$@
echo $name
```
```
$~> bash para1.sh reveng Reveng aekfm wfef wfeqf

reveng Reveng aekfm wfef wfeqf

```

### Making the script more interactive:

```
#!/usr/bin/bash

echo Enter your username:

read user

echo "Home of $user is /home/$user"

```
```
$~> bash para4.sh

Enter your username:
sudomom
Home of sudomom is /home/sudomom

```
### 1. How can we get the number of arguments supplied to a script?

### Ans: $#

### 2. How can we get the filename of our current script(aka our first argument)?

### Ans: $0

### 3. How can we get the 4th argument supplied to the script?

### Ans: $4

### 4. If a script asks us for input how can we direct our input into a variable called ‘test’ using “read”

### Ans: read test

### 5. What will the output of “echo $1 $3” if the script was ran with “./script.sh hello hola aloha”

### Ans: hello aloha




