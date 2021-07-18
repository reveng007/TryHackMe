#!/usr/bin/python3

import pickle

result = pickle.load(open("download.dat", 'rb'))

passwd = ""
user = ""
l_pass = []
l_user = []


for i,x in result:
    if 'ssh_user' in i:
        i = int(i[8::])
        l_user.append((i,x))

    else:
        i = int(i[8::])
        l_pass.append((i,x))

l_user.sort()
#Adding those `user` parts
for i,x in l_user:
    user += x

l_pass.sort()
#Adding those `pass` parts
for i,x in l_pass:
    passwd += x


print("Username: ", user)
print("Password: ", passwd)

