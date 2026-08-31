# Priručnik za razvoj poslovnih aplikacija

Zbirka znanja, obrazaca i zamki skupljenih tijekom izrade dvadesetak internih
aplikacija, alata i web stranica. Namijenjena je kao polazna točka za svaki
sljedeći projekt, da se isti problemi ne rješavaju dvaput.

Sve što je ovdje zapisano provjereno je u stvarnom radu. Zamke nisu teorijske,
svaka je koštala nekoliko sati traženja uzroka.

## Sadržaj

| Poglavlje | O čemu je |
| --- | --- |
| [01 Načela rada](01-nacela-rada.md) | Kako se radi, kako se komunicira, kada se pita |
| [02 Skelet aplikacije](02-skelet-aplikacije.md) | Standardna arhitektura, raspored mapa, samostalne aplikacije |
| [03 Windows i pokretanje](03-windows-i-pokretanje.md) | Batch, VBS, Task Scheduler, portovi, portal, vatrozid |
| [04 Baza i migracije](04-baza-i-migracije.md) | SQLite, Alembic, sigurnosne kopije, izolacija testne baze |
| [05 Excel i podaci](05-excel-i-podaci.md) | openpyxl, pandas, čitanje kalkulacija, zamke u izvorima |
| [06 PDF, Word i grafika](06-pdf-word-i-grafika.md) | ReportLab, python-docx, Ghostscript, matplotlib |
| [07 Sučelje: HTMX i Alpine](07-sucelje-htmx-alpine.md) | Obrasci, redoslijed ruta, hrvatski brojevi, grafovi |
| [08 Autentikacija i zapis rada](08-autentikacija-i-audit.md) | Dozvole, bcrypt, audit trag, kada preskočiti prijavu |
| [09 Integracija umjetne inteligencije](09-ai-integracija.md) | Strukturirani izlaz, demo način rada, učenje iz ispravaka |
| [10 Web stranice i dizajn](10-web-stranice-i-dizajn.md) | Dizajn sustavi, GitHub Pages, konverzijska struktura |
| [11 Git i objava](11-git-i-objava.md) | Sanitizacija za javne repozitorije, deploy, grananje |
| [12 Domena: tiskarstvo](12-domena-tiskarstvo.md) | Normativi, strojevi, skladište, nazivlje |
| [13 Katalog zamki](13-katalog-zamki.md) | Sve zamke na jednom mjestu, za brzo pretraživanje |
| [14 Kontrolne liste](14-kontrolne-liste.md) | Nova aplikacija, novi modul, prije puštanja u rad |

## Kako se koristi

Prije početka novog projekta pročitati [01](01-nacela-rada.md), [02](02-skelet-aplikacije.md)
i odgovarajuću kontrolnu listu iz [14](14-kontrolne-liste.md).

Kada nešto ne radi a nema očitog razloga, prvo pretražiti
[13 Katalog zamki](13-katalog-zamki.md). Velik dio problema koji izgledaju kao
greške u kodu zapravo su poznata ponašanja alata.

## Napomena o sadržaju

Primjeri su izvedeni iz stvarnih projekata, ali su nazivi tvrtki, kupaca,
internih poslužitelja i osoba izostavljeni. Ostavljeni su tehnički obrasci,
formule i zaključci, jer je u njima vrijednost.
