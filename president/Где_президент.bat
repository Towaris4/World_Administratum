@echo off
title Gde president — Mundus Administratum
cd /d "%~dp0"
python praeses.py
if errorlevel 1 pause
