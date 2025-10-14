#!/bin/sh

if [ "$#" -eq 1 ]; then
	curl -s  $1 | grep -oP '(?<=href=")[^"]*'

fi
