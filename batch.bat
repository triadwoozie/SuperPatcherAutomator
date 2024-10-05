@echo ---------------mkh.mourad batch script


rem Setup ENV
SETLOCAL ENABLEDELAYEDEXPANSION
rem // Delete Previous Folder
RMDIR /S /Q temp-folder
MKDIR temp-folder
call set curentDir="%cd%%"
FOR /f "delims=" %%G in ('DIR /S /A:-D /B  *.lz4') do (
	call cd %%~dpG
	call !curentDir!\BIN\tar --create --format=gnu -b20 --quoting-style=escape --owner=0 --group=0 --totals --mode=644  -f %%~nG.tar %%~nxG
        xcopy %%~nxG  !curentDir!\temp-folder\
	)
cd !curentDir!	


rem Build the TAR File
cd temp-folder
call !curentDir!\BIN\ls *.lz4 > temp-file.txt
call !curentDir!\BIN\tar --create --format=gnu -b20 --quoting-style=escape --owner=0 --group=0 --totals --mode=644  -f AP_TAR_MD5_CUSTOM_FILE_ODIN.tar -T temp-file.txt
del /Q temp-file.txt
cd !curentDir!	


rem Create the MD5 Final File:
FOR /f "delims="  %%G in ('DIR /S /A:-D /B  *.tar') do (
	call cd %%~dpG
	call !curentDir!\BIN\md5sum -t %%~nxG >> %%~nxG
        call !curentDir!\BIN\mv %%~nxG %%~nxG.md5
	)
cd !curentDir!

rem Cleaning Files
FOR /f "delims=" %%G in ('DIR /S /A:-D /B *.lz4 *.md5 ^| FINDSTR /v /i "\AP_TAR_MD5_CUSTOM_FILE_ODIN.tar.md5$"') do del /Q "%%G"

