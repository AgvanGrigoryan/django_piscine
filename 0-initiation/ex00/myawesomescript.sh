#!/bin/sh

if [ "$#" -eq 1 ]; then
	response=$(curl -s $1)
	echo $response | grep -oP 'href="\K[^"]+'
fi


