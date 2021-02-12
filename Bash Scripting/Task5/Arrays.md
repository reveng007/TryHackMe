
### Arrays are used to store multiple pieces of data in one variable, which can then be extracted by using an index. Most commonly notated as ```var [index_position]```

### Arrays use indexing meaning that each item in an array stands for a number.

### In the array ```['car', 'train', 'bike', 'bus']``` each item has a corresponding index.

### All indexes start at position 0

|   item         |  index      |
| :----------:   | :---------: |
|    car         |      0      |
|   train        |      1      |
|    bike        |      2      |
|    bus         |      3      |

### Let's make an array in bash,

#### We have the variable name, in our case ‘transport’

#### We then wrap each item in brackets leaving ```"a space"``` between each item.

```transport=('car' 'train' 'bike' 'bus')```

```diff
+ We can then echo out all the elements in our array like this:

echo "${transport[@]}"

echo "${transport[1]}"
```
>  @ : means all arguments
> [ ]: specifies its index

```
$~> bash array.sh

car train bike bus
train
```
### To remove any element, use ```unset```

```
#!/usr/bin/bash

transport=('car' 'train' 'bike' 'bus')

echo "${transport[@]}"

echo "${transport[1]}"

unset transport[1]

echo "${transport[@]}"
```
```
$~> bash array.sh

car train bike bus
train
car bike bus

```
### Index 1 value is removed...
### Now let input value to the unset position of the array.

```
#!/usr/bin/bash

transport=('car' 'train' 'bike' 'bus')

echo "${transport[@]}"

echo "${transport[1]}"

unset transport[1]

transport[1]='trainride'

echo "${transport[@]}"

```
```
$~> bash array.sh

car train bike bus
train
car trainride bike bus
```

