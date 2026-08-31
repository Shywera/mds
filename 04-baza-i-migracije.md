# 04 Baza i migracije

## SQLite je legitiman izbor, ne kompromis

Za interne aplikacije s nekoliko istovremenih korisnika SQLite je dovoljan i
uklanja cijeli sloj administracije. Uvjet je da `DATABASE_URL` dolazi iz okoline,
pa se prelazak na PostgreSQL svodi na promjenu varijable bez diranja koda.

Za velike sustave koristiti Alembic. Za male samostalne aplikacije `create_all`
na startu je dovoljan i brži za rad.

## Dva pristupa migracijama

### Alembic, za sustave koji rastu

Standardno, uz jedno upozorenje niže o stranim ključevima.

### Idempotentna migracija u `main.py`, za male aplikacije

Kada nema Alembica, a treba dodati stupac u bazu koja već ima podatke:

```python
from sqlalchemy import inspect as sa_inspect

def _migracija(engine):
    insp = sa_inspect(engine)
    stupci = {c["name"] for c in insp.get_columns("reklamacija")}
    if "tezina" not in stupci:
        with engine.begin() as veza:
            veza.execute(text("ALTER TABLE reklamacija ADD COLUMN tezina VARCHAR(20)"))
```

Poziva se na startu aplikacije. Mora biti idempotentno i nerazorno, jer se
izvršava pri svakom pokretanju.

Istim pristupom se i **uklanja** ograničenje koje više ne vrijedi:

```python
veza.execute(text("DROP INDEX IF EXISTS uq_paleta_aktivna_pozicija"))
```

## Zamka: SQLite ne može dodati strani ključ preko ALTER

`op.create_foreign_key` u Alembicu puca na SQLiteu. Rješenje je `batch` način:

```python
with op.batch_alter_table("materijal") as batch:
    batch.create_foreign_key("fk_materijal_pantone", "pantone", ["pantone_id"], ["id"])
```

Isto vrijedi za `downgrade`.

**Ako je migracija već pukla na pola:** baza tada ima dodane stupce, ali
`alembic_version` nije pomaknut i stranog ključa nema. Popravlja se ručnim
izvršavanjem `batch` operacije preko `MigrationContext`, pa `alembic stamp <rev>`.

## Najveća opasnost: testovi koji diraju stvarnu bazu

Jednom je stvarna baza obrisana testom. Spašena je iz automatske sigurnosne kopije.

`tests/conftest.py` **mora** postaviti `DATABASE_URL` na privremenu bazu **prije**
nego se aplikacija uveze:

```python
import os, tempfile
os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mkdtemp()}/test.db"

from app.main import app          # tek sada
```

Redoslijed nije stilsko pitanje. Uvoz aplikacije stvara engine prema tada
važećoj varijabli okoline.

Ako projekt koristi Alembic umjesto `create_all`, u `conftest.py` pozvati
`Base.metadata.create_all` ručno.

## Automatska sigurnosna kopija

```python
def auto_backup():
    izvor = db_putanja()
    if not izvor.exists():
        return
    odrediste = BACKUP_DIR / f"{izvor.stem}_{datetime.now():%Y%m%d_%H%M%S}.db"
    shutil.copy2(izvor, odrediste)
    stare = sorted(BACKUP_DIR.glob(f"{izvor.stem}_*.db"))[:-20]
    for s in stare:
        s.unlink()
```

Poziva se na startu u `main.py`. Čuva zadnjih dvadeset kopija.

Uz to ide ruta `GET /backup` za preuzimanje. **Ta ruta mora biti zaštićena
dozvolom** ako aplikacija ima prijavu, jer inače svatko na mreži skida cijelu
bazu. Dodati i `backup.bat` za ručno pokretanje.

## Djelomično jedinstveni indeksi

Za "jedna paleta može biti aktivna samo na jednoj poziciji" koristi se djelomični
jedinstveni indeks:

```python
Index("uq_paleta_aktivna_pozicija", "pozicija",
      unique=True, sqlite_where=text("datum_out IS NULL"))
```

Time se ujedno rješava utrka pri istovremenom upisu i dopušta ponovno korištenje
pozicije nakon izdavanja.

Kada se poslovno pravilo promijeni (dopušteno je više nepotpunih paleta na istoj
poziciji), indeks postaje običan, nejedinstveni, a stara baza se popravi
naredbom `DROP INDEX IF EXISTS` na startu.

## Obavezna pravila za podatke

Iz bolnog iskustva s naslijeđenim sustavom:

- **Datumi u bazi u ISO 8601 obliku.** Naslijeđeni sustav je čuvao `dd.mm.yyyy`
  kao tekst, pa je FIFO sortiranje po podnizu davalo pogrešnu paletu. Oblikovati
  isključivo pri prikazu.
- **Količine kao brojevi, ne tekst.** Inače nema djelomičnog izdavanja ni zbrojeva.
- **Validacija pozicije pri svakom upisu.** Naslijeđeni sustav je imao validator,
  ali ga nije zvao, pa su nastale palete na nepostojećim mjestima.
- **Transakcije, strani ključevi i indeksi** na sve što se često pretražuje.

## Snimke stanja umjesto prepisivanja

Kada aplikacija prima periodične izvoze iz drugog sustava, ne raditi `upsert`
preko postojećih podataka. Svaki izvoz je **snimka** s vlastitim identifikatorom
i zastavicom aktivnosti.

Prednosti koje su se pokazale u radu:

- povijest je odmah vidljiva na grafu, bez posebnog razvoja
- ponovno učitavanje istog izvoza zamjenjuje stari, bez dvostrukih točaka
- moguć je pregled starog stanja preko parametra u adresi

Važno razumjeti zašto povijest ne udvostručuje potrošnju: točke su **apsolutno
stanje**, dakle neovisna mjerenja, a ne zbroj događaja. Projekcija unaprijed
koristi samo aktivnu snimku.
