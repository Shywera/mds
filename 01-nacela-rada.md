# 01 Načela rada

## Jezik i ton

Sve prema korisniku ide na **hrvatskom književnom jeziku**, u profesionalnom tonu.
Kod, nazivi varijabli i tehničke oznake ostaju na engleskom kada je to uobičajeno,
ali sučelje, dokumentacija i poruke idu na hrvatski.

**Bez em crtica** (`—`) u tekstu. To je najprepoznatljiviji potpis strojno
generiranog teksta. Umjesto toga zarez, dvotočka, točka ili preoblikovana
rečenica. Dopušteno je:

- en crtica u brojčanim rasponima: `6-8 tjedana`, `1-2 dana`
- `·` kao dizajnerski razdjelnik u oznakama sučelja
- `|` kao razdjelnik u naslovima stranica

Za marketinške tekstove vrijedi i **suosjećajan ton**: krenuti od problema koji
kupac ima, ne od popisa vlastitih sposobnosti. Nema prodajnog pritiska.

## Kada pitati, a kada raditi

Pitati unaprijed kada:

- operacija traje dulje od minute prema dijeljenom sustavu koji drugi koriste
- odluka je poslovna, ne tehnička (cijene, pozicioniranje, tko ima pristup)
- postoji rizik da se prepiše ili obriše nešto što nema kopiju

Raditi bez pitanja kada je odluka tehnička i lako se mijenja. Bolje je isporučiti
razumnu pretpostavku i jasno je označiti nego stati i čekati.

## Rad prema sporim i dijeljenim sustavima

Interni ERP sustavi u proizvodnji su tipično spori i dijeljeni. Dok jedan izvoz
teško radi, usporava rad svima.

Pravila:

- jedan pokušaj od 30 do 60 sekundi, pa javiti što se dogodilo
- ne postavljati timeout od nekoliko minuta "za svaki slučaj"
- prije bilo čega dužeg pitati i predložiti termin izvan radnog vremena
- **prvo napraviti najjeftiniju provjeru koja odgovara na pitanje**

Zadnje pravilo se višestruko isplatilo. Umjesto punog izvoza tablice, prvo se
pročita 101 vidljivi redak. Tako je i otkriveno da izvještaj ima opciju "9999
redaka", čime je cijela tablica skinuta u nešto manje od pet minuta umjesto nikad.

## Dokumentacija ide uz kod

Uz svaku promjenu ponašanja ažurira se dokumentacija u istom prolazu. Bez toga
dokumentacija zaostane za tjedan dana rada i postane teret umjesto pomoći.

Provjereni raspored:

- `CLAUDE.md` u korijenu projekta: stanje modula, zamke, kako pokrenuti
- `docs/NN-modul-<naziv>.md`: opseg, tablice s popisom polja, rute, veze, status
- `README.md`: kako drugi čovjek pokreće aplikaciju na svom računalu

Formalna dokumentacija u Wordu ili PDF-u je teža i regenerira se samo na izričit
zahtjev. Markdown je živa dokumentacija.

## Testiranje prije nego se kaže "gotovo"

"Gotovo" ne znači "kod je napisan". Za svaki tok postoji provjera:

- `TestClient` za rute, s privremenom bazom
- Playwright ili preglednik za ono što se mora vidjeti
- rasterizacija PDF-a kada se provjerava izgled ispisa

Ako se javlja da testovi prolaze, prethodno ih treba stvarno pokrenuti. Ako
nešto nije provjereno, to se kaže otvoreno.

## Zakrpe uvijek s provjerom

Skripte koje mijenjaju postojeći kod moraju sadržavati `assert` ili barem ispis
koji potvrđuje da je zamjena stvarno izvršena.

Naučeno na primjeru: zakrpa koja je trebala postaviti jezik ponude tiho je
preskočena jer se traženi obrazac nije podudarao. Greška se pokazala tek dva
koraka kasnije, kada je izlaz bio pogrešan a uzrok već zaboravljen.

## Prekid u tijeku rada

Ako korisnik prekine dugu operaciju, to nije neuspjeh nego povratna informacija
da je pristup bio prekrup. Sljedeći pokušaj mora biti uži i brži.
