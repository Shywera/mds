# 10 Web stranice i dizajn

## Tehnologija za javne stranice

Statični HTML, CSS i JavaScript, bez koraka gradnje i bez npm-a. Objavljuje se
na GitHub Pages preko Actions radnog toka, uz `CNAME` za vlastitu domenu.

Prednost je što stranica radi otvaranjem `index.html`, a objava je jedan `push`.

### Zašto ne Tailwind s CDN-a na javnoj stranici

Play CDN kompajlira u pregledniku. To je oko 380 kB JavaScripta i bljesak
neoblikovanog sadržaja pri učitavanju. Za agenciju koja prodaje brzinu to je
kontraproduktivno.

Ako Tailwind mora biti, kompajlirati ga lokalno. Za male stranice je ručno pisan
CSS s varijablama jednako brz za rad i daje potpunu kontrolu.

## Dizajn sustav u varijablama

Sve boje, fontovi i razmaci u `:root`, jedna datoteka po stranici uz zajedničku
osnovu:

```css
:root {
  --bg: #08090a;
  --text: #f2f1ec;
  --accent: #14c99a;
  --font-display: "Instrument Serif", Georgia, serif;
  --font-body: "Inter", system-ui, sans-serif;
}
```

Time se cijela vizualna promjena radi na jednom mjestu. Kroz tri iteracije
stranice mijenjala se paleta i tipografija, a struktura je ostala.

**Zamka:** ako se boje pišu izravno u pravila (`rgba(91,140,255,.18)`), promjena
palete ih ne dohvati i plava ostane razasuta po datotekama nakon što je odlučeno
da plave više nema. Sve boje moraju ići kroz varijable.

## Odabir fontova

Provjerena kombinacija je **serif za naslove i sans za tijelo**. Serif daje
karakter i dojam ozbiljnosti, sans drži čitljivost.

Kod fontova s promjenjivom težinom paziti: ako se s Google Fontsa dohvate samo
određene težine (300, 400, 500, 600), a u CSS-u se traži 420, preglednik uzima
najbližu učitanu. Bolje je koristiti točno one težine koje su dohvaćene.

## Struktura konverzijske stranice

Redoslijed koji slijedi način na koji čovjek odlučuje:

1. **Hero** s jasnom vrijednosnom porukom i dva poziva na radnju
2. **Problem** koji čitatelj prepoznaje kod sebe
3. **Tko smo**, kratko i konkretno
4. **Usluge**, pregledno i s cijenama ili rasponima
5. **Dokaz ili izračun**, nešto opipljivo
6. **Proces**, što se događa nakon upita
7. **Obrazac**, s malo obaveznih polja

Hibrid je dobro rješenje: sve na naslovnici za konverziju, plus dubinske stranice
radi tražilica.

## Interakcije koje se isplate

Provjereno u tri iteracije stranice:

- **naslov koji dolazi u fokus** pri učitavanju, zamućenje prema oštrini
- **kinetička izmjena riječi** u naslovu, koja pokazuje tri strane posla
- **interaktivna mreža točaka** na canvasu koja reagira na pokazivač
- **beskonačna traka** s uslugama koja se polako pomiče
- **popis usluga u stilu kazala** s cijenom koja prati pokazivač
- **izračun s klizačima** koji pokaže učinak, s jasnom naznakom da je procjena

Pravila koja vrijede za sve:

- Poštovati `prefers-reduced-motion`, ugasiti animacije kada je tražena mirnija verzija.
- Efekti koji ovise o pokazivaču moraju imati smislenu verziju na dodirniku, jer
  na mobitelu nema kursora.
- **Nikada ne skrivati bitnu informaciju iza prelaska mišem.** Cijena mora biti
  vidljiva i bez toga, efekt je samo dodatak.

## Puni izbornik preko zaslona

Umjesto klasične vodoravne navigacije, gumb koji otvara izbornik preko cijelog
zaslona s velikim natpisima. Prednost je što je isti na računalu i na mobitelu,
pa nema zasebne mobilne verzije.

Stanje se drži na `aria-expanded`, a CSS reagira na taj atribut. Time je izbornik
i pristupačan i jednostavan.

## Prilagodba mobitelu

- Testirati na pravom telefonu, ne samo sužavanjem prozora.
- Široke tablice i dijagrami idu u vlastiti spremnik s vodoravnim klizanjem, tijelo
  stranice nikad ne smije klizati vodoravno.
- Za punu visinu zaslona koristiti `svh` uz `vh` kao pričuvu:
  `min-height: calc(100vh - 84px); min-height: calc(100svh - 84px);`

## Istinitost sadržaja

Kod nove tvrtke bez portfelja postoji napast da se sadržaj napuše. To se ne radi.

Provjerena rješenja:

- iskustvo iz drugih poslova navesti kao **dokaz sposobnosti**, anonimno, i jasno
  reći da nije klijentski projekt
- otvoreno napisati da prvi projekti idu po povoljnijim uvjetima jer se gradi portfelj
- brojke iz istraživanja označiti kao industrijske podatke, s izvorom
- izračune označiti kao procjenu, uz vidljivu pretpostavku

Ako se pretpostavka u izračunu promijeni, uskladiti i tekst ispod njega.

## Kontakt obrazac bez pozadinske usluge

Za početak je `mailto` prihvatljiv: obrazac sastavi poruku i otvori program za
poštu. Uz to jasno napisati adresu, za slučaj da se program ne otvori.

Ostaviti `TODO` iznad obrasca s uputom za prelazak na pravu uslugu. Adresa
e-pošte se ionako mora prije ozbiljne kampanje riješiti kako treba.

## Osnovna higijena stranice

- `robots.txt`, `sitemap.xml`, `canonical`, `og:` oznake na svakoj stranici
- `404.html` u duhu ostatka stranice
- favicon koji je dio identiteta, ne ostatak prethodne verzije
- naslov stranice s razdjelnikom `|`, bez em crtice
