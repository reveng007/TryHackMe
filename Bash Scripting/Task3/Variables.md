```
name="Reveng"
```

>NOTE:

>Please note that for variables to work you cannot leave a space between the variable name, the ”=” and the value. They cannot have spaces in.

>echo $name
>     |
>     |---> We have to add a '$' onto front of our variable name in order to use 
>            it

```
------> Reveng
```

## 1.

## Tracing the Execution ( -x option ):

> It instructs the shell to display how each command looks like before execution. Also, it gives you the choice whether to debug a whole script or just a part of it.

## Debugging the Whole Script:

>Starting the shell with –x option    will run the whole script in debugging mode. In this mode, traces of commands and their arguments are displayed to the output before they are executed.

> To run the entire script in debug mode, add a -x parameter before the .sh command as follows:

```
$ bash -x ./script.sh

OR,

$ bash -x script.sh
```
## Debugging a Part of Script:

> If we are sure only a part of the script is causing errors, then there is no need to debug an entire script. We can debug some portion or several portions of the script as follows:

> Place the “set –x” option at the starting point of the area that needs to debug and place the “set + x” option where you want it to stop. 

```
echo 'hi'

set -x

#this section will be debugged

set +x
```
## 2.
## Displaying the Scripts Commands ( -v option ):

> -v (short for verbose) instructs the shell to execute in verbose mode. When using this mode, it displays all commands in a script before executing them.
```
$ bash -v script.sh

OR,

$ bash -v ./script.sh
```
