# mdskills

Lokalni alat za pregled, izmjenu i izradu `.md` datoteka i Claude skillova.
Otvara se u pregledniku, kao interni alat: `http://127.0.0.1:7777`.

Bez ijedne vanjske ovisnosti. Samo Python 3 i standardna biblioteka.
Nema `pip install`, nema `npm install`, nema build koraka.

## Pokretanje

Dvoklik na **`start.cmd`**, ili u terminalu:

```
cd C:\Users\krist\mdskills
python server.py
```

Preglednik se otvori sam. Prekid: `Ctrl+C` u prozoru servera.
Ako ne zelite da se preglednik otvori: `python server.py --no-browser`.

## Precac i taskbar

`python make_icon.py` napravi `icon.ico`, bez vanjskih biblioteka: PNG se
sastavi rucno preko `zlib`, pa se zapakira u ICO kontejner.

Precac se napravi ovako:

```powershell
$sh = New-Object -ComObject WScript.Shell
$s = $sh.CreateShortcut("$([Environment]::GetFolderPath('Desktop'))\mdskills.lnk")
$s.TargetPath = "$PWD\start.cmd"
$s.WorkingDirectory = "$PWD"
$s.IconLocation = "$PWD\icon.ico,0"
$s.WindowStyle = 7
$s.Save()
```

**Pinanje na taskbar se ne da skriptirati.** Na Windowsu 11, provjereno na
buildu 26200, glagol *Pin to taskbar* ne postoji medu shell glagolima
(`Shell.Application` ih izlista, njega nema). Zadnji korak ide rucno: desni
klik na precac, pa *Pin to taskbar*. Isti precac lezi i u Start meniju, pa se
moze pinati i iz pretrage.

`start.cmd` je napisan tako da drugi klik ne padne na zauzet port: ako server
vec slusa na 7777, samo otvori preglednik.

## Sto moze

- **Pregled** svake `.md` datoteke, renderirano (naslovi, liste, tablice, kod,
  citati, linkovi).
- **Izmjena** u istom prozoru: `Uredi`, pa `Spremi` ili `Ctrl+S`.
- **Nova `.md`** u bilo kojoj od mapa iz `config.json`.
- **Novi skill**: napravi mapu, `SKILL.md` s ispravnim frontmatterom i praznu
  `references/` mapu.
- **Nova referenca** unutar otvorenog skilla.
- **Provjera skillova**: pokraj imena pise upozorenje ako nema frontmattera,
  ako nema `name` ili `description`, ili ako se `name` ne podudara s imenom mape.
- **`[[wikilinks]]`** su klikabilni. Ako ciljna datoteka ne postoji, link je
  zut, pa se odmah vidi sto treba napisati. Zato radi i nad `MEMORY.md`.
- **Filtriranje** po imenu i opisu, preko polja gore lijevo.

## Tipke

| Tipka | Radi |
| --- | --- |
| `Ctrl+S` | spremi (dok ste u uredivanju) |
| `Esc` | odustani od uredivanja |
| `e` | uredi otvorenu datoteku |
| `r` | osvjezi popis |
| `/` | skoci u polje za filtriranje |

## Mape (`config.json`)

Pri prvom pokretanju napravi se `config.json` s ovim mapama:

| Mapa | Vrsta | Sto je unutra |
| --- | --- | --- |
| `~/.agents/skills` | `skills` | skillovi instalirani preko `npx skills add` |
| `~/.claude/skills` | `skills` | Claude Code skillovi (cesto symlinkovi na gornje) |
| `~/.claude/projects/C--Users-krist/memory` | `md` | trajna memorija, `MEMORY.md` i ostalo |
| `~/Desktop/SiteSpec` | `md` | predlozak za brief i ispunjeni kai-sol brief |
| `~/mdskills/notes` | `md` | biljeznica za sve ostalo |

Dodavanje mape: upisite novi red u `config.json` i kliknite `Osvjezi`.
Server ne treba restart.

```json
{
  "roots": [
    { "label": "Moja mapa", "path": "~/negdje/drugdje", "kind": "md" }
  ]
}
```

`kind` je `skills` (mape koje sadrze `SKILL.md`) ili `md` (obicne `.md` datoteke,
trazi rekurzivno do 6 razina).

## Sigurnost i podaci

- Server slusa **samo na `127.0.0.1`**. Nije dostupan s mreze ni s interneta.
- Svaki put iz API-ja provjerava se da je **unutar mapa iz `config.json`**.
  Pokusaj izlaska iz njih vraca `403`.
- Spremanje je **atomarno** (pise u `.tmp~` pa preimenuje), tako da prekid ne
  ostavlja polovicnu datoteku.
- Ako je datoteka promijenjena izvan alata dok je bila otvorena, spremanje se
  **odbija** s porukom umjesto da tiho prepise tudu izmjenu.
- Brisanje ne brise: datoteka se seli u `.trash/` unutar iste mape, s
  vremenskom oznakom u imenu.
- Ogranicenje velicine datoteke je 4 MB.

## Granice, posteno

- Renderer markdowna je **podskup**, ne puni CommonMark: naslovi, odlomci,
  liste (jedna razina ugnjezdavanja), tablice, ograde koda, citati, `hr`,
  podebljano, kurziv, precrtano, inline kod, linkovi, slike kao oznaka,
  `[[wikilinks]]`. Ugnjezdene liste u vise razina i HTML u markdownu nisu
  podrzani u prikazu; u datoteci ostaju netaknuti.
- Uredivanje je obican `textarea`: nema isticanja sintakse ni automatskog
  dovrsavanja.
- Nema povijesti verzija. Ako vam treba, drzite mapu u gitu.
- Jedan korisnik u jednom trenutku. Alat je za jedno racunalo, ne za tim.
