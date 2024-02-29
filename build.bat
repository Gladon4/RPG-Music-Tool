@ECHO off
pip install -r requirements_win.txt
pip install pyinstaller

set "var1=%1"
if not defined var1 echo Enter Argument & goto -h

if /I "%var1%"=="-h" (
  goto -h
) else if /I "%var1%"=="-o" ( 
  goto -o
) else (
  echo Enter valid argument & goto -h
)

:-h
  ECHO -h : Help text
  ECHO -o [Arg] : Output File Name
  goto end

:-o
  set "var2=%2"
  if not defined Var2 echo Enter Filename & goto -h
  pyinstaller main.py --clean -F -n %2 --add-data img;img -w
  rmdir /s /q build\%2
  goto end

:end

