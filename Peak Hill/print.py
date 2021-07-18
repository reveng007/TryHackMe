#!/usr/bin/python3
import pickle

with open('download.dat', 'rb') as file:
    pickle_data = file.read()
    result = pickle.loads(pickle_data)
    print(result)

