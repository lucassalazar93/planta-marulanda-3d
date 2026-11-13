"""Lee el DXF una sola vez y guarda en JSON: textos, y segmentos/círculos/bloques de las capas de arquitectura,
para poder recortar cada planta sin volver a leer los 281 MB."""
import sys, json, math, re, collections
from ezdxf import recover

src, out = sys.argv[1:3]
doc, _ = recover.readfile(src)
msp = doc.modelspace()
CAPAS = None  # todas
clean = lambda s: re.sub(r"[\ud800-\udfff]", "?", s or "")

segs = collections.defaultdict(list)
circ = collections.defaultdict(list)
txt = []
ins = []


def seg_add(layer, x1, y1, x2, y2):
    segs[layer].append([round(x1, 4), round(y1, 4), round(x2, 4), round(y2, 4)])


def proc(e, lay=None, depth=0):
    t = e.dxftype()
    layer = lay or e.dxf.layer
    try:
        if t == "LINE":
            a, b = e.dxf.start, e.dxf.end
            seg_add(layer, a.x, a.y, b.x, b.y)
        elif t in ("LWPOLYLINE", "POLYLINE"):
            pts = [(p[0], p[1]) for p in e.get_points("xy")] if t == "LWPOLYLINE" else [(v.dxf.location.x, v.dxf.location.y) for v in e.vertices]
            closed = e.closed if t == "LWPOLYLINE" else e.is_closed
            if closed and pts:
                pts.append(pts[0])
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                seg_add(layer, x1, y1, x2, y2)
        elif t == "ARC":
            c, r = e.dxf.center, e.dxf.radius
            a0, a1 = math.radians(e.dxf.start_angle), math.radians(e.dxf.end_angle)
            if a1 < a0:
                a1 += 2 * math.pi
            n = max(4, int((a1 - a0) / 0.2))
            pts = [(c.x + r * math.cos(a0 + (a1 - a0) * i / n), c.y + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                seg_add(layer + "|arc", x1, y1, x2, y2)
        elif t == "CIRCLE":
            c = e.dxf.center
            circ[layer].append([round(c.x, 4), round(c.y, 4), round(e.dxf.radius, 4)])
        elif t in ("TEXT", "MTEXT"):
            p = e.dxf.insert
            s = e.plain_text() if t == "MTEXT" else e.dxf.text
            if s and s.strip():
                txt.append([layer, round(p.x, 3), round(p.y, 3), clean(s).replace("\n", " | ")[:120]])
        elif t == "INSERT" and depth < 3:
            p = e.dxf.insert
            ins.append([e.dxf.name, layer, round(p.x, 3), round(p.y, 3), round(e.dxf.get("rotation", 0), 2)])
            for ve in e.virtual_entities():
                proc(ve, None if ve.dxf.layer != "0" else layer, depth + 1)
    except Exception:
        pass


for e in msp:
    if e.dxftype() in ("HATCH", "SPLINE", "DIMENSION", "POINT", "SOLID", "IMAGE", "OLE2FRAME", "VIEWPORT"):
        continue
    proc(e)

json.dump({"segs": segs, "circ": circ, "txt": txt, "ins": ins}, open(out, "w", encoding="utf-8"))
print("capas:", len(segs), "segmentos:", sum(len(v) for v in segs.values()), "textos:", len(txt), "bloques:", len(ins))
