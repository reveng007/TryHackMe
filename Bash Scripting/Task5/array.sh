#!/usr/bin/bash

transport=('car' 'train' 'bike' 'bus')

echo "${transport[@]}"

echo "${transport[1]}"

unset transport[1]

transport[1]="trainride"

echo "${transport[@]}"


