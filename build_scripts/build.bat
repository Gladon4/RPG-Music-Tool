@ECHO off
setlocal

set "OUTPUT_NAME="

:: --- argument parsing ---
if /I "%~1"=="-h" (
  ECHO -h : Help text
  ECHO -o [Arg] : Output File Name
  goto end
) else if /I "%~1"=="-o" (
  set "OUTPUT_NAME=%~2"
  if not defined OUTPUT_NAME echo Enter Filename & goto end
  goto install
) else if not "%~1"=="" (
  echo Enter valid argument & goto -h
)

:: if no arguments, default to install with a name
if not defined OUTPUT_NAME set "OUTPUT_NAME=RPGMusicTool"

:install
  REM --- create / activate venv ---
  python -m venv .build_venv
  call .build_venv\Scripts\activate

  REM --- install deps ---
  pip install -r requirements_win.txt
  pip install pyinstaller

  REM --- build ---
  pyinstaller main.py ^
      --clean -F -n "%OUTPUT_NAME%" ^
      --add-data img;img ^
      --add-data resources;resources ^
      --hidden-import=PIL._tkinter_finder ^
      --add-data ".build_venv/Lib/site-packages/tkfilebrowser;tkfilebrowser" ^
      -w

  rmdir /s /q "build\%OUTPUT_NAME%"
  del "%OUTPUT_NAME%.spec"
  goto end

:-h
  ECHO -h : Help text
  ECHO -o [Arg] : Output File Name
  goto end

:end
endlocal
