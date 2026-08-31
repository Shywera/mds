# 14 Kontrolne liste

## Nova interna aplikacija

**Prije pisanja koda**

- [ ] Tko će je koristiti i s kojeg računala
- [ ] Treba li prijava, i ako ne treba, je li to svjesna odluka
- [ ] Odabran slobodan port, upisan u popis portova
- [ ] Odakle dolaze podaci i smije li se u izvor pisati

**Skelet**

- [ ] Raspored mapa prema [02](02-skelet-aplikacije.md)
- [ ] `app/core/templating.py` s jednom Jinja okolinom
- [ ] Poslovna logika u `service.py`, ne u rutama
- [ ] `.env.example` sa svim varijablama, `.env` u `.gitignore`
- [ ] `requirements.txt` s pripetim verzijama

**Pokretanje**

- [ ] `run.bat` u CRLF i ASCII, samoizlječiv, bez `--reload`
- [ ] `dev-wifi.bat` koji ispiše lokalnu adresu i adresu na mreži
- [ ] Provjereno da se prozor ne zatvara, pokretanjem iz Explorera
- [ ] Autostart `.vbs` ako aplikacija treba raditi stalno
- [ ] Dodana u upravljačku ploču i na portal

**Podaci**

- [ ] Automatska sigurnosna kopija na startu, zadržava zadnjih dvadeset
- [ ] Ruta za preuzimanje kopije, zaštićena ako postoji prijava
- [ ] Datumi u ISO obliku, količine kao brojevi
- [ ] Migracije idempotentne i nerazorne

**Prije predaje**

- [ ] `tests/conftest.py` postavlja `DATABASE_URL` prije uvoza aplikacije
- [ ] Svaki glavni tok prošao kroz `TestClient`
- [ ] Ono što se gleda provjereno u pregledniku
- [ ] PDF provjeren rasterizacijom, ne snimkom zaslona
- [ ] Testni podaci obrisani iz baze
- [ ] `README.md` s uputom za drugo računalo
- [ ] `CLAUDE.md` sa stanjem, zamkama i namjernim odstupanjima

---

## Novi modul u postojećoj aplikaciji

- [ ] Ima li modul unakrsne uvoze prema drugim modulima, i mogu li se izbjeći
- [ ] Rute s tekstualnim segmentom registrirane prije `/{id}`
- [ ] Nove dozvole dodane u popis i mapiranje putanja
- [ ] Poveznice u navigaciji skrivene prema dozvoli
- [ ] Migracija za nove stupce, idempotentna
- [ ] Dokumentacija modula i status u `CLAUDE.md` ažurirani u istom prolazu

---

## Preuzimanje naslijeđenog alata

- [ ] Pročitan izvorni kod, ne samo opis
- [ ] Popisani stupci koje čita, s indeksima, jer se izvori mijenjaju
- [ ] Provjereno računa li alat iz sirovih ulaza ili vjeruje spremljenim vrijednostima
- [ ] Rezultat nove verzije uspoređen s izlazom stare, brojka po brojku
- [ ] Poznate greške stare verzije popisane prije nego se prenesu
- [ ] Zapisano što je namjerno izostavljeno

---

## Prije objave u javni repozitorij

- [ ] Uklonjeni nazivi tvrtke, kupaca i dobavljača, uključujući iz povijesti
- [ ] Uklonjeni interni poslužitelji, imena računala i mrežne putanje
- [ ] Uklonjeni ključevi, tokeni i datoteke s lozinkama
- [ ] Uzorci podataka izmišljeni, ne stvarni
- [ ] Pročitan `NASTAVAK.md` i slični dokumenti, jer skupljaju poslovne bilješke
- [ ] Provjerena vidljivost repozitorija otvaranjem bez prijave
- [ ] Provjereno da `.gitignore` pokriva `.venv`, `data/`, `backup/`, `uploads/`, `.env`

---

## Nova javna web stranica

- [ ] Odlučeno gdje živi domena i koji repozitorij je nosi
- [ ] `CNAME`, `.nojekyll`, radni tok za objavu
- [ ] DNS zapisi u načinu bez posredovanja prometa
- [ ] `robots.txt`, `sitemap.xml`, `canonical` i `og:` oznake
- [ ] Vlastita `404.html`
- [ ] Favicon iz aktualnog identiteta
- [ ] Sve boje kroz varijable, bez upisanih vrijednosti
- [ ] Testirano na pravom telefonu
- [ ] `prefers-reduced-motion` poštovan
- [ ] Bitne informacije vidljive bez prelaska mišem
- [ ] Tvrdnje istinite, procjene označene kao procjene
- [ ] Bez em crtica u tekstu

---

## Prije puštanja u rad kod korisnika

- [ ] Mjerljiv kriterij dovršenosti dogovoren unaprijed
- [ ] Aplikacija testirana s računala korisnika, ne samo s vlastitog
- [ ] Objašnjeno što raditi kada nešto ne radi
- [ ] Početna lozinka promijenjena, testni korisnici obrisani
- [ ] Sigurnosna kopija provjerena, ne samo napisana
- [ ] Dogovoreno tko održava i pod kojim uvjetima
