# 09 Integracija umjetne inteligencije

## Osnovno pravilo

> **Umjetna inteligencija služi za objašnjenja, prijedloge i tekst. Nikada za
> aritmetiku.**

Svi iznosi se računaju u kodu, iz sirovih ulaza. Model dobiva već izračunate
brojke i objašnjava ih. Time nema tihih grešaka u novcu.

## Strukturirani izlaz

Tražiti odgovor u zadanoj strukturi, ne slobodan tekst koji se onda raščlanjuje:

```python
class ObjasnjenjeRazlike(BaseModel):
    sazetak: str
    razlozi: list[str]
    razina: Literal["info", "paznja", "kriticno"]
```

Sistemsku uputu držati stabilnom da se može predmemorirati.

## Demo način rada je obavezan

Aplikacija mora raditi i kada ključa nema, kada nema sredstava na računu ili kada
je usluga nedostupna.

```python
if settings.ai_demo:
    return _demo_objasnjenje(ctx)
try:
    return _stvarni_poziv(ctx)
except Exception:
    return _demo_objasnjenje(ctx)      # tihi povratak na pravila
```

Demo odgovor gradi se po jasnim pravilima i **vidljivo se označi** oznakom
`[DEMO]`. Korisnik u svakom trenutku zna gleda li odgovor modela ili pravila.

Ovo nije teorijska mjera. U stvarnom projektu je ključ bio ispravan, ali
organizacija nije imala sredstava, pa čak ni brojanje tokena nije prolazilo.
Aplikacija je zbog demo načina radila dalje.

## Učenje iz ispravaka, bez ponovnog treniranja

Provjeren obrazac za suradnju modela i čovjeka koji odlučuje:

1. Model daje prijedlog uz obrazloženje.
2. Čovjek prijedlog **prihvaća, odbija ili ispravlja**.
3. Svaka odluka se sprema u tablicu povratnih informacija.
4. Sljedeći prijedlog dobiva prošle odluke kao primjere u uputi.

Važno je korisniku pošteno objasniti da se model ne dotrenira, nego da uči iz
primjera u uputi. To je razumljivo i ne obećava previše.

### Kontekst je nužan, inače model uči krivu stvar

Prva verzija je pamtila samo brojku, pa je predlagala istu maržu uvijek. Korisnik
je s pravom prigovorio da ista brojka ne vrijedi za drugu količinu i drugi papir.

Ispravak je bio spremati **kontekst uz svaku odluku**: veličinu serije, trošak po
tisući, promjenu troška, datum. Model tada uči **obrazac**, ne tablicu.

U uputi izričito tražiti učenje odnosa: kako se cijena mijenja s volumenom, kako
reagira na promjenu troška, da su novije odluke važnije od starijih i da isti
proizvod nosi više težine od istog kupca.

Pričuvna pravila u demo načinu mogu isto: pronaći najbliži kontekst po logaritamskoj
udaljenosti veličine serije, pa prilagoditi prijedlog po pravilu.

Provjera koja pokazuje da radi:

- odluka 44 % pri seriji 2500
- ista etiketa pri seriji 800 daje prijedlog 48 % uz obrazloženje o manjoj seriji
- pri seriji 10000 daje 40 %

## Model kao kontrolor podataka

Vrijedna primjena koja se isplatila: model pregledava dokument i javlja
sumnjivosti, a čovjek potvrđuje ili odbacuje.

Provjere koje su nalazile stvarne greške:

- cijena stavke naspram medijana iste šifre u ostalim dokumentima
- nula u cijeni, iznosu ili vremenu
- velika promjena jedinične cijene u odnosu na prethodni dokument
- nedostaje veličina serije

Svaka napomena ima status (nova, potvrđena, odbačena) i onoga tko je odlučio.
Ponovni pregled briše samo napomene koje nitko nije riješio.

Rezultat u stvarnom skupu: od trideset dokumenata dvadeset tri su imala nešto za
provjeriti, a među njima i stavka s cijenom 0,01 € umjesto oko 6,50 €.

## Obavezan pregled prije slanja

Kada model priprema dokument koji ide kupcu, uvesti stanje **nacrt izrađen
modelom**. U tom stanju se izvoz u PDF ne nudi.

Na stranici pregleda po svakoj stavci ide odluka prihvati ili odbij, a ispod nje
polje za napomenu. Napomene su najvrjedniji ulaz za sljedeće prijedloge, jer
sadrže razlog, a ne samo ispravak.

Tek kada su sve odluke donesene, dokument prelazi u stanje spremno za slanje.

## Praktične sitnice

- Ključ ide u `.env`, koji je u `.gitignore`. Ako je ključ ikad prošao kroz
  razgovor ili dijeljeno računalo, zamijeniti ga.
- Cijeli krug mora raditi i u demo načinu, jer se tako testira bez troška.
- Ishod dokumenta (prihvaćen, odbijen) vratiti u povijest kao ulaz za učenje.
