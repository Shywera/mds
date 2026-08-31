# 07 Sučelje: HTMX i Alpine

## Redoslijed ruta

Ruta s tekstualnim segmentom mora biti registrirana **prije** rute s cjelobrojnim
parametrom, inače je pretvorba u broj uhvati i sruši:

```python
@router.get("/analitika")        # prvo
@router.get("/dobavljaci")       # prvo
@router.get("/{id}")             # tek onda
```

Alternativa koja uklanja cijeli problem je zaseban prefiks za detalj, primjerice
`/artikl/{sifra}`.

## Okidači koji ne rade ono što se očekuje

`hx-trigger="change"` na tekstualnom polju okida se tek pri gubitku fokusa. Dok
korisnik tipka i gleda rezultat, on ostaje na nuli. Ispravno za živi izračun:

```html
hx-trigger="keyup changed delay:400ms, change delay:150ms"
```

Prvi dio pokriva tipkanje uz odgodu, drugi promjenu padajućeg izbornika.

Forma s dva polja i bez gumba za slanje **ne šalje se pritiskom na Enter**. Kod
skenera koji se ponaša kao tipkovnica to znači da drugi sken ništa ne napravi.
Rješenje je premjestiti HTMX atribute s forme na samo polje, uz
`hx-trigger="keyup[key=='Enter']"` i `hx-include` za ostala polja.

## Sučelje za ručni skener

Skener tipa keyboard wedge upiše tekst i pritisne Enter. Iz toga slijedi:

- automatski fokus na polje za sken
- slanje na Enter, pa vraćanje fokusa na sljedeće polje
- `hx-disabled-elt` dok zahtjev traje, da dvostruki sken ne prođe dvaput
- velika polja i krupan tekst, jedan stupac

Kamera i JavaScript čitači nisu potrebni i samo smetaju.

## Alpine: tri provjerene zamke

**Zatvaranje padajućeg izbornika.** Ako je gumb izvan panela, a `@click.outside`
stoji na panelu, klik na gumb se broji kao "izvan" pa se izbornik odmah zatvori i
ponovno otvori. Direktivu staviti na zajedničkog roditelja.

**`overflow-x-auto` na tablici reže izbornik** koji izlazi iz nje. Ukloniti ga ili
izbornik prikazati izvan tablice.

**Podaci u atributu.** Veće JSON strukture ne stavljati izravno u `x-data` zbog
navodnika, nego u zaseban `<script type="application/json">`. U atributima
izbjegavati funkcije sa strelicom zbog znaka `>`.

## Polja izvan forme koja se svejedno šalju

Atribut `form="id-forme"` na polju koje je fizički izvan forme uključuje ga u
slanje. Korisno za trake s odabirom iznad tablice.

## Inline uređivanje kao u Excelu

Kada korisnik traži tablicu u kojoj se piše izravno u ćeliju:

- ćelije su `<input>`, računata polja su samo za čitanje i sivа
- tekstualna polja: `hx-swap="none"`, sprema se tiho i fokus ostaje za sljedeću ćeliju
- brojčana polja: preračun i zamjena cijele tablice, jer se lanac vrijednosti mijenja
- na poslužitelju bijela lista polja koja se smiju mijenjati

Za promjenu redoslijeda redaka SortableJS s ručkom. Skriptu za inicijalizaciju
staviti **u parcijalni predložak**, da se ponovno izvrši nakon zamjene sadržaja.
Ne koristiti `forceFallback`, jer kvari klon retka u tablici.

## Parcijalni predlošci i varijable

Uključeni parcijalni predložak vidi samo ono što mu roditelj proslijedi. Ako
`_troskovi.html` očekuje `troskovi`, a `detail.html` prosljeđuje samo objekt `r`,
sadržaj nestane nakon osvježavanja.

Sigurnije je u parcijalu čitati preko objekta (`r.troskovi`) nego preko zasebne
varijable.

## Statusi i boje

Vraćati **semantički tip** iz poslužitelja (`dobro`, `pazi`, `kritično`), a boje
rješavati u CSS-u. Tako se paleta mijenja na jednom mjestu.

Za dva različita prikaza istog podatka smiju vrijediti različita pravila, ali to
treba zapisati. Primjer iz skladišta: na tlocrtu je jedna ćelija cijela pozicija
sa svim visinama, pa se nepotpuno stanje prikazuje dijagonalnom polovicom boje. U
detaljnom prikazu je jedna ćelija jedan pretinac, pa je boja puna.

## Nadzorna ploča i izračuni

Ako nadzorna ploča prikazuje značku statusa, ona mora koristiti **isti puni
izračun** kao detaljni prikaz. Pojednostavljena verzija na naslovnici vraća
upravo onu grešku zbog koje je puni izračun i napisan.
