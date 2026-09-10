@echo off
title Grok - World_Administratum
cd /d "C:\Users\Ivant\Desktop\World_Administratum"
if exist "C:\Users\Ivant\.grok\bin\grok.exe" (
  "C:\Users\Ivant\.grok\bin\grok.exe" --cwd "C:\Users\Ivant\Desktop\World_Administratum"
) else (
  grok --cwd "C:\Users\Ivant\Desktop\World_Administratum"
)
if errorlevel 1 pause
