# 12 Domena: tiskarstvo etiketa

Poglavlje čuva domensko znanje koje se ponavlja kroz većinu projekata. Nazivi
tvrtki i kupaca su izostavljeni, ostaju pojmovi, veze i formule.

## Osnovni pojmovi

| Pojam | Značenje |
| --- | --- |
| Naklada | broj komada u nalogu |
| Arak | list papira koji ulazi u stroj |
| Kontakata | broj etiketa na jednom arku |
| Otisak | jedan prolaz arka kroz stroj |
| Normativ | koliko araka ili etiketa stroj obradi na sat |
| Priprema | vrijeme namještanja stroja prije posla |
| Pranje | vrijeme čišćenja između poslova |
| Napust | rub arka koji se ne koristi |
| Štancanje | izrezivanje etikete u konačni oblik |
| Dorada | sve poslije tiska: rezanje, štancanje, pakiranje |
| Mjesto troška | oznaka koja govori na kojem stroju materijal smije ići |
| Komplet | dvije ili više etiketa koje idu zajedno, primjerice prednja i stražnja |

Pozicije etiketa na boci: trbušna, leđna, vratna, grljak.

## Vrste strojeva

- **Tiskarski strojevi**, ofsetni, opisani brojem boja i time imaju li lak i UV.
- **Rezači**, giljotinski i programski.
- **Štance**, za izrezivanje konačnog oblika.

Za planiranje je bitno da se ne može svaki posao raditi na svakom stroju.

## Pravilo dopuštenosti stroja

Provjereno pravilo, izvedeno iz podataka koji već postoje i ne traži novu tablicu:

```
stroj je dopušten ako:
    stroj ∈ mjesta troška materijala
    format naloga ≤ najveći format stroja (uz dopuštenu rotaciju)
    broj boja naloga ≤ broj boja stroja
    ako nalog traži UV lak → stroj mora imati UV
    ako nalog traži lak → stroj mora imati lak
```

Kada stroj nije dopušten, korisniku treba pokazati **razlog**, ne samo izostaviti
stroj s popisa.

## Izračun vremena tiska

Formula potvrđena na stvarnom rasporedu:

```
otisaka  = ceil(naklada / kontakata) + otpad
RAD      = ceil(otisaka / normativ * 60 / 15) * 15      # minute, zaokruženo na 15
SATI     = priprema + RAD + pranje
```

Normativ, dakle brzina u arcima na sat, **ovisi o vrsti papira**. Metalizirani i
bijeli papir imaju različite brzine.

Zaokruživanje na petnaest minuta nije kozmetika, nego se tako planira u praksi.

## Raspored po stroju

Svaki redak je jedan nalog, a vremena se ulančavaju:

```
POČETAK naloga = ZAVRŠETAK prethodnog naloga
```

Pri promjeni redoslijeda ili bilo kojeg ulaza koji utječe na trajanje, cijeli
lanac se preračunava.

Nalog koji je gotov ostaje u planu, ali se vizualno odvoji. U Excelu se to radi
žutom bojom retka, pa isto vrijedi i u aplikaciji.

**Zašto se planiranje teško seli iz Excela:** planer ručno upisuje prazninu preko
noći i vikenda, jer sustav nema kalendar smjena. Dok kalendara nema, aplikacija
može samo prikazivati plan, ne i sastavljati ga.

Razuman redoslijed preseljenja:

1. aplikacija prikazuje plan, u Excelu se i dalje planira
2. aplikacija savjetuje, planer prijedloge primjenjuje sam
3. tek s kalendarom smjena planiranje se stvarno seli

## Montaža etiketa na arak

Cilj je smjestiti dvije vrste etiketa tako da bude najviše **cijelih kompleta**.

Postupak: proći sve moguće brojeve stupaca za etiketu A, ostatak širine popuniti
stupcima etikete B, odabrati raspored s najvećom vrijednosti `min(ukupno_A, ukupno_B)`.

Broj etiketa na arku, za jednu vrstu:

```
INT(širina_arka / bruto_širina_etikete) × INT(visina_arka / bruto_visina_etikete)
```

Baza papira nosi format i **rubove po vrstama**, jer se razlikuju. Aluminijski
papir ima drugačiji donji rub od bijelog.

## Skladište

Provjeren model: paleta, pozicija, zaprimanje, izdavanje, inventura, prioriteti
smještaja.

Oznaka pozicije nosi zonu, regal, poziciju i visinu, primjerice `A13P9V5`.
Brojevi se **ne nadopunjuju nulama**, pa se sortiranje mora raditi po raščlanjenim
brojevima, nikako po tekstu.

### Zaprimanje i izdavanje

- Zaprimanje: sken oznake, pa odabir pozicije. Kod više paleta sustav predloži
  popis pozicija, a skladištar potvrđuje jednu po jednu.
- Izdavanje: po količini, ne po paleti. Sustav uzima **cijele palete** po pravilu
  FIFO ili FEFO dok zbroj ne pokrije traženo. Višak se vraća kao nova paleta,
  bez ručnog uređivanja količine.
- Redoslijed FIFO uzima **datum iz izvornog sustava**, ne datum lokalnog upisa,
  inače vraćeni ostatak izgubi svoje mjesto u redu.

### Nepotpuna paleta

Ako na poziciju stane još robe, i nova i sve postojeće palete na toj poziciji
postaju nepotpune, bez obzira na to što je korisnik označio. Logika je
jednostavna: ako stane još, nijedna nije puna.

### Prioriteti smještaja

Prioriteti se vode **po šifri**, ne po formatu, jer više vrsta i dobavljača dijeli
isti format.

Načini smještaja koji imaju smisla ljudima su prostorni: bliže ulazu, bliže kraju,
popuni započete pozicije. Apstraktni nazivi se ne koriste.

## Kvaliteta i reklamacije

Model koji pokriva zahtjeve norme:

- reklamacija s vrstom (interna, kupac, dobavljač), statusom i rokom
- analiza uzroka metodom pet zašto
- CAPA mjere, korektivne i preventivne, s rokom i provjerom
- klasifikacija defekta, izvora i težine
- troškovi nekvalitete po kategorijama, uz oznaku tko ih snosi i jesu li naplativi
- zahtjev prema dobavljaču s vlastitim statusom i iznosom priznatog

Dvije stvari koje se lako previde:

**Provjera učinkovitosti prije zatvaranja.** Norma traži da se zabilježi narav
nesukladnosti, poduzeta radnja i rezultat. Ako učinkovitost nije potvrđena,
predmet se ne smije zatvoriti nego se vraća u stanje riješeno.

**Ocjena rizika** kao umnožak težine, učestalosti i mogućnosti otkrivanja, s
pragovima za nisku, srednju i visoku razinu.

Glavni dijagram za analizu je Pareto po kategoriji defekta, s kumulativnom
krivuljom.

## Nabava i zalihe

Minimum se određuje na tri načina: fiksni broj, bilo koja pozitivna vrijednost,
ili zbroj svih vrijednosti iznad zadanog praga.

```
fali = max(0, minimum - (zaliha + naručeno))
```

Za projekciju vrijedi pravilo iz [05](05-excel-i-podaci.md): spojiti potrošnju i
dolazak u jednu krivulju, inače alat lažno uzbunjuje.

## Kalkulacije

Kalkulacija sadrži troškove materijala i rada po strojevima i operacijama, pa
prodajnu cijenu izvedenu iz marže:

```
prodajna vrijednost = (marža + 1) × ukupni trošak
```

Kod kompleta se ukupni iznos dijeli po **stupcu udjela**, ne po broju proizvoda.
Kod ravnomjerne podjele to je isto kao dijeljenje s dva, ali udjeli često nisu
ravnomjerni, pa svaka etiketa dobiva svoju cijenu i svoj redak.
