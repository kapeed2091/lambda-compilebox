#!/bin/bash

#set -e

########################################################################
#	- This is the main script that is used to compile/interpret the source code
#	- The script takes 3 arguments
#		1. The compiler that is to compile the source file.
#		2. The source file that is to be compiled/interpreted
#		3. Additional argument only needed for compilers, to execute the object code
#	
#	- Sample execution command:   $: ./script.sh g++ file.cpp ./a.out
#	
########################################################################

temp_folder=$1
compiler=$2
file=$3
output=$4
addtionalArg=$5


########################################################################
#	- The script works as follows
#	- It first stores the stdout and std err to another stream
#	- The output of the stream is then sent to respective files
#	
#	
#	- if third arguemtn is empty Branch 1 is followed. An interpretor was called
#	- else Branch2 is followed, a compiler was invoked
#	- In Branch2. We first check if the compile operation was a success (code returned 0)
#	
#	- If the return code from compile is 0 follow Branch2a and call the output command
#	- Else follow Branch2b and output error Message
#	
#	- Stderr and Stdout are restored
#	- Once the logfile is completely written, it is renamed to "completed"
#	- The purpose of creating the "completed" file is because NodeJs searches for this file 
#	- Upon finding this file, the NodeJS Api returns its content to the browser and deletes the folder
#
#	
########################################################################

exec  1> "$temp_folder/logfile.txt"
exec  2> "$temp_folder/errors"
#3>&1 4>&2 >

START=$(date +%s.%2N)
#Branch 1
if [ "$output" = "" ]; then
    $compiler $file -< "$temp_folder/inputFile" #| tee /usercode/output.txt
#Branch 2
else
	#In case of compile errors, redirect them to a file
        $compiler /usercode/$file $addtionalArg #&> /usercode/errors.txt
	#Branch 2a
	if [ $? -eq 0 ];	then
		$output -< "$temp_folder/inputFile" #| tee /usercode/output.txt
	#Branch 2b
	else
	    echo "Compilation Failed"
	    #if compilation fails, display the output file	
	    #cat /usercode/errors.txt
	fi
fi

#exec 1>&3 2>&4

#head -100 /usercode/logfile.txt
#touch /usercode/completed
END=$(date +%s.%2N)
runtime=$(echo "$END - $START" | bc)

echo "*-COMPILEBOX::ENDOFOUTPUT-*" $runtime

mv "$temp_folder/logfile.txt" "$temp_folder/completed"
