#!/bin/bash

help_text() {
        echo "-h : Help text"
        echo "-o [Arg] : Output File Name"
}

while getopts hc:o: option
do
    case "${option}"       
    	in
        h)help_text
        exit
        ;;
        o)output=${OPTARG};;
    esac
done

pip install -r requirements_linux.txt
pip install pyinstaller
pyinstaller main.py --clean -F -n "$output" --add-data img:img -w
rm -rf build/"$output"