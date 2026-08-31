# 03 Windows i pokretanje

Ovo je poglavlje skupilo najviše izgubljenih sati. Gotovo sve zamke su u
`cmd.exe`, a manifestiraju se kao "aplikacija ne radi", iako aplikacija radi
cijelo vrijeme.

## Batch datoteke: tri zamke koje gase prozor

### 1. Prijelomi redaka moraju biti CRLF

Alat koji piše datoteku obično koristi LF. Windows `cmd.exe` tada **trenutno
zatvori prozor**, prije nego dođe do `pause`, jer krivo raščlani blok.

Ispravak:

```bash
awk '{sub(/\r$/,""); printf "%s\r\n",$0}' run.bat > tmp && mv tmp run.bat
```

Provjera **isključivo** s `od -c`. Naredbe `grep -P` i `$'\r'` lažno javljaju LF
zbog postavki jezika.

Uz to, batch datoteke pisati u ASCII znakovima. Em crtica u ispisu zna srušiti
raščlanjivanje.

### 2. Zagrade u `echo` unutar `if` bloka

```batch
if not exist .venv (
    echo Stvaram okolinu (prvi put)     REM zatvorena zagrada gasi blok
)
```

`cmd.exe` vidi `)` u tekstu kao kraj bloka. Prozor se zatvori bez poruke.

Rješenje je izbjeći višelinijski blok:

```batch
if exist .venv goto POKRENI
echo Stvaram okolinu, prvi put traje malo dulje
python -m venv .venv
:POKRENI
```

### 3. Escapeanje cijevi

`^|` vrijedi **samo** unutar `for /f "..."` ili unutar `echo`. Na običnom retku
mora biti obična cijev:

```batch
ipconfig | findstr IPv4          REM ispravno
ipconfig ^| findstr IPv4         REM "unrecognized command line"
```

## Samoizlječiva virtualna okolina

Isporučena `.venv` puca na drugom računalu jer je vezana uz točnu verziju
Pythona. Zato `run.bat` provjerava i po potrebi pregrađuje okolinu:

```batch
.venv\Scripts\python -c "import fastapi,uvicorn" 2>nul
if not errorlevel 1 goto START
echo Okolina nije ispravna, gradim ponovno
rmdir /s /q .venv
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
:START
.venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 86XX
```

Za produkciju maknuti `--reload`. Dodati razumljivu poruku ako `py` ne postoji.

Pri prvom pokretanju `run.bat` može generirati `.env` s nasumičnim `SECRET_KEY`
preko PowerShella (`[guid]::NewGuid()`).

## Autostart pri prijavi

Skriveni pokretač u Startup mapi diže aplikaciju bez prozora:

```vbs
' <naziv>.vbs u %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
CreateObject("WScript.Shell").Run "cmd /c run.bat", 0, False
```

Isključivanje je brisanje `.vbs` datoteke.

## Task Scheduler za zadatke po rasporedu

Za zadatke koji se moraju izvršiti svaki dan **Daily uz StartWhenAvailable** je
bolji izbor od okidača pri prijavi.

Naučeno na primjeru: prebacivanje na okidač "pri prijavi" izgledalo je sigurnije
zbog vikenda, ali zadatak se nije izvršio jer je računalo ostalo upaljeno i
prijavljeno od jučer, pa nove prijave nije ni bilo. `Daily + StartWhenAvailable`
pokriva oba slučaja: računalo stalno upaljeno i računalo ugašeno preko vikenda.

Registracija dnevnog zadatka radi **bez administratorskih ovlasti**. Okidač
`AtLogon` ih traži.

Uz to dodati **osigurač "jednom dnevno"**: datoteka koja pamti datum zadnjeg
uspješnog izvršenja. Time višestruke prijave u istom danu ne pokreću posao
više puta, a zastavice `--forsiraj` i `--vidljivo` zaobiđu osigurač za ručni rad.

## Dogovor o portovima

Kada na jednom računalu živi više aplikacija, potreban je popis portova. Provjerena
podjela:

| Port | Namjena |
| --- | --- |
| 80 | portal s poveznicama na sve aplikacije |
| 8000 | glavni sustav |
| 8010 | ponude |
| 8501 | zadano za Streamlit |
| 8600 | skladište |
| 8601 | kvaliteta i reklamacije |
| 8602 | nabava |
| 8603 | analiza pokrivenosti |
| 8604 | normativi i montaža |
| 8605 | neaktivni lager |
| 8606 | upiti kupaca |
| 8607 | obavijesti i planer |
| 8608 | kalkulacije |
| 8610 | planiranje |
| 8611 | certifikati |

Sudari portova su stvaran problem. Stara Streamlit aplikacija na 8501 sudarala
se s drugim alatom, pa se pri prijavi otvarala pogrešna. Kod uklanjanja iz
autostarta preimenovati datoteku umjesto brisanja, da je promjena reverzibilna.

## Portal umjesto pamćenja IP adresa

Kolegama je teško pamtiti adresu oblika `192.168.x.x:8602`. Rješenje je mala stranica na
portu 80 koja nudi pločice sa svim aplikacijama.

- Python **može** vezati port 80 bez administratorskih ovlasti ako je slobodan.
- Ime računala se na lokalnoj mreži razrješava samo, pa je adresa `http://<ime-racunala>`.
- Poveznice graditi u JavaScriptu iz `location.hostname + ":" + port`, tako rade
  i preko imena i preko IP adrese.
- `/status` vraća JSON s dostupnošću po portu, pa pločica ima živu točkicu.
- Jedna aplikacija može dati više pločica na različite putanje istog porta.

Vlastita riječ umjesto imena računala (`http://alati`) traži DNS na ruteru ili
unos u `hosts` na svakom klijentu. Ime računala radi bez ičega.

## Upravljačka ploča nad aplikacijama

Mali Tkinter alat koji otkriva aplikacije skeniranjem mapa s `run.bat`, čita
port iz naredbe i nudi pokretanje, gašenje i autostart.

Dvije stvari koje nisu očite:

**Provjera stanja uvijek ide na `127.0.0.1`, nikad na adresu veze.** Aplikacija
vezana na `0.0.0.0` ne prima spajanje na `0.0.0.0`, pa se prikazuje kao ugašena
iako radi. Normalizirati `0.0.0.0` u `127.0.0.1`.

**Pokretanje ide izravno preko `python.exe -m uvicorn` s `CREATE_NO_WINDOW`,** ne
preko `run.bat`. Batch ima `pause` na kraju, koji bi ostao skriveno visjeti kada
se poslužitelj ugasi.

Gašenje: pronaći PID preko `netstat -ano` u stanju LISTENING, pa `taskkill /PID x /F /T`.

## Vatrozid: ne zaključivati iz Windows pravila

Provjereno u praksi: Windows vatrozid nije imao pravilo za port aplikacije, a
kolege su svejedno dolazile do nje. Razlog je bio sigurnosni paket treće strane
koji je preuzeo upravljanje vatrozidom, pa Windows pravila više nisu mjerodavna.

Zaključak: **testirati sa stvarnog drugog računala**, ne zaključivati iz
`Get-NetFirewallRule`.

## Izbor verzije Pythona

Najnovija verzija često nema gotove pakete za znanstvene biblioteke. Provjereno
stanje u vrijeme pisanja:

- 3.14 nema `scipy` ni `pymupdf`
- 3.12 je bio dobar kompromis za sve što traži prevođenje
- ako paket puca pri gradnji iz izvora, prisiliti gotovi paket:
  `pip install --only-binary :all: <paket>`
