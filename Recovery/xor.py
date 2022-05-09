key=b"AdsipPewFlfkmll"
fil="todo.html"
f=open(fil,"rb")
contents=f.read()
for i in range(0,len(contents)):
      print(chr(contents[i]^key[i%len(key)]),end='')

