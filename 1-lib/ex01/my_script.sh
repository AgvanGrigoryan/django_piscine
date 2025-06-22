#!/bin/bash
lib_folder="local_lib"
log_file=$lib_folder/"path.log"
py_script="my_program.py"
green="\e[32m"
red="\e[31m"
reset_color="\e[0m"

echo -e $green"Using pip version:"$reset_color
pip --version

mkdir -p $lib_folder

echo -e $green"Installing path.py in ./$lib_folder/"$reset_color
pip install --target $lib_folder --upgrade git+https://github.com/jaraco/path.git > $log_file 2>&1

if [ $? -eq 0 ]; then
	echo -e $green"Installation successful. Running Python script..."$reset_color
	PYTHONPATH=$lib_folder python3 $py_script
else
	echo -e $red"Installation failed. Check ./$log_file for details."$reset_color
fi