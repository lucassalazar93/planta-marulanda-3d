"""Incrusta edificio.json en el visor (sala3d-marulanda.html), entre /*EDIFICIO*/ y /*FIN EDIFICIO*/.

    python herramientas/edificio/incrustar.py herramientas/edificio/edificio.json sala3d-marulanda.html

Deja fuera los trazos de escalera y los textos de lavamanos (el visor dibuja escaleras y lavamanos con sus propias medidas).
"""
import json, sys

src, html = sys.argv[1:3]
d = json.load(open(src, encoding="utf-8"))
for p in d["pisos"]:
    p.pop("escaleras", None)
    p.pop("lavamanos", None)
txt = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
h = open(html, encoding="utf-8").read()
a, b = h.index("/*EDIFICIO*/"), h.index("/*FIN EDIFICIO*/")
h = h[:a] + "/*EDIFICIO*/" + txt + h[b:]
open(html, "w", encoding="utf-8", newline="\n").write(h)
print(f"edificio incrustado: {len(txt) / 1024:.1f} kB")
