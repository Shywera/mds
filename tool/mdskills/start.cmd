@echo off
rem mdskills - dvoklik za pokretanje. Zatvaranje: Ctrl+C ili zatvori prozor.
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo Python nije pronaden u PATH-u.
  echo Instalirajte Python 3 pa pokrenite ponovno.
  pause
  exit /b 1
)

echo Pokrecem mdskills na http://127.0.0.1:7777
echo.
python server.py
if errorlevel 1 (
  echo.
  echo Server je zavrsio s greskom. Prozor ostaje otvoren da vidite poruku.
  pause
)
