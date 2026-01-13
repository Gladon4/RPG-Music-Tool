#!/bin/bash

help_text() {
        echo "-h : Help text"
        echo "-o [Arg] : Output File Name"
}

install() {
    output=${OPTARG}
    python3 -m venv .build_venv
    source .build_venv/bin/activate
    pip install -r requirements_linux.txt
    pip install pyinstaller
    pyinstaller main.py \
        --clean -F -n "$output" \
        --add-data img:img \
        --add-data resources:resources \
        --hidden-import=PIL._tkinter_finder \
        --add-data ".build_venv/lib/python3.12/site-packages/tkfilebrowser:tkfilebrowser" \
        -w
    rm -rf build/"$output"
    rm "$output".spec
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