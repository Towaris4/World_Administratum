@echo off
title Interfacies — Praeses silet
cd /d "%~dp0"
start "" "http://127.0.0.1:2026/"
python interfacies.py
if errorlevel 1 pause
