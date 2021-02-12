
#### When we talk about conditionals it means that a certain piece of code relies on a condition being met, this is often determined with relational operators, such as equal to, greater than, and less than.

```
count=10

if [ $count -eq 10 ]
then
    echo "true"
else
    echo "false"
fi

OR,

count=10

if [ $count = 10 ]
then
    echo "true"
else
    echo "false"
fi

```
>1. If statements always use a pair of brackets

>2. In the case of the [] we need to leave a ***space*** on both sides of the text(the bash syntax)

>3. We also always need to end the ***if*** statement with fi


|   Operator     |                    Description                                    |  
| -------------- | ------------------------------------------------------------------| 
|  -eq or =      |  Checks if the value of two operands are equal or not; if yes,    |         |                |    then the condition becomes true.                               |
|                |                                                                   |
|     -ne        |  Checks if the value of two operands are equal or not; if values  | 
|                |   are not equal, then the condition becomes true.                 |
|                |                                                                   | 
|     -gt        |  Checks if the value of left operand is greater than the value of | 
|                |  right operand; if yes, then the condition becomes true.          |
|                |                                                                   | 
|      -lt       |  Checks if the value of left operand is less than the value of    |
|                |  right operand; if yes, then the condition becomes true.          |
|                |                                                                   |
|      -ge       |  Checks if the value of left operand is greater than or equal to  | 
|                |  the value of right operand; if yes, then the condition becomes   | 
|                |  true.                                                            |

### Lets do this,

```
#!/usr/bin/bash

value="guessme"

guess=$1

if [ "$value" = "$guess" ] 
then
	echo "They are equal"
else
	echo "They are not equal"
fi

```
### 1. What is the flag to check if we have read access to a file?

### Ans: -r

### 2. What is the flag to check if we have write access to a file?

### Ans: -w

### 3. What is the flag to check the existance a file?

### Ans: -f

### 4. What is the flag to check to see if it's a directory?

### Ans: -d




