@echo off
title Where is the president — Mundus Administratum
cd /d "%~dp0"
python praeses.py
if errorlevel 1 pause
