# 18 Mini igre i zvuk u pregledniku

Ritamska igra, trener mehanika i nekoliko vizualizacija glazbe, sve u običnom
HTML-u, CSS-u i JavaScriptu, bez ijednog frameworka. Ovo poglavlje je ono što se
iz toga prenosi na sljedeći projekt.

Vrijedi i za poslovne aplikacije: sat, kalibracija i tiho podnošenje nedostupne
usluge isti su problemi kao u svakom alatu koji nešto mjeri u stvarnom vremenu.

## Sat igre nije `performance.now()`

Ako se nešto sinkronizira sa zvukom, **zvuk je sat**, a ne sličice.

```js
// Ovako. Nota pada kad je zvuk tu.
var t = audio.currentTime;

// Ne ovako. Na dugoj pjesmi se razilazi.
var t = (performance.now() - start) / 1000;
```

Sličice se preskaču, kartica u pozadini staje, a zvuk ide dalje. Nakon tri minute
razlika je čujna i igra izgleda pokvarena iako je logika ispravna.
`requestAnimationFrame` ostaje za **crtanje**, a ne za mjerenje vremena.

## Dva različita puta za zvuk

| Vrsta zvuka | Čime | Zašto |
| --- | --- | --- |
| Duga pjesma | `<audio>` element | Streama se, ne čeka se cijeli download, skakanje po pjesmi je jedan `currentTime =` |
| Kratki udarac, klik, potvrda | WebAudio: `decodeAudioData` jednom, pa `createBufferSource` po svakom udarcu | `<audio>` element za kratke zvukove ima čujno zakašnjenje i ne da se pouzdano preklapati sam sa sobom |

Dekodirati jednom pri učitavanju, pa samo stvarati izvore. Stvaranje novog
`Audio()` objekta po udarcu je najčešći uzrok zvuka koji "kasni" i "pucketa".

## Kalibracija odmaka

Svaki lanac zvuka ima svoje zakašnjenje: bluetooth slušalice lako dodaju 150 ms i
više. Bez kalibracije igra je netočna za pola korisnika, i to na način koji oni ne
mogu opisati, samo im je loše.

Rješenje je jedan ekran na kojem korisnik tapka u ritam, pa se razlika **spremi po
korisniku** (`localStorage`) i doda na vrijeme note. Vrijednost je njegova, ne
globalna postavka.

## Autoplay se ne zaobilazi

Preglednici ne puštaju zvuk prije prve korisnikove interakcije, i to je ispravno.

Ne tražiti zaobilaznicu. Stranica se **napravi tako da prvi klik ima smisla u
priči**: "uđi u svetište", "pali", "pojačaj". Jedna interakcija koja je ionako
trebala postojati rješava i tehničko ograničenje i uvod.

Isto vrijedi za `AudioContext`: stvoriti ga, ali `resume()` tek na klik.

## Treperenje, i izlaz iz njega

Vizualizacija koja radi na bas bubnju treperi. To nekima nije samo neugodno nego
opasno.

- **`prefers-reduced-motion`** gasi prostorno gibanje, kao i svugdje drugdje.
- Uz to **vlastita opcija** (nazvana *calm*), zapamćena u `localStorage`, jer dio
  korisnika ne mijenja postavke sustava, ali će kliknuti prekidač na stranici.
- Opcija ne smije samo stišati efekt nego ga ukinuti: bez naglih promjena
  svjetline preko velikih površina.

## Podaci igre: sekunde, ne taktovi

Note se čuvaju u **sekundama od početka pjesme**. Djelovalo je elegantnije čuvati
ih u taktovima i množiti s dužinom takta, ali karte koje mijenjaju tempo usred
pjesme razbiju tu pretpostavku, a nije ih malo.

Pozicija u taktu se i dalje može izračunati, iz mjerne točke koja u tom trenutku
vrijedi, i korisna je za razdvajanje nota na taktu od onih između, npr. pri
automatskoj podjeli na težine.

**Zamka:** ako je format već krenuo u taktovima, migracija je jednokratna skripta i
treba je zadržati u repozitoriju. Inače nitko poslije ne zna kako su stari podaci
pretvoreni.

## Generirana stranica

Kad se podaci ulijevaju u stranicu skriptom, ta stranica je **artefakt**, ne izvor.

```
tools/dungeons.json   <- konfiguracija, ovo se uređuje
tools/charts/*.txt    <- podaci, ovo se uređuje
tools/build_beat.py   <- gradnja
public/beat/index.html <- rezultat, ovo se NE uređuje ručno
```

Napisati na vrh generirane datoteke da je generirana i čime. Bez toga se izmjena
napravi ručno, pa se izgubi pri sljedećoj gradnji, i to obično nekoliko dana
kasnije kad se već zaboravilo.

**Zamka:** alati za gradnju lako dobiju apsolutni put (`ROOT = "C:/Users/..."`) jer
tako rade na prvom računalu. Izvesti put iz `__file__`, inače repozitorij ne radi
nigdje drugdje.

## Rezultati: usluga koja smije ne postojati

Lista najboljih rezultata treba pohranu na serveru. Cloudflare Pages Functions plus
jedan KV store rješavaju to bez vlastitog servera:

```
GET  /api/scores?g=<razina>   -> liste po težini
POST /api/scores              -> { g, d, n, s, a, c }
```

Tri pravila koja su se isplatila:

1. **Bez vezanja pohrane funkcija vraća `503`, a stranica to podnese** i pokaže
   lokalne najbolje rezultate. Igra radi prvog dana, prije nego je infrastruktura
   spremna.
2. **Ograničiti ulaz**: najveći dopušteni score, popis dopuštenih razina, i broj
   zapisa koji se drži (npr. 25). Javni POST bez ograničenja je javni POST.
3. **Isti store, različiti ključevi** za dvije različite stvari (lista i knjiga
   gostiju), pa nema potrebe za drugim vezanjem.

Lokalni najbolji rezultat u `localStorage` nije zamjena za server, nego prvi sloj:
igrač vidi svoj napredak i bez mreže.

## Unos

- Slušati i `keydown` i `pointerdown`. Ista igra na mobitelu treba dodirne zone, i
  to nije dodatak nego polovica korisnika.
- Tipke dati korisniku da ih promijeni, i zapamtiti odabir. Raspored tipki nije
  isti na svakoj tipkovnici.
- `preventDefault()` na tipke koje inače skrolaju stranicu (`Space`), inače igra
  radi, a stranica pod njom skače.

## Težina resursa

Nekoliko pjesama je desetke megabajta. Dvije posljedice:

- **Audio ne ide u git bez razmišljanja.** Repozitorij s dvadesetak pjesama naraste
  na stotinu megabajta i to se ne da poslije očistiti bez prepisivanja povijesti.
  Ili LFS, ili pohrana izvan repozitorija, ili svjesna odluka da je tako u redu.
- Ne učitavati sve unaprijed. Pjesma se učita kad se odabere, ne pri otvaranju
  stranice.

## Zamke, skupljeno

| Zamka | Kako se pokazuje |
| --- | --- |
| Sat na `performance.now()` | Sinkronizacija se raspada nakon minute ili dvije, jače ako je kartica bila u pozadini |
| Novi `Audio()` po udarcu | Zvuk kasni i pucketa pod bržim ritmom |
| Bez kalibracije odmaka | Dio korisnika je uvjeren da igra ne registrira pritiske |
| Zvuk pokušava krenuti sam | Preglednik ga blokira, a igra tiho čeka zvuk koji nikad ne dođe |
| Samo `prefers-reduced-motion`, bez prekidača na stranici | Većina korisnika nikad nije dirala tu postavku sustava |
| Ručna izmjena generirane datoteke | Izgubi se pri sljedećoj gradnji |
| Apsolutni put u alatu | Repozitorij radi samo na računalu na kojem je nastao |
| Javni POST bez ograničenja | Lista se napuni besmislicama ili nemogućim rezultatima |
