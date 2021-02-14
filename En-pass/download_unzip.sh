#!/bin/bash

for i in `seq 1 100`;
do
	wget -q http://10.10.112.97:8001/zip/a$i.zip;
	unzip a$i.zip;
	cat a;
	rm a;
 	rm a$i.zip;

done

