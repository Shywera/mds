# 02 Skelet aplikacije

## Provjereni tehnološki slog

Za interne poslovne aplikacije koje koristi nekoliko ljudi na lokalnoj mreži:

```
FastAPI + SQLAlchemy 2.0 + SQLite
Jinja2 + HTMX + Alpine.js + Tailwind (CDN)
Uvicorn, pokretanje kroz run.bat
```

Zašto baš to:

- **FastAPI** je brz za pisanje, ima ugrađenu validaciju i `TestClient` za provjere
- **SQLite** ne traži instalaciju poslužitelja ni administratorske ovlasti
- **HTMX** daje osjećaj jednostraničnе aplikacije bez gradnje i bez npm-a
- **Tailwind s CDN-a** je prihvatljiv za interne alate jer nema koraka gradnje

Streamlit je odbačen nakon usporedbe: sporiji je i manje se da oblikovati. Za
prototip je dobar, za alat koji ljudi koriste svaki dan nije.

**Napomena o Tailwind CDN-u:** prihvatljiv je interno, ali ne za javne stranice
koje prodaju brzinu. Play CDN kompajlira u pregledniku, oko 380 kB JavaScripta i
bljesak neoblikovanog sadržaja. Za javne stranice pisati CSS ručno s varijablama.

## Raspored mapa

```
Aplikacija/
├── app/
│   ├── core/
│   │   ├── config.py         # pydantic-settings, čita .env
│   │   ├── database.py       # engine, SessionLocal, Base, get_db
│   │   ├── templating.py     # JEDNA Jinja okolina za sve module
│   │   └── backup.py         # auto_backup() na startu
│   ├── modules/
│   │   └── <modul>/
│   │       ├── models.py     # SQLAlchemy modeli
│   │       ├── routes.py     # APIRouter s prefiksom
│   │       ├── service.py    # poslovna logika, bez HTTP-a
│   │       └── utils.py
│   ├── templates/
│   │   ├── base.html
│   │   └── <modul>/
│   └── main.py               # include_router, middleware, migracije
├── .venv/                    # u .gitignore
├── data/                     # učitane datoteke, u .gitignore
├── backup/                   # u .gitignore
├── requirements.txt
├── .env.example
├── run.bat
├── dev-wifi.bat
├── CLAUDE.md
└── README.md
```

Ključno: **poslovna logika ide u `service.py`, ne u `routes.py`.** Rute samo
primaju zahtjev, zovu servis i vraćaju predložak. Tako se logika da testirati bez
HTTP sloja i kasnije preseliti u drugu aplikaciju.

## Jedna Jinja okolina za sve module

Svaki router koji si sam stvori `Jinja2Templates` dobiva **svoju** okolinu.
Filtri i globalne funkcije registrirane u jednoj tada ne postoje u drugima.

Zato postoji `app/core/templating.py`:

```python
from fastapi.templating import Jinja2Templates
from pathlib import Path

templates = Jinja2Templates(directory=str(Path(__file__).parents[1] / "templates"))
templates.env.filters["hr"] = hr_broj
templates.env.filters["hrg"] = hr_broj_kratki
templates.env.globals["has_perm"] = has_perm
```

Svi routeri rade `from app.core.templating import templates`. Bez toga se
događa da `has_perm` radi u jednom modulu, a u drugom ruši predložak.

## Izdvajanje samostalne aplikacije iz većeg sustava

Kada modul iz velikog sustava treba postati zasebna aplikacija, provjeren je
pristup **kopije uz zadržavanje istog imenskog prostora**:

1. Zadržati isti `app.` namespace u novoj aplikaciji.
2. Kopirati `app/modules/<modul>/*` i `app/templates/<modul>/*` doslovno,
   bez ijedne izmjene uvoza.
3. Napisati novo samo: `core/config.py`, `core/database.py`, `main.py`,
   `templates/base.html`, `requirements.txt`, `run.bat`.

Uvjet da kopija prođe čisto: modul ne smije imati unakrsne uvoze prema drugim
modulima. Jedina vanjska ovisnost predložaka smije biti `base.html`.

Cijena pristupa: dvije kopije koje se ručno usklađuju. To je prihvatljivo kada
se modul rijetko mijenja. Za module koji se često mijenjaju bolje je dijeljeni
paket s jasnom granicom.

**Provjeriti prije kopiranja:** ako `routes.py` gradi putanju do predložaka iz
radne mape, promijeniti u `Path(__file__).parents[2] / "templates"` da ne ovisi
o tome odakle je aplikacija pokrenuta.

## Granica prema vanjskom sustavu

Kada aplikacija čita iz tuđeg ERP-a, ne zvati ga izravno iz servisa. Uvesti
adapter:

```python
class ErpAdapter:
    def lookup_barcode(self, barkod: str) -> ArtiklInfo: ...

class MockAdapter(ErpAdapter):   # razvoj, stvarni uzorak podataka
class RestAdapter(ErpAdapter):   # produkcija
```

Odabir preko `.env` (`ERP_ADAPTER=mock|rest`). Time se cijela aplikacija razvije
i testira prije nego vanjski sustav uopće ima sučelje, a puštanje u rad je
promjena jedne varijable okoline.

Ako sučelje tek nastaje, **mi definiramo ugovor**, a njihova strana gradi prema
njemu. U ugovor odmah upisati:

- datumi u ISO 8601 obliku
- količine kao brojevi, ne tekst

Time se unaprijed sprječavaju greške sortiranja i zbrajanja opisane u
[13 Katalog zamki](13-katalog-zamki.md).

Za prvu verziju vrijedi pravilo **samo čitanje**. Pisanje natrag u tuđi sustav
tek uz izričito odobrenje.

## Namjerna odstupanja se dokumentiraju

Kada nova aplikacija svjesno odstupa od obrasca svoje braće, to se zapisuje u
`CLAUDE.md` s razlogom. Primjeri stvarnih odstupanja:

- bez prijave, jer je aplikacija jednokorisnička i ne dira osobne podatke
- `pandas` umjesto čistog `openpyxl`, jer se prenosi već provjerena logika
- `CLAUDE.md` ide u git, iako je kod ostalih greškom u `.gitignore`

Bez zapisa razloga sljedeći čitatelj to vidi kao nedosljednost i "popravi".

## Redoslijed gradnje modula

Provjeren redoslijed za sustav koji upravlja materijalima i proizvodnjom:

1. **Šifrarnik materijala** je temelj, jer ga i strojevi i normativi referenciraju
2. **Strojevi**
3. **Normativi**, koji spajaju prva dva
4. tek onda tokovi koji ih koriste (planiranje, skladište, kalkulacije)

Za skladišni modul: model podataka, prijava, glavni tok (zaprimanje, smještaj,
izdavanje, inventura), karta, veza na ERP, izvještaji.
