@echo off
setlocal
echo Starting WSL APK build...
wsl bash -lc "cd /mnt/d/py_projects/detection_tkinter; chmod +x build_apk_wsl.sh; ./build_apk_wsl.sh"
echo.
echo If the build succeeds, the APK will be in the bin\ folder.
pause
