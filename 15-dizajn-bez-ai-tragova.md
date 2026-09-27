# 15 Dizajn bez AI tragova

Stranice koje generira jezični model dijele prepoznatljiv otisak. Problem nije
u tome da su ružne, nego da su **iste**: posjetitelj u sekundi prepozna da nitko
nije odlučivao, samo popunjavao. Za agenciju koja prodaje dizajn to je najskuplja
moguća poruka.

Ovo poglavlje je popis tragova i ispravaka. Nije stvar ukusa, nego prepoznatljivosti.

## Tragovi u tipografiji

| Trag | Zašto pada | Ispravak |
| --- | --- | --- |
| Kurzivna riječ unutar uspravnog naslova (`Web stranica koja *stvarno prodaje*`) | Najpouzdaniji pojedinačni trag. Čita se kao "trudim se izgledati uređivački" | Naslovi su **uspravni**. Naglasak nosi akcentna boja i nacrtana linija ispod riječi |
| Cijeli display font u kurzivu | Isto, samo posvuda | Kurziv ostaje samo za naglasak u tekućem tekstu |
| Oznaka nad svakom sekcijom (`01 / USLUGE`, `02 / CIJENE`) | Izgleda kao poglavlja, čita se kao tik. Kad je svaka sekcija numerirana, ni jedna nije | Oznake su **ugašene po defaultu**. Dopuštene samo kad je sadržaj stvarno redni, i najviše dvije po stranici |
| Oznaka **lijevo**, naslov **desno**, u istom redu | Takozvani viseći naslov. Za uređivačke stranice najjači trag da je sve iz predloška | Ako oznaka postoji, naslov ide **ispod nje, u istom stupcu**. Nikad dvostupčano |
| Više od tri obitelji fonta | Display, tekst, pa još mono i još jedan display | Dvije obitelji, treća samo kao izdvojeni registar (npr. logotip) |
| Velika slova s `line-height` manjim od 1.0 | Velika slova nemaju donje dužine, pa se pri lomu vrhovi slijepe s prethodnim redom | Pod za velika slova je `1.0`, ugodno je `1.02` do `1.08` |

## Tragovi u strukturi

| Trag | Ispravak |
| --- | --- |
| Hero visok `100vh` sa svime centriranim na istoj osi | Najviše dva elementa centrirana, ostalo razlomiti. Donji unutarnji rub hera barem 1.3 puta veći od gornjeg, da hero sjedne u stranicu |
| Tri jednaka stupca kartica s ikonom nad naslovom | Promijeniti oblik: popis, diptih, tablica, redni popis |
| Kartica unutar kartice | Jedna razina. Hairline linija radi isti posao |
| Podnožje: četiri stupca linkova, red ikona društvenih mreža, sitna autorska crta | Zaključna rečenica, pa logotip i nekoliko linkova u sitnom tekstu. Četiri stupca samo na stvarnom čvorištu |
| Navigacija: logotip lijevo, četiri linka, gumb desno, hairline ispod | Puni izbornik preko zaslona, plutajuća pilula, bočna traka, masthead. Bilo što osim defaulta |
| Sve sekcije s istim unutarnjim rubom | Ritam se pravi razlikom. Tri razine visine sekcije su dovoljne |
| Ista struktura na dvije različite stranice | Prije pisanja koda odabrati oblik stranice i **zapisati odabir u komentar na vrhu CSS-a**. Sljedeći put mora biti drugi oblik |

## Nacrtani lažni okvir

Lažna traka preglednika (pilula s adresom i tri kružića), lažni okvir mobitela s
urezom, lažni prozor s kodom, lažna traka uređivača koda. Sve nacrtano u HTML-u
ili SVG-u.

**Zašto pada:** posjetitelj **već ima** preglednik, mobitel i uređivač. Crtanje
istog okvira unutar stranice je kao fotografija okvira za sliku unutar pravog
okvira. Uz to je i netočno: adresa je izmišljena, kružići nisu pravi, urez je
pogrešnog oblika.

**Ispravak:** prava snimka zaslona u `<figure>` s hairline rubom, ili bez okvira,
pa sadržaj stoji sam. Ako nema snimke, onda nema ni okvira.

## Proračun gibanja

Najviše **tri primitive gibanja** na cijeloj stranici. Rezati prije nego dodavati:
ako uklanjanje animacije ne odnosi nikakvu informaciju, animacija ne treba postojati.

Za kai-sol.com te tri su: jedan usklađen ulaz pri učitavanju, akcentna linija koja
se izvuče na hover, i mekani sjaj koji prati kursor.

| Pravilo | Obrazloženje |
| --- | --- |
| Animirati samo `transform` i `opacity` | Sve ostalo prisiljava preračun rasporeda |
| Nikad `width`, `height`, `top`, `left`, `margin`, `padding` | Isto. Umjesto širine koristiti `transform: scaleX()` s `transform-origin` |
| Nikad `transition: all` | Navesti svojstva, inače se animira i ono što ne treba |
| Tri imenovana easinga, nikad goli `ease` | `--ease-out`, `--ease-in`, `--ease-in-out` |
| Bez odskoka na promjenama stanja sučelja | Odskok je za fizičke interakcije, ne za gumb |
| Fokusni prsten se **ne** pojavljuje animirano | Tipkovnica traži trenutni pokazatelj |
| Nikad fade-up na svakoj sekciji pri skrolanju | Jedan usklađen ulaz pri prvom učitavanju, dalje sadržaj samo stoji |
| `prefers-reduced-motion` gasi prostorno gibanje | Prijelaz na kratki fade, do 150 ms. Boje ostaju, gibanje staje |

**Zamka:** animiranje `padding-left` na hover izgleda bezopasno i lako promakne
u pregledu koda, a ruši oba pravila odjednom: animira raspored **i** slaže treći
istovremeni efekt na isti element.

## Boje i razmaci

- Sve boje i svi fontovi **preko varijabli**. Jedna ostavljena `oklch(...)` ili
  `#hex` u pravilu znači da je paleta odabrana pa zaboravljena.
- OKLCH umjesto heksadekadskog zapisa. Svjetlina je predvidljiva, pa se nijanse
  izvode bez pogađanja. Postojeća paleta se **prevede**, ne mijenja.
- Neutralne boje **nisu čiste sive**. Minimalna kroma oko `0.005`, nagnuta prema
  akcentu, inače površina izgleda mrtvo.
- Akcent pokriva **manje od 5 %** površine zaslona. Označava jednu stvar, ne puni.
- Razmaci idu po skali od 4 točke, s imenima. `padding: 17px` je trag.
- Mjera teksta između 45 i 75 znakova. Ispod je isprekidano, iznad se oko gubi.

## Istinitost brojki

Nijedna brojka se ne izmišlja da ispuni raspored. Dopuštene su samo tri vrste:

1. brojka koju je dao klijent,
2. brojka izmjerena u pregledniku posjetitelja,
3. obećanje koje tvrtka već javno daje (npr. odgovor u 24 sata).

Sve ostalo se izostavlja ili zamijeni oznakom da podatak treba potvrditi.
`+47 % konverzije` i `više od 50.000 zadovoljnih korisnika` su trag u trenutku
kad su izmišljeni.

Dobar obrazac: izmjeriti **vlastitu stranicu** u pregledniku posjetitelja preko
Performance API-ja i prikazati vrijeme do prikaza, prenesene kilobajte, broj
zahtjeva i broj vanjskih skripti. Ako preglednik ne da podatak, red se **sakrije**
umjesto da prikaže nulu.

## Pristupačnost kao pod, ne kao želja

- `overflow-x: clip` na `html` **i** `body`. `clip`, ne `hidden`, jer `hidden`
  ubija `position: sticky` na potomcima.
- Svaki interaktivni element ima: osnovno, hover, `:focus-visible`, `:active` i
  onemogućeno stanje. Dva stanja nisu dovoljna.
- Tekst 4.5:1, veliki tekst i fokusni prsteni 3:1, **prema izračunatoj podlozi**,
  ne prema pozadini stranice. Najčešći promašaj je prigušeni tekst na kartici
  koja je promijenila podlogu.
- Nijedan klikabilni natpis ne prelazi u dva reda, od 320 px nadalje.
- Stupci rešetke koji nose sliku ili dugu riječ: `minmax(0, 1fr)`, nikad goli `1fr`.
- Naslovi u display veličini: `overflow-wrap: anywhere; min-width: 0`.
- Ukrasni SVG i CSS grafika dobivaju `aria-hidden="true"` ili pristupačno ime.

## Kako se to provodi u praksi

Postoji vanjski skill `hallmark` (`npx skills add nutlope/hallmark`) koji ovo
kodificira: bira oblik stranice prije pisanja koda, pa nakon gradnje propušta
izlaz kroz 58 provjera. Vrijedi ga pustiti, ali s dvije napomene:

1. Provjere se pokreću **nakon** gradnje, ne prije. Prije gradnje se čita popis
   tragova, ne popis provjera.
2. Skill je općenit. Kad se njegovo pravilo sukobi s odlukom o marki, odluka o
   marki pobjeđuje, ali se sukob **izgovori naglas** pa neka klijent presudi.

Konkretan primjer: potpis kai-sol stranice bio je kurzivna akcentna riječ u
naslovu. To je po popisu trag. Odluka je bila ukloniti kurziv, jer je taj potez
i sam nastao iz generiranog nacrta, a ne iz svjesnog odabira.

## Zamke iz stvarnog rada

| Zamka | Kako se pokazuje |
| --- | --- |
| Ukrasna linija ispod riječi zadana u `em` | Na display veličini 0.06 em je pet i više piksela, pa izgleda kao debelo podcrtavanje. Zadati u pikselima, 1 do 2 |
| Prigušena siva koja je prošla na papiru, pada na kartici | Kontrast se mjeri prema izračunatoj, a ne prema osnovnoj podlozi |
| Paleta prevedena u OKLCH, ali jedna vrijednost ostala umetnuta u pravilu | Promjena teme je ne dohvati. Provjera: `grep -cE "#[0-9a-fA-F]{3,6}\|oklch\(\|rgb\(" stil.css` mora dati nulu izvan datoteke s varijablama |
| Dvije ljepljive trake na `top: 0` | Obje se zalijepe na vrh i preklope. Sekundarna dobiva `top: var(--visina-trake)` i niži `z-index` |
| Mjerenje preko `file://` | Performance API ne prijavljuje prenesenu veličinu, pa blok s brojkama sakrije pola redova i izgleda pokvareno. Uvijek posluživati preko HTTP-a |
