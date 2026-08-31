# 06 PDF, Word i grafika

## ReportLab i hrvatski znakovi

Ugrađeni fontovi nemaju č, ć, š, ž, đ. Registrirati TrueType font:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def _font_datoteka():
    kandidati = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans.ttf",
    ]
    for k in kandidati:
        if k.exists():
            return k
    raise RuntimeError("Nema dostupnog fonta s hrvatskim znakovima")

pdfmetrics.registerFont(TTFont("Glavni", str(_font_datoteka())))
```

Pričuvni font je bitan: putanja `C:/Windows/Fonts` ne postoji u Linux spremniku,
pa testovi u oblaku padnu ako se font traži samo tamo. DejaVu iz matplotliba je
pouzdan pričuvni izbor.

**Arial nema znakove ✓ i ☐.** Umjesto njih se ispiše prazan kvadratić. Za oznaku
stanja koristiti boju retka i podebljanje, ne simbole.

## Provjera izgleda PDF-a

Preglednik u načinu bez sučelja **ne renderira sadržaj PDF-a**, pa snimka zaslona
ne dokazuje ništa. Za stvarnu provjeru rasterizirati stranicu:

```python
import fitz                      # pymupdf
stranica = fitz.open("izlaz.pdf")[0]
stranica.get_pixmap(dpi=110).save("provjera.png")
```

Pa pogledati sliku.

## Preuzimanje datoteke iz preglednika

Ako se PDF vraća kao odgovor na `hx-post`, HTMX ga ubaci u DOM umjesto da ga
preuzme. Za preuzimanje koristiti `fetch` i `blob`:

```javascript
const odgovor = await fetch(url, { method: "POST", body: new FormData(forma) });
const blob = await odgovor.blob();
const a = document.createElement("a");
a.href = URL.createObjectURL(blob);
a.download = ime;
a.click();
```

### Zamka: hrvatski znakovi u nazivu datoteke

Zaglavlje `Content-Disposition` koristi latin-1. Naziv s "leđna" ruši odgovor sa
statusom 500. Transliterirati prije slanja:

```python
def _ascii_ime(tekst: str) -> str:
    zamjene = {"č": "c", "ć": "c", "š": "s", "ž": "z", "đ": "d",
               "Č": "C", "Ć": "C", "Š": "S", "Ž": "Z", "Đ": "D"}
    for a, b in zamjene.items():
        tekst = tekst.replace(a, b)
    return re.sub(r"[^A-Za-z0-9._-]", "_", tekst)
```

## Word: postojeći dokument kao predložak

Kada u tvrtki postoji nekoliko tisuća starih dokumenata i nijedan nije predložak
(nema `.dot`, nema `{{polje}}`), ne treba raditi novi predložak.

Provjeren pristup: **svaki postojeći dokument je predložak**, a vrijednosti se
traže iza oznaka koje su iste kroz sve kupce i jezike. Tako svaki stari dokument
radi odmah, bez pripreme.

Tablice se prenose doslovnim kopiranjem XML čvora `<w:tbl>` iz izvornog dokumenta,
čime se čuva oblikovanje.

Automatske dorade koje se isplati raditi u istom prolazu: uklanjanje zastarjelih
redaka, zamjena naziva radnog mjesta, pretvaranje utipkanog datuma u praznu crtu
kada se datum stavlja datumarom.

## Ghostscript za separacije boja

Za mjerenje pokrivenosti bojom po separaciji koristi se `tiffsep`, koji daje po
jednu osmobitnu ploču za svaku separaciju, uključujući imenovane spot boje.
Obično RGB renderiranje ne može rekonstruirati pokrivenost po ploči.

**U izlazu `tiffsep` vrijednost 255 znači odsutnost boje.**

Instalacija bez administratorskih ovlasti: instalacijski program traži povišenje
ovlasti, ali se arhiva može raspakirati. Za NSIS arhive potreban je puni 7-Zip s
`7z.dll`, samostalni `7za.exe` ih ne otvara.

### Pronalaženje etikete u PDF-u

Rasterska analiza ne radi pouzdano. Dva stvarna načina na koja pada:

1. Linije kota dijele istu separaciju kao rezna linija i zatvaraju dodatna
   područja, pa se etiketa od 95 x 95 mm prikaže kao 95 x 106.
2. Na zaobljenim etiketama radijalne linije presijecaju unutrašnjost i dijele je
   na sedam dijelova.

Pouzdano rješenje je filtrirati **vektorske putanje** po tome leži li rub na
separaciji rezne linije. Razlikovanje je oštro: prava kontura daje vrijednost
između 0,88 i 1,00, linije kota između 0,00 i 0,02.

Tehničke separacije isključiti iz zbroja po nazivu, uz popis riječi na više
jezika (CUT, CUTTER, CONTOUR, TRACCIATO, FUSTELLA, TAGLIO, CORDONATURA,
SUBSTRAT, crease).

### Model potrošnje boje

Prvi model je uključivao površinu etikete u kvadratnim metrima i davao je otprilike
deset puta premale brojeve. Ispravljeni model:

```
kg/1000 = broj_etiketa × (pokrivenost / 100) × konstanta
```

Konstanta se kalibrira na poznatom poslu, zadana vrijednost je 1,0. Pouka je
šira od ovog slučaja: kada model daje red veličine promašaja, problem je u
postavci modela, ne u podacima.

## Pakiranje u samostalni program

PyInstaller u načinu `onedir`, ne `onefile`, kada se uz program isporučuje i
vanjski alat.

- Kopira se **cijela mapa**, ne samo `.exe`. Mapa `_internal` sadrži biblioteke.
- Vanjski alat spakirati obrezan, samo ono što treba za rad.
- Traženje alata redom: `sys._MEIPASS`, mapa programa, pa tek onda sustav.
- **Kada je program zamrznut, zadana mapa nije `Path(__file__).parent`,** jer to
  pokazuje u `_internal`. Koristiti mapu izvršne datoteke.
- Znanstvene biblioteke znaju činiti većinu veličine. Prihvatljivo je ostaviti ih
  ako zamjena ugrožava točnost.

## Grafovi

Za PDF izvoz iz matplotliba dovoljno je `savefig(format="pdf")`.

Za grafove u pregledniku koristi se Chart.js s CDN-a. Zamka: adapter za datume
zna biti nepouzdan i vraćati 404. Sigurnije je koristiti linearnu os s
vremenskim oznakama u milisekundama i sam oblikovati oznake.
