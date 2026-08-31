# 05 Excel i podaci

Excel je u proizvodnim tvrtkama i dalje glavni format razmjene. Ovo poglavlje je
skup pravila kako ga čitati a ne nasjesti.

## Temeljno pravilo: ne vjerovati spremljenoj vrijednosti

`openpyxl` čita **samo spremljene vrijednosti** formula. Ako datoteka nije bila
otvorena u Excelu nakon što ju je sustav generirao, formula nema spremljenu
vrijednost i dobiva se `#VALUE!` ili `None`.

Zato:

> **Iznose računati u kodu iz sirovih ulaza. Ne oslanjati se na predračunatu
> vrijednost iz Excela.**

To je spasilo cijeli projekt u kojem je sedam od dvadeset pet datoteka imalo
pokvarenu kaskadu prodajne cijene. Troškovi materijala i rada bili su ispravni,
pa se sve dalo preračunati.

### Zamka koju Excel sam sakrije

U tim datotekama uzrok je bio dvostruki znak jednakosti (`==`) u formuli.
Zanimljivo je da se **u Excelu ne vidi**, jer ga automatska korekcija formule
tiho popravi pri otvaranju. Vidi se samo u spremljenoj datoteci, u sirovom XML-u:

```xml
<f>=H12*E16</f><v>#VALUE!</v>
```

Ako korisnik tvrdi da je datoteka ispravna jer je otvorio i vidio broj, to nije
protuargument.

### Pričuvni izvor

Kada glavni redak daje `#VALUE!`, dogovoriti pričuvni redak s istim značenjem i
uz njega prikazati upozorenje. Provjeriti podudarnost na svim ispravnim
datotekama prije nego se pričuva pusti u rad.

## Čitanje po oznakama, ne po fiksnim redcima

Izvještaji mijenjaju raspored ovisno o broju stavki. Fiksne koordinate ćelija se
raspadnu na prvoj datoteci s drugačijim brojem artikala.

Umjesto toga tražiti **sidrišne oznake** u tekstu (`"KALKULACIJA BR"`,
`"UTROŠAK MATERIJALA"`, `"STROJ:"`), pa čitati blok ispod svake.

Isti pristup vrijedi za Word dokumente: vrijednost se traži iza oznake
(`"Br. Narudžbe:"`, `"Order Number:"`), jer su oznake iste kroz sve kupce i oba
jezika. Time svaki postojeći dokument postaje predložak bez pripreme.

## Brzina

Velike datoteke čitati u jednom prolazu i pamtiti rezultat:

```python
wb = load_workbook(putanja, read_only=True, data_only=True)
```

Uz predmemoriju po vremenu izmjene datoteke. Bez toga je jedan klik u sučelju
trajao šest do devet sekundi.

Ako se predmemorija gradi na prvi zahtjev, zagrijati je na startu aplikacije,
inače prvi korisnik čeka učitavanje.

## Zamke po bibliotekama

### openpyxl

- Za ćelije s neobičnim ili nultim datumima zna vratiti goli `datetime.time`
  umjesto `datetime.datetime`. Provjeriti tip prije `.date()`.
- Puca na `stylesheet Fill` u izvozima nekih ERP sustava. Tada koristiti
  `pandas.read_excel(..., engine="calamine")`.

### pandas

- `str.contains` prema zadanim postavkama koristi **regularni izraz**. Točka u
  upitu tada postaje divlji znak i daje pogrešne pogotke. Za doslovnu pretragu
  postaviti `regex=False`.
- Kod spajanja izvora paziti na smjer: ići **od manjeg skupa prema tablici**, ne
  obrnuto, inače se povuče cijela tablica.

## Regularni izrazi na šiframa

Šifra od osam znamenki unutar naziva mora imati granice:

```python
re.search(r"(?<!\d)\d{8}(?!\d)", naziv)
```

Bez granica izraz uhvati komad trinaesteznamenkastog broja kalkulacije i tiho
poveže krivi redak.

## Spajanje po dva ključa

Kada nijedan ključ nije potpun, spajati po oba i uniju rezultata:

- po broju dokumenta, jer stariji zapisi nemaju šifru u nazivu
- po šifri artikla, jer kod kompleta samo jedan od dva retka ima upisan broj

U stvarnom slučaju je tek unija oba ključa pronašla sedam redaka koji su prije
ispadali.

## Grupiranje: po šifri, ne po nazivu

Grupiranje po početku naziva do razdjelnika daje lažne pogotke, jer dvije
različite stavke dijele početak naziva. Grupirati po **šifri** za materijale i po
**stroju i operaciji** za rad. Dva stroja sličnog naziva mogu imati različitu
satnicu.

## Duplikati i sukobi u izvorima

Ista šifra dokumenta zna nositi **različit sadržaj** u dvije datoteke. U stvarnom
skupu to je bilo deset od dvadeset sedam slučajeva.

Provjeren pristup:

1. Računati s prvom pronađenom datotekom.
2. Poseban ekran koji prikazuje razlike, uključujući dodane, uklonjene i
   promijenjene stavke.
3. Kada je sadržaj stvarno drugi dokument, dopustiti ručni ispravak broja **u
   aplikaciji**, u zasebnoj tablici, bez diranja izvornog sustava. Prazno polje
   vraća izvorni broj.

## Provjera vlastitog izračuna

Uz svaki izračun koji zbraja i oduzima dodati samoprovjeru koja usporedi završnu
bilancu s brojkom iz izvora i javi odstupanja. U jednom projektu je ta provjera
potvrdila da se svih pedeset dva artikla slažu, što je dalo povjerenje da se
stari alat smije zamijeniti.

## Projekcija zaliha: česta pogreška u modelu

Alat koji je gledao **samo potrošnju** lažno je uzbunjivao. Artikl bi u
simulaciji pao ispod nule, iako narudžba stiže prije toga i vraća zalihu iznad
minimuma.

Ispravan model spaja **obje** vremenske crte, potrošnju i dolazak, u jednu
krivulju. Značka na nadzornoj ploči mora koristiti punu verziju, inače se lažna
uzbuna vraća na druga vrata.

## Hrvatski format brojeva

Decimalni zarez i točka za tisućice, i u prikazu i pri kopiranju, jer se tako
lijepi ravno u hrvatski Excel.

Filtri se registriraju u zajedničkoj Jinja okolini. Dvije zamke:

- Prioritet operatora: `a + b|hr(2)` primijeni filtar samo na `b`. Uvijek
  `(a + b)|hr(2)`.
- Iznimke gdje mora ostati točka: CSS vrijednosti i `value` brojčanih polja.
