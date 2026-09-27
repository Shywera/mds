# 16 Brief za stranicu

Zahtjev "napravi mi stranicu kao ova" propada na dva načina. Ili je premalo
činjenica, pa je rezultat općenito pogađanje, ili je puno pridjeva i nijedan broj,
pa rezultat ne izgleda ni blizu onome što je naručitelj vidio u glavi.

Rješenje je obrazac koji se ispuni prije nego se napiše ijedan red koda.

## Obrazac

`SITE-SPEC-TEMPLATE.md`: sedamnaest odjeljaka, ponovno upotrebljiv za bilo koju
temu. Nastao je razlaganjem jednog konkretnog prompta za stranicu proizvoda na
polja, tako da se pojmovi poopće:

| Konkretno u izvoru | Polje u obrascu |
| --- | --- |
| okus (klasični, limeta) | **varijanta**: bilo koje stanje između kojih se prebacuje |
| limenka u središtu | **središnji objekt**: 3D model, PNG, video, shader, ili sama tipografija |
| višnje i listovi koji lebde | **ukrasni slojevi**, s parallax množiteljem po sloju |
| mjehurići koji se dižu | **ambijentalne čestice**: interval, veličina, prozirnost, trajanje, putanja |
| koreografija zamjene okusa | **popis kadrova**: greda, trajanje, easing, početak |

Ostali odjeljci su ljuska stranice, paleta, karta rasporeda, tipografija, blokovi
sadržaja, interakcije, učitavanje, prilagodba mobitelu, popis resursa, tekst,
ograničenja i predaja.

## Dva prekidača koja odlučuju sve ostalo

Samo na ova dva vrijedi čekati odgovor. Ostalo se izvede ili pretpostavi.

1. **Ponašanje stranice**: jedan zaključan zaslon bez skrolanja / obično skrolanje /
   skrolanje s pristajanjem / vodoravno.
2. **Razina detalja**:
   - *točna replika* — svaka brojka je zadana, slijedi se doslovno,
   - *čvrst okvir* — dane su paleta, tekst i resursi, vrijednosti gibanja se biraju,
   - *osjećaj* — dana je tema, ostalo se komponira.

## Ispuni iz repozitorija, ne iz čovjeka

Ako stranica već postoji, obrazac se ispunjava **čitanjem koda**: varijable, fontovi,
tekst, cijene, interakcije. Nikad ne pitati za vrijednost koja stoji u CSS datoteci.

Kod kai-sol stranice tako je nastao ispunjeni brief u kojem je sve iz repozitorija,
a osam redova koji su bili prosudba, a ne činjenica, označeno je posebno i skupljeno
u popis otvorenih odluka na kraju. Naručitelj tada presuđuje samo o tih osam, ne o
cijelom dokumentu.

## Najmanji ispun

Kad nema vremena, ovih deset odgovora je dovoljno za cijelu stranicu:

```
1. Tema                     6. Podloga: tamna ili svijetla + osnovna nijansa
2. Naziv stranice           7. Glavni naslov, točan tekst
3. Rečenica pitcha          8. Jedan poziv na akciju
4. Osjećaj, tri pridjeva    9. Skrolanje ili jedan zaslon
5. Akcentna boja (hex)     10. Središnji objekt + adresa ako postoji
```

## Slabo i jako zadano

Razlika između pogađanja i replike je isključivo u desnom stupcu.

| Polje | Slabo | Jako |
| --- | --- | --- |
| Akcent | "roza" | `#fbcfe8`, tekst na njoj `#011d17` |
| Podloga | "tamno zelena" | radijalno: `#0b8a78` 0 %, `#044e3b` 50 %, `#011411` 100 % |
| Naslov | "nešto pamtljivo" | red 1 `Pure`, red 2 `Zero` u akcentu, `clamp(5rem,10vw,12rem)`, `line-height 0.8` |
| Hover | "neka se pomakne" | `translateY(-30px) rotate(-12deg) scale(1.15)` kroz `0.5s cubic-bezier(0.34,1.56,0.64,1)` |
| Prijelaz | "neka se kul zavrti" | 0→360° uz blur 0→15px kroz `0.6s power2.in`, zamjena teksture u vrhu, pa 360→720° uz blur→0 kroz `1.5s back.out(0.7)` |
| Čestice | "mjehurići" | PNG, jedan na `400ms`, `10–30px`, prozirnost `0.2–0.6`, dizanje `-110vh` uz `+30px` zanošenja i `360°` kroz `4–10s` |

## Resursi se ne izmišljaju

3D modeli, fotografije i teksture ne mogu nastati iz teksta. Ako ih naručitelj nema,
odabire se zamjena i **kaže se koja**:

1. središnji objekt u čistom CSS-u ili SVG-u (limenke, boce, telefoni, kartice),
2. osnovna tijela iz three.js s materijalima umjesto pravog modela,
3. besplatni vanjski izvori, uz prihvatanje da se mogu promijeniti,
4. vidljivi okviri s natpisom što tu ide,
5. gradnja na imenima resursa, datoteke dolaze kasnije.

**Nikad** ne poslati izmišljenu fotografiju kao da je konačna, i nikad ne nacrtati
lažni okvir preglednika oko makete. Vidi [15](15-dizajn-bez-ai-tragova.md).

## Tekst

Činjenice, pa stop. Bez izazivanja, bez superlativa. "Interaktivno, ima zvuk, dvije
minute" je bolje od "kliknite ako se usudite i pojačajte zvuk". Samopouzdanje je
navesti činjenicu; reklama je moliti da se vjeruje.

Za hrvatske stranice: obraćanje na *vi*, kratke rečenice, prvo se imenuje problem
kupca pa onda usluga, cijene se pokazuju a ne skrivaju za "kontaktirajte nas".

## Predaja

1. Graditi kao **novu datoteku kandidata** (`index-v4.html`), nikad preko žive
   stranice, osim ako je zamjena izričito zatražena.
2. Posluživati lokalno preko HTTP-a, ne `file://`, pa otvoriti u pregledniku.
3. Objaviti kao privatni pregled s pripadajućim CSS-om i JS-om, da se može pogledati
   na mobitelu, i dati vezu.
4. Izvijestiti što je izmišljeno, što je uklonjeno i zašto, i što je ostalo otvoreno.
5. Na živu stranicu ide tek na izričit zahtjev, pa onda po kontrolnoj listi iz
   [14](14-kontrolne-liste.md) i po pravilima iz [11](11-git-i-objava.md).

## Zamke

| Zamka | Kako se pokazuje |
| --- | --- |
| Ispunjavanje obrasca umjesto naručitelja, bez oznake | Pola stranice počiva na pretpostavkama koje nitko nije potvrdio. Svaka izmišljena vrijednost mora biti označena i skupljena na kraju |
| Preuzimanje obrasca kao svetog | Obrazac je popis pitanja, ne ugovor. Ako polje ne odgovara temi, briše se |
| Redizajn koji samo premješta sekcije | Čita se kao da se nije ništa dogodilo. Redizajn znači **drugi vizualni jezik**, ne drugi redoslijed |
| Ispunjeni brief u istoj datoteci kao prazni obrazac | Sljedeći projekt nema od čega početi. Prvo `cp`, pa ispunjavanje |
