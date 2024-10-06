@echo off
setlocal enabledelayedexpansion

:: Step 1: Download vbmeta.img file
set "url=https://dl.google.com/developers/android/qt/images/gsi/vbmeta.img"
set "temp_dir=temp"
if not exist "%temp_dir%" mkdir "%temp_dir%"

echo Downloading vbmeta.img...
bitsadmin /transfer downloadvbmeta /priority foreground %url% "%temp_dir%\vbmeta.img"
if errorlevel 1 (
    echo Error downloading vbmeta.img.
    exit /b 1
)
echo Downloaded vbmeta.img to %temp_dir%\vbmeta.img

:: Step 2: Compress vbmeta.img using lz4.exe
set "lz4_exe=%~dp0lz4.exe"
set "vbmeta_img=%temp_dir%\vbmeta.img"
set "vbmeta_img_lz4=%temp_dir%\vbmeta.img.lz4"
"%lz4_exe%" -B6 --content-size "%vbmeta_img%" "%vbmeta_img_lz4%"
if errorlevel 1 (
    echo Error compressing vbmeta.img.
    exit /b 1
)
echo Compression successful: %vbmeta_img_lz4%

:: Step 3: Delete the original vbmeta.img
del "%vbmeta_img%"
echo Deleted original file: %vbmeta_img%

:: Step 4: Create temp-folder and prompt user
set "temp_folder=temp-folder"
if not exist "%temp_folder%" mkdir "%temp_folder%"
pause
echo Please place the extracted AP file for your Samsung model in the folder "%temp_folder%", then press Enter to continue...
pause

:: Step 5: Delete all files except specific ones in temp-folder
setlocal
set files_to_keep=boot.img.lz4 dtbo.img.lz4 recovery.img.lz4 scp-verified.img.lz4 spmfw-verified.img.lz4 sspm-verified.img.lz4 super.img.lz4 tee-verified.img.lz4 tzar.img.lz4 userdata.img.lz4 vbmeta.img.lz4 vbmeta_system.img.lz4
for %%f in ("%temp_folder%\*") do (
    set "delete_flag=true"
    for %%k in (%files_to_keep%) do (
        if "%%~nxf"=="%%k" set "delete_flag=false"
    )
    if "!delete_flag!"=="true" (
        del "%%f"
        echo Deleted: %%~nxf
    )
)
endlocal

:: Step 6: Replace vbmeta.img.lz4 in temp-folder with the downloaded one
if exist "%temp_folder%\vbmeta.img.lz4" del "%temp_folder%\vbmeta.img.lz4"
move "%vbmeta_img_lz4%" "%temp_folder%\vbmeta.img.lz4"
echo Replaced vbmeta.img.lz4 in %temp_folder%

:: Step 7: Extract super.img.lz4 to super.img
set "super_img_lz4=%temp_folder%\super.img.lz4"
set "super_img=%temp_folder%\super.img"
"%lz4_exe%" -d "%super_img_lz4%" "%super_img%"
if errorlevel 1 (
    echo Error during extraction.
    exit /b 1
)
echo Extracted: %super_img%

:: Step 8: Run SuperPatcherGSI.py with flags
set "superpatcher_script=%~dp0SuperPatcherGSI.py"
python "%superpatcher_script%" -i "%super_img%" -o "%temp_folder%\output.img" -s 2
if errorlevel 1 (
    echo Error running SuperPatcherGSI.py.
    exit /b 1
)
echo SuperPatcherGSI.py executed successfully

:: Step 9: Rename output.img to super.img
if exist "%super_img%" del "%super_img%"
move "%temp_folder%\output.img" "%super_img%"
echo Renamed output.img to super.img

:: Step 10: Delete the old super.img.lz4 in temp-folder
if exist "%super_img_lz4%" del "%super_img_lz4%"
echo Deleted old super.img.lz4

:: Step 11: Compress new super.img into super.img.lz4
"%lz4_exe%" -B6 --content-size "%super_img%" "%super_img_lz4%"
if errorlevel 1 (
    echo Error compressing super.img.
    exit /b 1
)
echo Compressed new super.img into %super_img_lz4%

:: Step 12: Move new super.img.lz4 to temp-folder
move "%super_img_lz4%" "%temp_folder%\super.img.lz4"
echo Moved new super.img.lz4 into %temp_folder%

:: Step 13: Delete all .img files in the script directory
for %%f in ("%~dp0*.img") do del "%%f"
echo Deleted all .img files in the script directory

:: Step 14: Move files from temp-folder to script directory
for %%f in ("%temp_folder%\*") do move "%%f" "%~dp0"
echo Moved all files from %temp_folder% to script directory

:: Step 15: Ask if user wants to root the device
set /p root_choice="Do you want to root the device? (yes/no): "
if /i "%root_choice%"=="yes" (
    set /p patched_confirm="Have you patched the file according to the XDA guide? (yes/no): "
    if /i not "%patched_confirm%"=="yes" (
        echo Please patch the file before proceeding.
        exit /b 1
    )
)

:: Step 16: Run batch.bat
call "%~dp0batch.bat"
if errorlevel 1 (
    echo Error running batch.bat.
    exit /b 1
)
echo batch.bat executed successfully

:: Step 17: Inform user to check temp-folder for Odin3 files
echo Process complete. Please check the 'temp-folder' for the necessary files to flash the device using Odin3.

pause
