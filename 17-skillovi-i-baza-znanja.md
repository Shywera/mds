# 17 Skillovi i baza znanja

Ovaj priručnik postoji da se isti problem ne rješava dvaput. Skill je isti alat,
samo namijenjen pomoćniku umjesto čovjeku: skup uputa koji se učita **samo kad
zatreba**, pa ne troši prostor dok ne treba.

## Anatomija skilla

```
ime-skilla/
  SKILL.md          <- ulazna točka, mala i odlučna
  references/
    detalji.md      <- učitava se samo kad SKILL.md kaže
    primjeri.md
```

`SKILL.md` počinje frontmatterom:

```markdown
---
name: ship-site
description: "Objava i provjera živih stranica. Koristiti kad se traži push,
deploy, objava ili vraćanje na staro, ili pri izmjeni datoteka u web repozitoriju."
---
```

| Polje | Pravilo |
| --- | --- |
| `name` | Mora biti **jednako imenu mape**. Mala slova, crtice. Alat javlja neusklađenost |
| `description` | Ovo je jedino što pomoćnik vidi prije učitavanja, pa odlučuje **hoće li se skill uopće pozvati**. Piše se kao popis okidača, ne kao sažetak |

**Zamka:** opis napisan kao sažetak (`"Pravila za objavu stranica."`) zvuči uredno,
a skill se nikad ne učita, jer ništa u zahtjevu korisnika ne odgovara tom tekstu.
Opis mora sadržavati riječi koje će čovjek stvarno napisati: *push, deploy, objavi,
vrati na staro, pokvarilo se*.

## Što ide u SKILL.md, a što u references

`SKILL.md` je kratak i govori **što odlučiti i u kojem redu**. Dugi popisi,
tablice vrijednosti i primjeri idu u `references/`, uz izričitu uputu kada se
učitavaju.

Vanjski skill `hallmark` je dobar primjer razmjera: `SKILL.md` ima 558 redova i
uglavnom usmjerava, a uz njega je 106 referentnih datoteka od kojih se po gradnji
učita pet do sedam. Da je sve u jednoj datoteci, svaki bi poziv plaćao cijeli
katalog.

## Gdje žive

| Mjesta | Tko ih čita |
| --- | --- |
| `~/.claude/skills/<ime>/SKILL.md` | Claude Code, osobni skillovi |
| `~/.agents/skills/<ime>/` | dijeljeno mjesto za više alata, često simbolički povezano u gornje |

Instalacija tuđeg skilla: `npx skills add <korisnik>/<repozitorij>`. Instalater
ispiše izvještaj o riziku i napravi simboličku vezu iz `~/.claude/skills`.

**Prije korištenja tuđeg skilla provjeriti sadrži li izvršne datoteke:**

```bash
find ~/.agents/skills/<ime> -type f ! -name "*.md" | wc -l
```

Nula znači da je sve tekst, pa je rizik samo u sadržaju uputa. Sve iznad nule
traži pogled u te datoteke prije prvog poziva, jer skill radi s punim dozvolama
kao i pomoćnik koji ga čita.

## Alat za pregled i izmjenu

Uređivanje skillova i bilježaka kroz uređivač koda radi, ali je nespretno kad ih
je stotinu. Za to postoji mali lokalni alat, isti obrazac kao interne aplikacije
iz [03](03-windows-i-pokretanje.md): Python iz standardne biblioteke, jedan
`server.py`, jedna `app.html`, `start.cmd` za dvoklik, `http://127.0.0.1:7777`.

Što radi: popis svih mapa iz `config.json`, prikaz renderiranog markdowna,
uređivanje u istom prozoru, izrada nove `.md` datoteke, izrada novog skilla s
ispravnim frontmatterom i praznom `references/` mapom, i provjera koja pokraj
imena skilla ispiše upozorenje ako nema frontmattera, ako nema `name` ili
`description`, ili ako se `name` ne podudara s imenom mape.

Odluke koje se isplatilo napraviti odmah:

| Odluka | Zašto |
| --- | --- |
| Sluša samo na `127.0.0.1` | Alat piše po disku. Ne smije biti dostupan s mreže |
| Svaki put se provjerava protiv popisa dopuštenih mapa | Inače `?path=../../../Windows/win.ini` čita što god želi |
| Atomarno pisanje (`.tmp~` pa `os.replace`) | Prekid ne ostavlja polovičnu datoteku |
| Spremanje odbija ako je datoteka promijenjena izvan alata | Inače tiho pregazi izmjenu napravljenu u uređivaču |
| Brisanje seli u `.trash/` s vremenskom oznakom | Brisanje bez povratka je za alate koji imaju povijest verzija |

**Zamka:** vrijeme izmjene u cijelim sekundama čini provjeru sudara slijepom
unutar iste sekunde. Dva spremanja u istoj sekundi prođu kao da nije bilo
promjene. Uzeti milisekunde (`int(st.st_mtime * 1000)`).

## Baza znanja u datotekama

Trajna memorija pomoćnika drži se po istom pravilu kao i ovaj priručnik: **jedna
činjenica, jedna datoteka**, plus indeks koji se čita na početku svakog razgovora.

```markdown
---
name: kratka-oznaka
description: <jedan red, po njemu se odlučuje je li datoteka relevantna>
metadata:
  type: user | feedback | project | reference
---

Sadržaj. Povezano s [[ime-druge-datoteke]].
```

Vrste: `user` (kdo je korisnik), `feedback` (kako želi da se radi, uz obrazloženje),
`project` (tekući rad i ograničenja koja se ne vide iz koda), `reference` (vanjski
izvori).

Dva pravila koja se lako prekrše:

1. **Ne zapisivati ono što repozitorij već čuva.** Struktura koda, povijest
   izmjena i prošli popravci su u gitu. U memoriju ide ono što se iz koda ne vidi:
   zašto je nešto odlučeno, što je odbijeno, čega se ne smije dirati.
2. **Relativne datume pretvoriti u apsolutne.** "Prošli tjedan" je za pola godine
   bezvrijedno.

Veze u dvostrukim uglatim zagradama (`[[ime]]`) povezuju datoteke. Veza na datoteku
koja još ne postoji nije greška, nego oznaka što treba napisati. Alat iz prethodnog
odjeljka ih prikazuje klikabilnima, i drugom bojom kad cilj ne postoji, pa se odmah
vidi što je ostalo nedovršeno.

## Kada skill, a kada poglavlje priručnika

| Ide u priručnik | Ide u skill |
| --- | --- |
| Znanje koje čovjek čita prije posla | Postupak koji pomoćnik izvodi tijekom posla |
| Objašnjenje zašto je nešto tako | Popis koraka i naredbi |
| Zamke i uzroci | Provjere koje se moraju proći prije predaje |

Isto znanje često ide na oba mjesta, ali u drugom obliku: poglavlje objašnjava,
skill provodi. Ako je sadržaj identičan, jedno od dvoje je nepotrebno.
