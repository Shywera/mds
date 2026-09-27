@echo off
rem mdskills - dvoklik za pokretanje.
rem Ako je server vec pokrenut, samo otvori preglednik.
rem Zatvaranje servera: Ctrl+C u ovom prozoru, ili ga zatvori.
cd /d "%~dp0"
title mdskills

netstat -ano | findstr "LISTENING" | findstr ":7777" >nul
if not errorlevel 1 goto :otvori

where python >nul 2>nul
if errorlevel 1 goto :nemapythona

echo Pokrecem mdskills na http://127.0.0.1:7777
echo Za prekid pritisni Ctrl+C.
echo.
python server.py
if errorlevel 1 goto :greska
exit /b 0

:otvori
echo mdskills je vec pokrenut. Otvaram preglednik.
start "" "http://127.0.0.1:7777/"
exit /b 0

:nemapythona
echo Python nije pronaden u PATH-u.
echo Instaliraj Python 3 pa pokreni ponovno.
pause
exit /b 1

:greska
echo.
echo Server je zavrsio s greskom. Prozor ostaje otvoren da se vidi poruka.
pause
exit /b 1
