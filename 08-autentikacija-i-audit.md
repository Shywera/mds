# 08 Autentikacija i zapis rada

## Kada prijava treba, a kada ne

Prijava **treba** kada aplikacija bilježi tko je što napravio, kada su podaci
osjetljivi ili kada više ljudi mijenja iste zapise i za to postoji odgovornost.

Prijava **ne treba** kada je alat jednokorisnički, radi lokalno i barata podacima
koji nisu osobni.

To je poslovna odluka, ne tehnička. U jednoj aplikaciji je prijava prvo bila
napravljena pa uklonjena na izričit zahtjev, jer je usporavala svakodnevni rad,
a podaci su interni.

**Opasnost koju treba izgovoriti naglas:** aplikacija bez prijave vezana na
`0.0.0.0` znači da svatko na lokalnoj mreži može brisati zapise. Ako se tako
ostavi, to mora biti svjesna odluka, a ne previd. Alternativa je vezanje samo na
`127.0.0.1`.

## Obrazac koji se pokazao prenosivim

Cijeli sloj se dodaje **bez diranja postojećih modula**, kroz međusloj i zaseban
modul:

```
app/modules/auth/
├── models.py      # Korisnik, AuditLog
├── security.py    # dozvole, hash lozinke, mapiranje putanje na dozvolu
└── routes.py      # prijava, odjava, upravljanje korisnicima, zapis rada
```

U `main.py` idu dva međusloja, redoslijed je bitan:

```python
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)   # vanjski
@app.middleware("http")
async def auth_audit(request, call_next):                               # unutarnji
    ...
```

`SessionMiddleware` se dodaje **zadnji**, jer mora biti vanjski sloj.

Međusloj radi tri stvari: traži prijavu, provjerava dozvolu i bilježi izmjene.

## Dozvole po namjeni, ne po ulozi

Provjereno je da su korisne granularne dozvole vezane uz posao, a ne apstraktne
uloge:

```python
PERMISSIONS = {"zaprimanje", "izdavanje", "inventura", "prioriteti", "admin"}
```

`admin` obuhvaća sve. Pregled je dopušten svakom prijavljenom korisniku.
Mapiranje putanje na dozvolu drži se na jednom mjestu (`required_perm`).

U predlošcima se ista funkcija koristi kao globalna Jinja funkcija, pa se
poveznice i osjetljivi dijelovi sučelja skrivaju kada korisnik nema pravo.
Registrirati je u **zajedničkoj** okolini, vidi [02](02-skelet-aplikacije.md).

## Lozinke i kolačići

- `bcrypt` ili `argon2`, nikako SHA-256
- potpisani kolačić s oznakom `httpOnly`, ne token u adresi
- ograničenje broja pokušaja
- bez ugrađenih pristupnih podataka u kodu

Pri praznoj bazi posijati administratora s lozinkom iz varijable okoline i jasno
reći korisniku da je promijeni.

### Zamka: `os.getenv` ne vidi `.env`

Ako projekt koristi `pydantic-settings`, varijable se učitavaju u objekt
postavki, a **ne** u `os.environ`. Poziv `os.getenv("ADMIN_PASSWORD")` tada
vraća `None`, a sijanje administratora tiho postavi pogrešnu lozinku.

Dodati polje u `Settings` i čitati `settings.admin_password`.

## Zaštite koje se lako zaborave

- korisnik ne može obrisati sam sebe
- ne smije ostati nula aktivnih administratora
- ruta za preuzimanje sigurnosne kopije zaštićena dozvolom `admin`

## Zapis rada

Bilježe se **izmjene** (POST, PUT, DELETE) sa statusom manjim od 400. Pregledi se
ne bilježe, inače zapis postane neupotrebljiv.

Korisno proširenje: stupac `predmet_id` izvučen iz putanje. Time se na detaljnoj
stranici predmeta može prikazati vremenski slijed svega što se s njim događalo.

Kada ruta sama zapisuje detaljniji trag (primjerice "QR oznaka prema poziciji"),
međusloj je mora preskočiti, inače postoje dva zapisa za istu radnju. Za to služi
popis prefiksa koji se izuzimaju.

Prihvatljivo odstupanje: neuspjela validacija koja završi preusmjeravanjem bilježi
se kao pokušaj. To je bolje nego ne bilježiti ništa.

## Obavijesti e-poštom

`smtplib` i `EmailMessage` iz standardne biblioteke, bez novih ovisnosti.

Ključno je da slanje bude **best-effort**: obavijest ne smije srušiti radnju.

```python
def posalji_email(...):
    if not settings.notif_enabled or not settings.smtp_host:
        return                       # tihi rad nasuho
    try:
        ...
    except Exception:
        log.warning("Slanje obavijesti nije uspjelo", exc_info=True)
```

Provjera rokova ne treba ugrađeni raspoređivač. Zasebna skripta koju pokreće
Task Scheduler je jednostavnija i vidljivija.

Eskalacija koja se pokazala korisnom: prekoračenje dulje od sedam dana dodaje
administratore u kopiju.
