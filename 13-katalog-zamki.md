# 13 Katalog zamki

Sve zamke na jednom mjestu, za brzo pretraživanje. Poredane po simptomu, jer se
tako i traže: prvo se vidi simptom, uzrok se traži.

Uz svaku stoji poveznica na poglavlje s objašnjenjem.

---

## Prozor se otvori i odmah zatvori

| Uzrok | Provjera i ispravak |
| --- | --- |
| Batch datoteka ima LF prijelome | `od -c` je jedina pouzdana provjera. Pretvoriti u CRLF. [03](03-windows-i-pokretanje.md) |
| Zagrada u `echo` unutar `if (...)` bloka | `cmd.exe` vidi `)` kao kraj bloka. Prijeći na `if exist ... goto OZNAKA`. [03](03-windows-i-pokretanje.md) |
| `^|` na običnom retku | Escapeana cijev vrijedi samo unutar `for /f` i `echo`. [03](03-windows-i-pokretanje.md) |
| Ne-ASCII znak u batch datoteci | Em crtica u ispisu zna srušiti raščlanjivanje. [03](03-windows-i-pokretanje.md) |

Aplikacija je u svim ovim slučajevima radila ispravno cijelo vrijeme.

## Aplikacija radi, ali se prikazuje kao ugašena

Provjera stanja ide na adresu veze umjesto na `127.0.0.1`. Aplikacija vezana na
`0.0.0.0` ne prima spajanje na `0.0.0.0`. [03](03-windows-i-pokretanje.md)

## Zakazani zadatak se nije izvršio

Okidač je bio "pri prijavi", a računalo je ostalo upaljeno i prijavljeno od
jučer, pa nove prijave nije bilo. Koristiti `Daily` uz `StartWhenAvailable`.
[03](03-windows-i-pokretanje.md)

## Kolege ne mogu doći do aplikacije, ili mogu iako pravila kažu da ne bi trebali

Vatrozidom možda upravlja sigurnosni paket treće strane, pa Windows pravila nisu
mjerodavna. Testirati sa stvarnog drugog računala.
[03](03-windows-i-pokretanje.md)

## Virtualna okolina puca na drugom računalu

Isporučena `.venv` je vezana uz točnu verziju Pythona. `run.bat` mora provjeriti
uvoze i po potrebi pregraditi okolinu. [03](03-windows-i-pokretanje.md)

## Paket se ne da instalirati

Gradnja iz izvora pada. Prisiliti gotovi paket:
`pip install --only-binary :all: <paket>`. Provjeriti i verziju Pythona, najnovija
često nema gotove pakete za znanstvene biblioteke. [03](03-windows-i-pokretanje.md)

---

## Baza je izgubila podatke nakon pokretanja testova

`conftest.py` nije postavio `DATABASE_URL` **prije** uvoza aplikacije. Uvoz
stvara engine prema tada važećoj varijabli. Ovo je jednom stvarno obrisalo bazu.
[04](04-baza-i-migracije.md)

## Alembic migracija pada na SQLiteu

Dodavanje stranog ključa traži `op.batch_alter_table`. Ako je migracija već pukla
na pola, baza ima stupce ali `alembic_version` nije pomaknut. Ručno izvršiti
`batch` operaciju, pa `alembic stamp`. [04](04-baza-i-migracije.md)

## Lozinka iz `.env` se ne primjenjuje

Uz `pydantic-settings` varijable idu u objekt postavki, **ne** u `os.environ`.
`os.getenv(...)` vraća `None`. Dodati polje u `Settings`.
[08](08-autentikacija-i-audit.md)

## Sortiranje po datumu daje pogrešan zapis

Datumi su spremljeni kao tekst u obliku `dd.mm.yyyy`, pa se uspoređuju kao niz
znakova. U bazi držati ISO 8601, oblikovati samo pri prikazu.
[04](04-baza-i-migracije.md)

## Nema djelomičnog izdavanja ni zbroja količina

Količina je spremljena kao tekst. Mora biti broj. [04](04-baza-i-migracije.md)

---

## Excel pokazuje broj, program čita `#VALUE!` ili `None`

Datoteka nije bila otvorena u Excelu nakon što ju je sustav generirao, pa formula
nema spremljenu vrijednost. `openpyxl` čita samo spremljeno.
**Rješenje: računati iz sirovih ulaza u kodu.** [05](05-excel-i-podaci.md)

## Greška u formuli koja se u Excelu ne vidi

Dvostruki znak jednakosti (`==`). Automatska korekcija ga tiho popravi pri
otvaranju, pa je vidljiv samo u spremljenoj datoteci, u sirovom XML-u.
[05](05-excel-i-podaci.md)

## `openpyxl` puca na stilovima

Izvozi nekih ERP sustava ruše čitanje na `stylesheet Fill`. Koristiti
`pandas.read_excel(..., engine="calamine")`. [05](05-excel-i-podaci.md)

## `AttributeError` pri čitanju datuma iz Excela

Za ćelije s neobičnim ili nultim datumima vraća se goli `datetime.time`.
Provjeriti tip prije `.date()`. [05](05-excel-i-podaci.md)

## Pretraga vraća besmislene pogotke

`pandas.str.contains` prema zadanim postavkama koristi regularni izraz, pa točka
u upitu postaje divlji znak. Postaviti `regex=False`.
[05](05-excel-i-podaci.md)

## Regularni izraz hvata dio dužeg broja

Šifra od osam znamenki bez granica uhvati komad trinaesteznamenkastog broja.
Koristiti `(?<!\d)\d{8}(?!\d)`. [05](05-excel-i-podaci.md)

## Grupiranje spaja stavke koje nisu iste

Grupira se po početku naziva. Grupirati po šifri, odnosno po stroju i operaciji.
[05](05-excel-i-podaci.md)

## Jedan klik u sučelju traje šest sekundi

Velika datoteka se čita pri svakom zahtjevu. Čitati `read_only=True` u jednom
prolazu, uz predmemoriju po vremenu izmjene, i zagrijati je na startu.
[05](05-excel-i-podaci.md)

## Alat javlja da će zaliha pasti, iako narudžba stiže na vrijeme

Model gleda samo potrošnju. Spojiti potrošnju i dolazak u jednu krivulju, i to i
na nadzornoj ploči, ne samo u detalju. [05](05-excel-i-podaci.md)

---

## Hrvatski znakovi u PDF-u su prazni kvadratići

Ugrađeni ReportLab font ih nema. Registrirati TrueType font, uz pričuvni DejaVu
iz matplotliba za okruženja bez `C:/Windows/Fonts`. [06](06-pdf-word-i-grafika.md)

## Kvačica u PDF-u se ne ispisuje

Arial nema znakove ✓ i ☐. Koristiti boju i podebljanje.
[06](06-pdf-word-i-grafika.md)

## Snimka zaslona PDF-a je prazna

Preglednik bez sučelja ne renderira sadržaj PDF-a. Rasterizirati stranicu preko
`pymupdf`. [06](06-pdf-word-i-grafika.md)

## Preuzimanje datoteke vraća 500 kod hrvatskog naziva

Zaglavlje `Content-Disposition` koristi latin-1. Transliterirati naziv.
[06](06-pdf-word-i-grafika.md)

## PDF se pojavi u stranici umjesto da se preuzme

Odgovor na `hx-post` HTMX ubaci u DOM. Koristiti `fetch` i `blob`.
[06](06-pdf-word-i-grafika.md)

## Detekcija oblika u PDF-u daje pogrešne dimenzije ili razlomljeno područje

Rasterski pristup pada jer linije kota dijele separaciju s reznom linijom, a
radijalne linije presijecaju zaobljene etikete. Filtrirati vektorske putanje po
tome leži li rub na separaciji rezne linije. [06](06-pdf-word-i-grafika.md)

## Izračun daje red veličine promašaja

Provjeriti postavku modela prije podataka. U izračunu potrošnje boje suvišan
faktor površine davao je otprilike deset puta premale brojeve.
[06](06-pdf-word-i-grafika.md)

## Program radi kod mene, kod kolege ne

Kopiran je samo `.exe`, a ne cijela mapa. Kod `onedir` gradnje mapa `_internal`
sadrži biblioteke i pakirane alate. Uz to, zamrznuti program ne smije računati
zadanu mapu iz `Path(__file__).parent`. [06](06-pdf-word-i-grafika.md)

---

## Ruta se ne poziva, javlja grešku pretvorbe u broj

Ruta `/{id}` je registrirana prije rute s tekstualnim segmentom i hvata je.
Registrirati konkretne rute prije parametarskih. [07](07-sucelje-htmx-alpine.md)

## Polje se izračunava tek kad kliknem izvan njega

`hx-trigger="change"` okida se na gubitak fokusa. Dodati
`keyup changed delay:400ms`. [07](07-sucelje-htmx-alpine.md)

## Enter u obrascu ne šalje ništa

Obrazac s dva polja i bez gumba za slanje ne šalje se na Enter. Premjestiti HTMX
atribute na samo polje, uz `hx-include`. [07](07-sucelje-htmx-alpine.md)

## Padajući izbornik se ne da zatvoriti

Gumb je izvan panela, pa `@click.outside` na panelu broji klik na gumb kao vanjski.
Direktivu staviti na zajedničkog roditelja. [07](07-sucelje-htmx-alpine.md)

## Izbornik je odrezan unutar tablice

`overflow-x-auto` na tablici reže sadržaj koji izlazi iz nje.
[07](07-sucelje-htmx-alpine.md)

## Sadržaj nestane nakon osvježavanja dijela stranice

Parcijalni predložak koristi varijablu koju roditelj ne prosljeđuje. Čitati preko
objekta. [07](07-sucelje-htmx-alpine.md)

## Promjena redoslijeda prestane raditi nakon prve zamjene

Skripta koja inicijalizira SortableJS je izvan parcijala, pa se ne izvrši ponovno.
[07](07-sucelje-htmx-alpine.md)

## Filtar za broj daje čudan rezultat

Filtar veže jače od zbrajanja: `a + b|hr(2)` primijeni se samo na `b`. Koristiti
zagrade. [05](05-excel-i-podaci.md)

## Funkcija iz predloška ne postoji u drugom modulu

Svaki router je stvorio vlastitu Jinja okolinu. Koristiti jednu zajedničku iz
`app/core/templating.py`. [02](02-skelet-aplikacije.md)

## Kopiranje u međuspremnik ne radi

`navigator.clipboard` ne radi preko nesigurne veze. Dodati pričuvu preko skrivenog
polja. [05](05-excel-i-podaci.md)

## Graf s vremenskom osi ne radi

Adapter za datume zna biti nepouzdan. Koristiti linearnu os s vremenskim oznakama
u milisekundama. [06](06-pdf-word-i-grafika.md)

---

## Brojanje ruta pokazuje premalo, iako rutanje radi

Novije verzije FastAPI-ja ne spljošte rute, pa `len(app.routes)` pokazuje broj
routera. Provjeravati `TestClient`-om, ne brojanjem. [02](02-skelet-aplikacije.md)

## Predložak puca uz `TypeError: unhashable type: 'dict'`

Novija Starlette verzija traži `templates.TemplateResponse(request, name, context)`,
sa zahtjevom kao prvim pozicijskim argumentom.

## Zakrpa je "prošla", ali ništa se nije promijenilo

Skripta za izmjenu koda nije našla traženi obrazac i tiho je prošla. Uvijek
dodati `assert`. [01](01-nacela-rada.md)

## Heredoc s hrvatskim tekstom puca u ljusci

Skripte s hrvatskim tekstom pisati kao datoteku pa je pokrenuti, ne kroz heredoc.

---

## Plava boja i dalje viri nakon promjene palete

Boje su bile upisane izravno u pravila umjesto kroz varijable.
[10](10-web-stranice-i-dizajn.md)

## Font izgleda drugačije nego što je zadano

Tražena je težina koja nije dohvaćena s Google Fontsa, pa preglednik uzima
najbližu. Koristiti točno dohvaćene težine. [10](10-web-stranice-i-dizajn.md)

## Cijena se ne vidi na mobitelu

Informacija je skrivena iza prelaska mišem, kojeg na dodirniku nema. Bitno mora
biti vidljivo uvijek. [10](10-web-stranice-i-dizajn.md)

## Blok s izmjerenim brojkama prikaže pola redova

| Uzrok | Provjera i ispravak |
| --- | --- |
| Stranica je otvorena kao `file://` | Performance API ne prijavljuje `transferSize` za lokalne datoteke, pa se redovi s kilobajtima i brojem zahtjeva sakriju. Posluživati preko `python -m http.server 8080 --bind 127.0.0.1`. [15](15-dizajn-bez-ai-tragova.md) |
| Vanjski izvor bez `Timing-Allow-Origin` | Ista posljedica na pravoj domeni. Ne prikazivati nulu nego sakriti red, inače stranica tvrdi nešto neistinito |

## Spremanje pregazi tuđu izmjenu iako postoji provjera

| Uzrok | Provjera i ispravak |
| --- | --- |
| Vrijeme izmjene uzeto u cijelim sekundama | Dva spremanja u istoj sekundi prođu kao da nije bilo promjene. Uzeti milisekunde: `int(os.stat(p).st_mtime * 1000)`. [17](17-skillovi-i-baza-znanja.md) |

## Datoteka koja nije smjela biti javna pojavila se na stranici

| Uzrok | Provjera i ispravak |
| --- | --- |
| GitHub Pages radni tok objavljuje korijen repozitorija (`path: '.'`) | Sve što je u gitu je javno. Nacrte i verzije kandidata **ne dodavati u git**, ostaviti ih nepraćene. Nakon objave provjeriti da vraćaju 404 |

## Provjera u ljusci tiho preskoči pola koraka

| Uzrok | Provjera i ispravak |
| --- | --- |
| `grep -c` vezan s `&&` | Kad `grep -c` nađe nula pogotaka, ispiše `0` **i vrati izlazni kod 1**, pa se ostatak lanca ne izvrši. U provjerama koristiti `;` umjesto `&&`, ili `if` blok |

## Naslov s velikim slovima se slijepi pri lomu u dva reda

| Uzrok | Provjera i ispravak |
| --- | --- |
| `line-height` ispod 1.0 na verzalu | Velika slova nemaju donje dužine, pa vrhovi drugog reda dodiruju osnovnu liniju prvog. Pod je `1.0`, ugodno `1.02`–`1.08`. [15](15-dizajn-bez-ai-tragova.md) |

## Animacija radi, ali stranica poskakuje

| Uzrok | Provjera i ispravak |
| --- | --- |
| Animira se `width`, `padding` ili `margin` | Svaki kadar prisiljava preračun rasporeda. Za liniju koja se izvlači koristiti `transform: scaleX()` uz `transform-origin: left`. [15](15-dizajn-bez-ai-tragova.md) |
