# 11 Git i objava

## Prije objave privatnog rada u javni repozitorij

Ovo je najvažnije poglavlje po posljedicama. Objavljeno se ne da povući, jer
ostaje u kopijama i pretraživačima i nakon brisanja.

### Popis za provjeru

Prije prvog `push` u javni repozitorij ukloniti:

- naziv tvrtke i njezine adrese, OIB, matični broj
- **imena kupaca i dobavljača**, uključujući ona u nazivima datoteka i u povijesti
- interne poslužitelje, imena računala i mrežne putanje
- pristupne podatke, ključeve, tokene, `config.ini` s lozinkama
- stvarne podatke o proizvodima i cijenama
- poslovne pretpostavke koje bi štetile u pregovorima, primjerice da su cijene
  privremene ili da klijenata još nema

Provjereni pristupi:

- naziv tvrtke u varijable okoline (`FIRMA_*`)
- interni ERP preimenovati u generički naziv, uz zadržavanje starog imena kao aliasa
  da kod i dalje radi
- **izmišljeni** uzorci podataka s prepoznatljivim prefiksom
- osjetljivo ukloniti i **iz povijesti**, ne samo iz zadnje verzije

### Povijest

Ako je osjetljivo ikad bilo u repozitoriju, dovoljno je da netko dohvati stariju
verziju. Za javnu objavu privatnog rada najsigurnije je krenuti od čistog
repozitorija bez povijesti.

### Provjeriti prije nego se nešto pusti van

```bash
git ls-remote https://github.com/<vlasnik>/<repo>.git
```

Uspješan odgovor bez traženja lozinke znači da je repozitorij dostupan, ali ako
su podaci za prijavu spremljeni na računalu, to nije dokaz da je javan.
Vidljivost provjeriti otvaranjem stranice repozitorija bez prijave.

## Objava statične stranice

GitHub Pages uz Actions radni tok. Bitni dijelovi:

```yaml
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
```

Uz to `CNAME` s domenom, `.nojekyll` da se ne pokreće Jekyll, i u postavkama
repozitorija uključena vlastita domena uz obavezan HTTPS.

DNS za vršnu domenu: četiri A zapisa prema GitHub Pages adresama, `www` kao CNAME
prema `<korisnik>.github.io`. Kod Cloudflarea zapisi moraju biti u načinu **DNS
only**, bez posredovanja prometa.

## Više verzija dizajna

Provjeren raspored kada se stranica redizajnira, a stara verzija se želi sačuvati:

- glavni repozitorij nosi **živu verziju**, jer je na njega vezana domena
- zaseban repozitorij služi kao **arhiva** prethodne verzije
- u dokumentu za nastavak zapisati koja je verzija gdje

Time se izbjegava premještanje domene, koje traži ručnu izmjenu DNS-a i postavki.

## Poruke uz izmjene

Kratak naslov u imperativu, pa odlomak koji objašnjava **zašto**, ne samo što.
Kod većih zahvata navesti i što je namjerno izostavljeno.

## Dokument za nastavak

U svakom projektu koji se nastavlja na drugom računalu ili nakon duže pauze
držati `NASTAVAK.md` s:

- što je projekt i za koga
- ključne odluke i razlozi
- gdje živi kod i kako se pokreće
- što je namjerno izostavljeno
- popis preostalih zadataka

**Oprez:** taj dokument prirodno skuplja osjetljive poslovne bilješke. Ako
repozitorij postane javan, prvo pročitati taj dokument.

## Rad na tuđem računalu

Kada se radi na poslovnom računalu, a rezultat pripada privatnom projektu:

- raditi u privremenoj mapi, ne na radnoj površini
- nakon objave lokalnu kopiju obrisati
- ne mijenjati globalne postavke gita ni spremati nove pristupne podatke

Sitnica koja zna zasmetati: mapa se ne da obrisati dok je ljuska u njoj. Prvo
izaći iz mape, pa brisati.
