#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mdskills - lokalni alat za pregled, izmjenu i izradu .md datoteka i skillova.

Pokretanje:   python server.py
Otvori:       http://127.0.0.1:7777

Bez ijedne vanjske ovisnosti: samo Python standardna biblioteka.
Slusa iskljucivo na 127.0.0.1, pa nije dostupan s mreze.
Svaki put se provjerava da je unutar dopustenih korijena (config.json),
tako da API ne moze pisati izvan njih.
"""

import json
import os
import re
import shutil
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "config.json")
HOST, PORT = "127.0.0.1", 7777
MAX_BYTES = 4 * 1024 * 1024          # 4 MB po datoteci, dovoljno za bilo koji .md
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".trash", ".venv", "venv"}

DEFAULT_CONFIG = {
    "roots": [
        {"label": "Skills (agents)", "path": "~/.agents/skills", "kind": "skills"},
        {"label": "Skills (claude)", "path": "~/.claude/skills", "kind": "skills"},
        {"label": "Memory", "path": "~/.claude/projects/C--Users-krist/memory", "kind": "md"},
        {"label": "SiteSpec", "path": "~/Desktop/SiteSpec", "kind": "md"},
        {"label": "Biljeznica", "path": "~/mdskills/notes", "kind": "md"},
    ]
}


# ------------------------------------------------------------------
# Konfiguracija i putovi
# ------------------------------------------------------------------
def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    out = []
    for r in cfg.get("roots", []):
        p = os.path.abspath(os.path.expanduser(r["path"]))
        out.append({"label": r.get("label") or os.path.basename(p),
                    "path": p,
                    "kind": r.get("kind", "md"),
                    "exists": os.path.isdir(p)})
    return out


ROOTS = load_config()


def root_for(path):
    """Vrati korijen kojem put pripada, ili None. Blokira traversal."""
    ap = os.path.abspath(path)
    for r in ROOTS:
        try:
            if os.path.commonpath([ap, r["path"]]) == r["path"]:
                return r
        except ValueError:          # razliciti diskovi na Windowsu
            continue
    return None


def safe(path):
    ap = os.path.abspath(os.path.expanduser(path))
    if root_for(ap) is None:
        raise PermissionError("put je izvan dopustenih korijena: %s" % ap)
    return ap


def slugify(name):
    s = name.strip().lower()
    for a, b in (("č", "c"), ("ć", "c"), ("ž", "z"), ("š", "s"), ("đ", "d")):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "bez-naziva"


# ------------------------------------------------------------------
# Citanje strukture
# ------------------------------------------------------------------
def read_frontmatter(path):
    """Vrati (dict, ima_frontmatter). Cita samo prvih 4 kB."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = f.read(4096)
    except OSError:
        return {}, False
    if not head.startswith("---"):
        return {}, False
    end = head.find("\n---", 3)
    if end == -1:
        return {}, False
    meta = {}
    in_metadata = False
    for line in head[3:end].splitlines():
        if not line.strip():
            continue
        indented = line[0] in " \t"
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if not indented:
            in_metadata = (k == "metadata")
            meta[k] = v
        elif in_metadata and k == "type":
            meta["metadata_type"] = v
    return meta, True


TYPE_WORDS = ("project", "feedback", "reference", "user", "memory", "skill")


def prettify(stem):
    """iz `project_kai_sol_site` napravi `Kai Sol Site`"""
    parts = [p for p in re.split(r"[-_\s]+", stem.strip()) if p]
    if len(parts) > 1 and parts[0].lower() in TYPE_WORDS:
        parts = parts[1:]
    out = [p if (p.isupper() or any(c.isdigit() for c in p)) else p.capitalize()
           for p in parts]
    return " ".join(out) or stem


def describe(path, meta):
    """Vrati (naslov, jedna linija o cemu je, sifra arhetipa ili "").

    Naslov: prvi naslov u tekstu, pa slug iz frontmattera, pa ime datoteke.
    Linija: `description` iz frontmattera, pa prva prava recenica teksta.
    Cilj je da se u popisu vidi sto je datoteka bez otvaranja."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = f.read(4096)
    except OSError:
        head = ""

    body = head
    if body.startswith("---"):
        end = body.find("\n---", 3)
        if end != -1:
            body = body[end + 4:]

    title, code = "", ""
    m = re.search(r"^#{1,6}[ \t]+(.+?)[ \t]*#*$", body, re.M)
    if m:
        title = re.sub(r"^[#\s]+", "", m.group(1).strip())
    if not title:
        title = prettify(meta.get("name") or
                         os.path.splitext(os.path.basename(path))[0])

    # Ocisti naslov: bez backtickova, bez zvjezdica, bez rijeci "hallmark".
    title = re.sub(r"[`*]", "", title).strip()
    title = re.sub(r"^hallmark\s+", "", title, flags=re.I)

    # Sifra arhetipa na pocetku (H8, Ft5, N1b, C1, HP3) nije ime nego oznaka:
    # izvadi je u zasebno polje pa je prikazi sitno sa strane.
    mc = re.match(r"^([A-Za-z]{1,3}\d{1,2}[a-z]?)\s*[\u00b7:\u2013\u2014-]\s*(.+)$", title)
    if mc:
        code, title = mc.group(1), mc.group(2).strip()

    # Podnaslov odvojen crticom je opis, ne dio imena.
    ms = re.match(r"^(.{3,}?)\s+[\u2013\u2014]\s+(.+)$", title)
    tail = ""
    if ms:
        title, tail = ms.group(1).strip(), ms.group(2).strip()

    blurb = (meta.get("description") or "").strip() or tail
    if not blurb:
        after = body[m.end():] if m else body
        for raw in after.splitlines():
            line = raw.strip()
            if not line or line.startswith(("#", "|", "```", "---", "<!--", "!")):
                continue
            line = re.sub(r"^\s*>+\s*", "", line)                 # citat
            line = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", line)    # oznaka popisa
            line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line)  # [tekst](veza) -> tekst
            line = re.sub(r"[*_`]", "", line).strip()
            if len(line) > 12:
                blurb = line
                break
    blurb = " ".join(blurb.split())
    if len(blurb) > 150:
        cut = blurb[:150].rsplit(" ", 1)[0]
        blurb = cut + "\u2026"
    return title, blurb, code


def file_entry(path, root):
    st = os.stat(path)
    rel = os.path.relpath(path, root["path"]).replace("\\", "/")
    meta, _has = read_frontmatter(path)
    # fmname: slug iz frontmattera. Veze u dvostrukim uglatim zagradama
    # gadaju njega, a ne ime datoteke, pa mora biti u popisu.
    title, blurb, code = describe(path, meta)
    return {"path": path.replace("\\", "/"), "rel": rel,
            "name": os.path.basename(path), "size": st.st_size,
            "title": title, "blurb": blurb, "code": code,
            "kindtag": meta.get("metadata_type") or "",
            "fmname": meta.get("name"), "mtime": int(st.st_mtime)}


def list_md(root, base=None, depth=0):
    base = base or root["path"]
    out = []
    if depth > 6 or not os.path.isdir(base):
        return out
    try:
        names = sorted(os.listdir(base))
    except OSError:
        return out
    for n in names:
        p = os.path.join(base, n)
        if os.path.isdir(p):
            if n not in SKIP_DIRS and not n.startswith("."):
                out.extend(list_md(root, p, depth + 1))
        elif n.lower().endswith((".md", ".markdown", ".mdc")):
            out.append(file_entry(p, root))
    return out


def list_skills(root):
    """Svaki poddirektorij sa SKILL.md je skill; skupi i njegove reference."""
    skills = []
    if not os.path.isdir(root["path"]):
        return skills
    for n in sorted(os.listdir(root["path"])):
        d = os.path.join(root["path"], n)
        if not os.path.isdir(d):
            continue
        skill_md = None
        for cand in ("SKILL.md", "skill.md"):
            if os.path.exists(os.path.join(d, cand)):
                skill_md = os.path.join(d, cand)
                break
        if not skill_md:
            continue
        meta, has_fm = read_frontmatter(skill_md)
        refs = []
        for sub, _dirs, files in os.walk(d):
            if os.path.basename(sub) in SKIP_DIRS:
                continue
            for f in sorted(files):
                p = os.path.join(sub, f)
                if p == skill_md:
                    continue
                if f.lower().endswith((".md", ".markdown", ".mdc")):
                    refs.append(file_entry(p, root))
        problems = []
        if not has_fm:
            problems.append("nema frontmattera")
        else:
            if not meta.get("name"):
                problems.append("nema polja name")
            elif meta["name"] != n:
                problems.append("name (%s) != ime mape (%s)" % (meta["name"], n))
            if not meta.get("description"):
                problems.append("nema polja description")
        skills.append({
            "dir": d.replace("\\", "/"), "folder": n,
            "skill": file_entry(skill_md, root),
            "meta": meta, "refs": refs, "problems": problems,
            "symlink": os.path.islink(d),
        })
    return skills


def build_tree():
    tree = []
    for r in ROOTS:
        node = {"label": r["label"], "path": r["path"].replace("\\", "/"),
                "kind": r["kind"], "exists": r["exists"]}
        if not r["exists"]:
            node["files"], node["skills"] = [], []
        elif r["kind"] == "skills":
            node["skills"] = list_skills(r)
            node["files"] = []
        else:
            node["files"] = list_md(r)
            node["skills"] = []
        tree.append(node)
    return tree


# ------------------------------------------------------------------
# Pisanje
# ------------------------------------------------------------------
def write_atomic(path, text):
    tmp = path + ".tmp~"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


def to_trash(path):
    root = root_for(path)
    trash = os.path.join(root["path"], ".trash")
    os.makedirs(trash, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    dest = os.path.join(trash, "%s__%s" % (stamp, os.path.basename(path)))
    shutil.move(path, dest)
    return dest


SKILL_TEMPLATE = """---
name: %(slug)s
description: "%(desc)s"
---

# %(title)s

%(desc)s

## Kada se koristi

- <situacija u kojoj ovaj skill ima smisla>

## Kako radi

1. <prvi korak>
2. <drugi korak>

## Pravila

- <sto se uvijek radi>
- <sto se nikad ne radi>
"""

NOTE_TEMPLATE = """# %(title)s

<sadrzaj>
"""


# ------------------------------------------------------------------
# HTTP
# ------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "mdskills/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))

    # ---- helpers ----
    def send_json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path, ctype):
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def body_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > MAX_BYTES:
            raise ValueError("neispravna velicina tijela zahtjeva")
        return json.loads(self.rfile.read(n).decode("utf-8"))

    # ---- GET ----
    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path in ("/", "/index.html"):
                return self.send_file(os.path.join(HERE, "app.html"),
                                      "text/html; charset=utf-8")
            if u.path == "/api/tree":
                global ROOTS
                ROOTS = load_config()
                return self.send_json({"roots": build_tree()})
            if u.path == "/api/file":
                p = safe(q.get("path", [""])[0])
                if not os.path.isfile(p):
                    return self.send_json({"error": "datoteka ne postoji"}, 404)
                if os.path.getsize(p) > MAX_BYTES:
                    return self.send_json({"error": "datoteka je prevelika"}, 413)
                with open(p, encoding="utf-8", errors="replace") as f:
                    text = f.read()
                meta, has_fm = read_frontmatter(p)
                return self.send_json({"path": p.replace("\\", "/"), "content": text,
                                       "meta": meta, "frontmatter": has_fm,
                                       "mtime": int(os.stat(p).st_mtime * 1000)})
            return self.send_json({"error": "nepoznata ruta"}, 404)
        except PermissionError as e:
            return self.send_json({"error": str(e)}, 403)
        except Exception as e:                                  # noqa: BLE001
            return self.send_json({"error": "%s: %s" % (type(e).__name__, e)}, 500)

    # ---- POST ----
    def do_POST(self):
        u = urlparse(self.path)
        try:
            data = self.body_json()

            if u.path == "/api/save":
                p = safe(data["path"])
                if not os.path.isfile(p):
                    return self.send_json({"error": "datoteka ne postoji"}, 404)
                # Sprijeci tiho gazenje izmjene napravljene izvan alata.
                if data.get("mtime") and int(data["mtime"]) != int(os.stat(p).st_mtime * 1000):
                    return self.send_json(
                        {"error": "datoteka je promijenjena izvan alata. "
                                  "Osvjezite prikaz pa ponovno spremite."}, 409)
                write_atomic(p, data["content"])
                return self.send_json({"ok": True, "mtime": int(os.stat(p).st_mtime * 1000)})

            if u.path == "/api/new-note":
                root = safe(data["root"])
                name = data.get("name") or "nova-biljeska"
                if not name.lower().endswith(".md"):
                    name = slugify(name) + ".md"
                p = safe(os.path.join(root, name))
                if os.path.exists(p):
                    return self.send_json({"error": "datoteka vec postoji"}, 409)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                title = data.get("title") or os.path.splitext(os.path.basename(p))[0]
                write_atomic(p, NOTE_TEMPLATE % {"title": title})
                return self.send_json({"ok": True, "path": p.replace("\\", "/")})

            if u.path == "/api/new-skill":
                root = safe(data["root"])
                slug = slugify(data.get("name") or "")
                desc = (data.get("description") or "").replace('"', "'").strip()
                d = safe(os.path.join(root, slug))
                if os.path.exists(d):
                    return self.send_json({"error": "skill s tim imenom vec postoji"}, 409)
                os.makedirs(os.path.join(d, "references"), exist_ok=True)
                title = data.get("name") or slug
                write_atomic(os.path.join(d, "SKILL.md"), SKILL_TEMPLATE % {
                    "slug": slug, "desc": desc or "Opis skilla.", "title": title})
                return self.send_json({"ok": True,
                                       "path": os.path.join(d, "SKILL.md").replace("\\", "/")})

            if u.path == "/api/new-ref":
                skill_dir = safe(data["dir"])
                name = data.get("name") or "nova-referenca"
                if not name.lower().endswith(".md"):
                    name = slugify(name) + ".md"
                refs = os.path.join(skill_dir, "references")
                os.makedirs(refs, exist_ok=True)
                p = safe(os.path.join(refs, name))
                if os.path.exists(p):
                    return self.send_json({"error": "referenca vec postoji"}, 409)
                write_atomic(p, NOTE_TEMPLATE % {
                    "title": os.path.splitext(os.path.basename(p))[0]})
                return self.send_json({"ok": True, "path": p.replace("\\", "/")})

            if u.path == "/api/trash":
                p = safe(data["path"])
                if not os.path.exists(p):
                    return self.send_json({"error": "ne postoji"}, 404)
                dest = to_trash(p)
                return self.send_json({"ok": True, "trashed": dest.replace("\\", "/")})

            return self.send_json({"error": "nepoznata ruta"}, 404)

        except PermissionError as e:
            return self.send_json({"error": str(e)}, 403)
        except KeyError as e:
            return self.send_json({"error": "nedostaje polje %s" % e}, 400)
        except Exception as e:                                  # noqa: BLE001
            return self.send_json({"error": "%s: %s" % (type(e).__name__, e)}, 500)


def main():
    print("mdskills")
    print("  korijeni:")
    for r in ROOTS:
        print("    %-18s %s%s" % (r["label"], r["path"],
                                  "" if r["exists"] else "   (ne postoji)"))
    url = "http://%s:%d/" % (HOST, PORT)
    print("\n  otvori: %s      (Ctrl+C za prekid)\n" % url)
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        if "--no-browser" not in sys.argv:
            webbrowser.open(url)
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  prekinuto")
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
