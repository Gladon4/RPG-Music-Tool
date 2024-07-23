#!/bin/bash

help_text() {
        echo "-h : Help text"
        echo "-o [Arg] : Output File Name"
}

install() {
    output=${OPTARG}
    pipenv run pip install -r requirements_linux.txt
    pipenv run pip install pyinstaller
    pipenv run pyinstaller main.py --clean -F -n "$output" --add-data img:img -w
    rm -rf build/"$output"
}

while getopts hc:o: option
do
    case "${option}"       
    	in
        h) help_text
        exit
        ;;
        o) install;;
    esac
done