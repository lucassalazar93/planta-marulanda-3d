"""Arma el modelo del edificio (pisos -1, 1 y 2) a partir del DWG arquitectónico ya convertido.

    python herramientas/edificio/construir_edificio.py <dxf_cache.json> <salida edificio.json> [png de control]

dxf_cache.json sale de herramientas/edificio/dxf_cache.py (lee el DXF una vez). Todo queda en coordenadas
del piso 1 del DWG, las mismas que usa el visor (X este, Y norte, metros).

Pasos:
1. Toma las capas de muros y columnas de cada planta y las lleva a coordenadas del piso 1 (los tres pisos
   comparten ejes: A-B 3,5 · B-C 5,0 · C-D 6,3 m).
2. Une líneas duplicadas y empareja las caras paralelas de cada muro (0,07 a 0,42 m) -> tramos de muro.
3. Los huecos entre tramos de un mismo muro son puertas (si hay un arco de puerta cerca) o ventanas.
4. Rasteriza muros y vanos cerrados a 5 cm y rellena desde cada nombre de recinto -> contorno y área de cada sala.
"""
import sys, json, math, re, collections
from collections import deque
import numpy as np
from matplotlib.path import Path
import contourpy

cache_path, salida = sys.argv[1:3]
png = sys.argv[3] if len(sys.argv) > 3 else None
d = json.load(open(cache_path, encoding="utf-8"))

PISOS = {
    "p-1": dict(nombre="Piso -1", reg=(300, 372, -40, 15), dx=62.44, dy=0.0, nivel="N -2,85", y0=-3.0, alto=3.0),
    "p1": dict(nombre="Piso 1", reg=(372, 440, -40, 15), dx=0.0, dy=0.0, nivel="N +0,15", y0=0.0, alto=3.04),
    "p2": dict(nombre="Piso 2", reg=(440, 520, -40, 15), dx=-70.36, dy=1.87, nivel="N +3,19", y0=3.04, alto=2.7),
}
CLIP = (379.6, 430.0, -22.0, -4.6)
GARITA = (379.6, 382.2, -15.8, -13.0)
CAPAS_MURO = {"Muro", "ESTRUCTURA", "A-ECON-COLS"}
# Zonas que ya modela el visor a mano (muros de recibo, producción 1 y la «L»): el DWG no se repite ahí
ZONA_PROD = [(387.80, 392.42, -15.48, -9.52), (392.10, 410.95, -15.48, -9.52), (405.50, 410.95, -20.72, -15.20)]
# Cierres manuales (solo para el relleno, no son muros): puertas anchas, accesos abiertos y divisiones sin muro
CIERRES = {
    "p-1": [((394.15, -8.25), (394.15, -9.75)), ((405.55, -8.25), (405.55, -9.75))],
    "p1": [((405.62, -15.353), (410.80, -15.353)),   # zona 1 | la «L»
           ((394.17, -15.30), (394.17, -17.50)),     # acceso oeste a entrega de producto
           ((405.60, -15.30), (405.60, -16.75)),     # entrega | producción 2
           ((399.20, -17.45), (401.60, -17.45)),     # escalera al almacén de empaques
           ((394.10, -8.38), (395.75, -8.38)),       # puerta del carbón
           ((394.15, -8.25), (394.15, -9.75)), ((405.55, -8.25), (405.55, -9.75)),  # hall de calderas
           ((416.20, -13.95), (416.20, -15.40)),     # bienestar | zona administrativa
           ((417.75, -15.25), (417.75, -16.70)),     # puerta baños 1
           ((417.75, -17.95), (417.75, -19.45)),     # puerta baños 2
           ((416.05, -19.30), (416.05, -20.65)),     # puerta cuarto de lavado
           ((415.95, -19.38), (417.80, -19.38)),     # cuarto de lavado, costado norte
           ((421.00, -13.90), (421.00, -15.40)),     # atención al usuario, costado este
           ((421.00, -17.90), (421.00, -20.70)),     # baños 2, costado este
           ((414.00, -17.45), (414.00, -20.65))],    # escalera a la oficina
    "p2": [((405.62, -15.353), (410.80, -15.353)),
           ((399.20, -17.40), (401.60, -17.40))],
}
# Muros del visor que también cierran recintos (recibo) para el relleno
# Muros que dibuja el visor (sala3d-marulanda.html, MUROS): en la zona del visor reemplazan a los del DWG
_ZONA1 = [(387.85, 410.864, -9.707, -9.577), (387.85, 405.684, -15.418, -15.288), (387.85, 387.98, -15.418, -9.577),
          (392.233, 392.363, -15.288, -9.707), (410.734, 410.864, -15.288, -9.577), (405.684, 410.734, -15.418, -15.288)]
_L = [(410.734, 410.864, -20.668, -15.288), (405.554, 405.684, -20.668, -15.418), (405.554, 410.864, -20.668, -20.538)]
MUROS_VISOR = {"p1": _ZONA1 + _L, "p2": _ZONA1}

NOMBRES = [  # (patrón, nombre, tipo)
    (r"PRODUCCI.N\s*\|\s*ZONA 1", "Zona de producción 1", "produccion"),
    (r"PRODUCCI.N\s*\|\s*ZONA 2", "Zona de producción 2", "produccion"),
    (r"CUARTO FRIO", "Cuarto frío", "frio"),
    (r"ENTREGA DE\s+PRODUCTO", "Zona de entrega de producto", "produccion"),
    (r"CALDERAS", "Zona de calderas", "tecnico"),
    (r"CARBON", "Almacenamiento de carbón", "tecnico"),
    (r"LABORATORIO", "Laboratorio", "laboratorio"),
    (r"ATENCI.N AL USUARIO", "Atención al usuario", "administrativo"),
    (r"BATERIA DE BA", "Batería de baños", "servicios"),
    (r"ADMINISTRATIVA", "Zona administrativa", "administrativo"),
    (r"VESTUARIO", "Vestuario", "servicios"),
    (r"Planta Electrica", "Planta eléctrica", "tecnico"),
    (r"Bodega", "Bodega", "tecnico"),
    (r"Garita", "Garita", "administrativo"),
    (r"CUARTO DE LAVADO", "Cuarto de lavado", "lavado"),
    (r"BIENESTAR", "Zona de bienestar", "servicios"),
    (r"Residuos", "Cuarto de residuos sólidos", "tecnico"),
    (r"Cuarto\s*\|\s*Almacenamiento", "Cuarto de almacenamiento", "tecnico"),
    (r"ALMACEN\s*\|\s*EMPAQUES", "Almacén de empaques", "produccion"),
    (r"OFICINA", "Oficina", "administrativo"),
    (r"^HALL", "Hall", "circulacion"),
]
MANUALES = {  # (nombre, tipo, x, y, área del plano)
    "p-1": [("Hall del sótano", "circulacion", 400.0, -9.0, None)],
    "p1": [("Zona de recibo", "produccion", 390.1, -12.6, 23.7),
           ("Hall de calderas", "circulacion", 400.0, -9.0, None),
           ("Escalera al almacén de empaques", "escalera", 400.4, -19.0, None),
           ("Escalera a la oficina", "escalera", 412.5, -19.0, None)],
    "p2": [("Doble altura de producción", "vacio", 400.0, -12.5, None),
           ("Doble altura de recibo", "vacio", 390.1, -12.6, None),
           ("Espacio sobre producción 2", "porDefinir", 408.2, -18.0, None),
           ("Escalera", "escalera", 400.4, -19.0, None)],
}


def en(r, x, y):
    return r[0] <= x <= r[1] and r[2] <= y <= r[3]


def a_p1(p, x, y):
    return x + p["dx"], y + p["dy"]


# ---------- 1. segmentos por piso
def segmentos(pid):
    p = PISOS[pid]; x0, x1, y0, y1 = p["reg"]
    out = []
    for capa in CAPAS_MURO:
        for a, b, c, e in d["segs"].get(capa, []):
            if not (x0 <= a <= x1 and y0 <= b <= y1):
                continue
            ax, ay = a_p1(p, a, b); cx, cy = a_p1(p, c, e)
            if not (en(CLIP, ax, ay) and en(CLIP, cx, cy)):
                continue
            if (ax < 386 or cx < 386) and not (en(GARITA, ax, ay) and en(GARITA, cx, cy)):
                continue
            if pid != "p1" and (ax < 389.0 or cx < 389.0):
                continue
            out.append((ax, ay, cx, cy))
    return out


def lineas(segs):
    """Agrupa por ángulo, une duplicados (<3 cm) y devuelve líneas con intervalos."""
    items = []
    for x1, y1, x2, y2 in segs:
        L = math.hypot(x2 - x1, y2 - y1)
        if L < 0.04:
            continue
        ang = math.atan2(y2 - y1, x2 - x1) % math.pi
        if ang > math.pi - 0.004:
            ang -= math.pi
        items.append((ang, x1, y1, x2, y2))
    items.sort()
    grupos, act = [], []
    for it in items:
        if act and it[0] - act[-1][0] > 0.006:
            grupos.append(act); act = []
        act.append(it)
    if act:
        grupos.append(act)
    res = []
    for g in grupos:
        ang = sum(i[0] for i in g) / len(g)
        ux, uy = math.cos(ang), math.sin(ang); nx, ny = -uy, ux
        ls = []
        for _, x1, y1, x2, y2 in g:
            c = (x1 * nx + y1 * ny + x2 * nx + y2 * ny) / 2
            t1, t2 = x1 * ux + y1 * uy, x2 * ux + y2 * uy
            ls.append((c, min(t1, t2), max(t1, t2)))
        ls.sort()
        bloques, b = [], []
        for l in ls:
            if b and l[0] - b[-1][0] > 0.03:
                bloques.append(b); b = []
            b.append(l)
        if b:
            bloques.append(b)
        for bl in bloques:
            c = sum(l[0] for l in bl) / len(bl)
            iv = sorted((l[1], l[2]) for l in bl)
            merged = []
            for a, z in iv:
                if merged and a <= merged[-1][1] + 0.01:
                    merged[-1][1] = max(merged[-1][1], z)
                else:
                    merged.append([a, z])
            res.append(dict(ang=ang, u=(ux, uy), n=(nx, ny), c=c, iv=merged))
    return res


def restar(iv, a, b):
    out = []
    for x, y in iv:
        if y <= a or x >= b:
            out.append([x, y]); continue
        if x < a:
            out.append([x, a])
        if y > b:
            out.append([b, y])
    return [s for s in out if s[1] - s[0] > 0.01]


def intersec(iv1, iv2, a, b):
    out = []
    for x1, y1 in iv1:
        for x2, y2 in iv2:
            lo, hi = max(x1, x2, a), min(y1, y2, b)
            if hi - lo > 0.04:
                out.append((lo, hi))
    return out


def tramos(ls):
    """Empareja caras paralelas -> tramos de muro (cuadriláteros)."""
    por_ang = collections.defaultdict(list)
    for i, l in enumerate(ls):
        por_ang[round(l["ang"], 3)].append(i)
    cands = []
    for idxs in por_ang.values():
        idxs.sort(key=lambda i: ls[i]["c"])
        for k, i in enumerate(idxs):
            for j in idxs[k + 1:]:
                dd = ls[j]["c"] - ls[i]["c"]
                if dd < 0.07:
                    continue
                if dd > 0.42:
                    break
                for x, y in ls[i]["iv"]:
                    for xx, yy in ls[j]["iv"]:
                        lo, hi = max(x, xx), min(y, yy)
                        if hi - lo > 0.04:
                            cands.append((dd, i, j, lo, hi))
    cands.sort()
    disp = [list(map(list, l["iv"])) for l in ls]
    quads = []
    for dd, i, j, lo, hi in cands:
        for a, b in intersec(disp[i], disp[j], lo, hi):
            li, lj = ls[i], ls[j]
            (ux, uy), (nx, ny) = li["u"], li["n"]
            pts = [(a * ux + li["c"] * nx, a * uy + li["c"] * ny), (b * ux + li["c"] * nx, b * uy + li["c"] * ny),
                   (b * ux + lj["c"] * nx, b * uy + lj["c"] * ny), (a * ux + lj["c"] * nx, a * uy + lj["c"] * ny)]
            quads.append(dict(pts=pts, ang=li["ang"], cmid=(li["c"] + lj["c"]) / 2, esp=dd, t=(a, b), u=li["u"], n=li["n"]))
            disp[i] = restar(disp[i], a, b); disp[j] = restar(disp[j], a, b)
    # quitar duplicados (columnas salen dos veces)
    vistos, uniq = set(), []
    for q in quads:
        xs = [p[0] for p in q["pts"]]; ys = [p[1] for p in q["pts"]]
        k = (round(min(xs), 2), round(max(xs), 2), round(min(ys), 2), round(max(ys), 2))
        if k in vistos:
            continue
        vistos.add(k); uniq.append(q)
    return uniq


def arcos(pid):
    p = PISOS[pid]; x0, x1, y0, y1 = p["reg"]; pts = []
    for capa, ss in d["segs"].items():
        if not capa.endswith("|arc"):
            continue
        for a, b, c, e in ss:
            if x0 <= a <= x1 and y0 <= b <= y1:
                pts.append(a_p1(p, (a + c) / 2, (b + e) / 2))
    return np.array(pts) if pts else np.zeros((0, 2))


def vanos(qs, arc_pts):
    pistas = collections.defaultdict(list)
    for q in qs:
        pistas[(round(q["ang"], 3), round(q["cmid"], 2), round(q["esp"], 2))].append(q)
    out = []
    for k, lista in pistas.items():
        lista.sort(key=lambda q: q["t"][0])
        for q1, q2 in zip(lista, lista[1:]):
            a, b = q1["t"][1], q2["t"][0]
            gap = b - a
            if not (0.55 <= gap <= 3.4):
                continue
            (ux, uy), (nx, ny) = q1["u"], q1["n"]; c = q1["cmid"]
            m = ((a + b) / 2 * ux + c * nx, (a + b) / 2 * uy + c * ny)
            p1 = (a * ux + c * nx, a * uy + c * ny); p2 = (b * ux + c * nx, b * uy + c * ny)
            puerta = False
            if len(arc_pts):
                dist = np.hypot(arc_pts[:, 0] - m[0], arc_pts[:, 1] - m[1])
                puerta = bool((dist < gap * 0.95 + 0.15).any())
            out.append(dict(p1=p1, p2=p2, ancho=round(gap, 3), esp=q1["esp"], tipo="puerta" if puerta else "ventana", ang=q1["ang"]))
    return out


def en_prod(pts, margen=0.0, zonas=ZONA_PROD):
    """True si todos los puntos (y el centro) caen dentro de la unión de las zonas del visor."""
    if not zonas:
        return False
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    return all(any(x0 - margen <= x <= x1 + margen and y0 - margen <= y <= y1 + margen for (x0, x1, y0, y1) in zonas)
               for x, y in list(pts) + [(cx, cy)])
    return False


# ---------- 4. salas por relleno
RES = 0.05
CIERRE_M = 0.55


def salas(pid, qs, vs):
    X0, X1, Y0, Y1 = CLIP[0] - 10.0, CLIP[1] + 1.0, CLIP[2] - 1.0, CLIP[3] + 1.0
    W, H = int((X1 - X0) / RES) + 1, int((Y1 - Y0) / RES) + 1
    gx = X0 + (np.arange(W) + 0.5) * RES; gy = Y0 + (np.arange(H) + 0.5) * RES
    muro = np.zeros((H, W), bool)

    def pintar(poly, crecer=0.0):
        pxs = [p[0] for p in poly]; pys = [p[1] for p in poly]
        i0 = max(0, int((min(pxs) - crecer - X0) / RES) - 1); i1 = min(W, int((max(pxs) + crecer - X0) / RES) + 2)
        j0 = max(0, int((min(pys) - crecer - Y0) / RES) - 1); j1 = min(H, int((max(pys) + crecer - Y0) / RES) + 2)
        if i1 <= i0 or j1 <= j0:
            return
        XX, YY = np.meshgrid(gx[i0:i1], gy[j0:j1])
        pts = np.column_stack([XX.ravel(), YY.ravel()])
        dentro = Path(poly).contains_points(pts, radius=crecer * 2)
        muro[j0:j1, i0:i1] |= dentro.reshape(YY.shape)

    def linea(a, b, grosor=0.12):
        ux, uy = b[0] - a[0], b[1] - a[1]; L = math.hypot(ux, uy) or 1
        nx, ny = -uy / L * grosor / 2, ux / L * grosor / 2
        pintar([(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)])

    for q in qs:
        pintar(q["pts"], 0.02)
    for v in vs:
        linea(v["p1"], v["p2"], max(0.12, v["esp"]))
    for a, b in CIERRES.get(pid, []):
        linea(a, b, 0.14)
    for x0, x1, y0, y1 in MUROS_VISOR.get(pid, []):
        pintar([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 0.02)

    # cierre: engordar los muros K celdas tapa puertas y uniones mal cerradas (huecos <= 2*K*RES)
    def dilatar(m, k):
        out = m.copy()
        for it in range(k):
            o = out.copy()
            o[1:, :] |= out[:-1, :]; o[:-1, :] |= out[1:, :]
            o[:, 1:] |= out[:, :-1]; o[:, :-1] |= out[:, 1:]
            if it % 2:
                o[1:, 1:] |= out[:-1, :-1]; o[:-1, :-1] |= out[1:, 1:]
                o[1:, :-1] |= out[:-1, 1:]; o[:-1, 1:] |= out[1:, :-1]
            out = o
        return out

    K = int(CIERRE_M / RES)
    cerrado = dilatar(muro, K)

    # nombres de los recintos
    p = PISOS[pid]; rx0, rx1, ry0, ry1 = p["reg"]
    etiquetas = []
    for capa, x, y, s in d["txt"]:
        if not (rx0 <= x <= rx1 and ry0 <= y <= ry1) or not capa.startswith("Texto"):
            continue
        X, Y = a_p1(p, x, y)
        if not en(CLIP, X, Y):
            continue
        for pat, nombre, tipo in NOMBRES:
            if re.search(pat, s, re.I):
                m = re.search(r"([\d]+[.,]?\d*)\s*M2", s, re.I)
                area = float(m.group(1).replace(",", ".")) if m else None
                if nombre == "Cuarto de residuos sólidos":
                    m = re.search(r"\|\s*([\d.]+)\s*$", s); area = float(m.group(1)) if m else area
                etiquetas.append(dict(nombre=nombre, tipo=tipo, x=X, y=Y, area=area))
                break
    for nombre, tipo, x, y, area in MANUALES.get(pid, []):
        etiquetas.append(dict(nombre=nombre, tipo=tipo, x=x, y=y, area=area))

    # componentes conexas (BFS) sobre el plano cerrado
    lab = np.full((H, W), -1, np.int32)
    libre = ~cerrado
    comps = []
    for j in range(H):
        for i in range(W):
            if not libre[j, i] or lab[j, i] >= 0:
                continue
            cid = len(comps); q = deque([(j, i)]); lab[j, i] = cid; n = 0; borde = False
            while q:
                y, x = q.popleft(); n += 1
                if x == 0 or y == 0 or x == W - 1 or y == H - 1:
                    borde = True
                for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if 0 <= yy < H and 0 <= xx < W and libre[yy, xx] and lab[yy, xx] < 0:
                        lab[yy, xx] = cid; q.append((yy, xx))
            comps.append(dict(n=n, borde=borde))

    def celda(x, y):
        i = int((x - X0) / RES); j = int((y - Y0) / RES)
        return (j, i) if 0 <= i < W and 0 <= j < H else None

    R = int(2.5 / RES)
    for e in etiquetas:
        c = celda(e["x"], e["y"])
        if c is None or lab[c] >= 0 or muro[c]:
            continue
        # ¿el recinto del nombre ya tiene un núcleo? (entonces el crecimiento lo alcanza solo)
        visto = {c}; q = deque([c]); toca = False
        while q and not toca:
            y, x = q.popleft()
            for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if (yy, xx) in visto or not (0 <= yy < H and 0 <= xx < W) or muro[yy, xx]:
                    continue
                if abs(yy - c[0]) > R or abs(xx - c[1]) > R:
                    continue
                if lab[yy, xx] >= 0:
                    toca = True; break
                visto.add((yy, xx)); q.append((yy, xx))
        if toca:
            continue
        cid = len(comps)
        for y, x in visto:
            lab[y, x] = cid
        comps.append(dict(n=len(visto), borde=False, sembrado=True))

    # devolver a cada recinto lo que el cierre le quitó (crecen compitiendo, sin pasar muros reales)
    for it in range(400):
        antes = int((lab >= 0).sum())
        for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            cand = np.full_like(lab, -1)
            ys = slice(max(dj, 0), H + min(dj, 0)); yd = slice(max(-dj, 0), H + min(-dj, 0))
            xs = slice(max(di, 0), W + min(di, 0)); xd = slice(max(-di, 0), W + min(-di, 0))
            cand[ys, xs] = lab[yd, xd]
            m = (lab < 0) & ~muro & (cand >= 0)
            lab[m] = cand[m]
        if int((lab >= 0).sum()) == antes:
            break
    cuenta = np.bincount(lab[lab >= 0].ravel(), minlength=len(comps))
    for cid, comp in enumerate(comps):
        comp["n"] = int(cuenta[cid])

    por_comp = collections.defaultdict(list)
    for e in etiquetas:
        c = celda(e["x"], e["y"])
        cid = lab[c] if c else -1
        if cid < 0:  # el texto cayó sobre un muro: buscar la celda libre más cercana
            for r in range(1, 12):
                hallado = False
                for dj in range(-r, r + 1):
                    for di in range(-r, r + 1):
                        jj, ii = c[0] + dj, c[1] + di
                        if 0 <= jj < H and 0 <= ii < W and lab[jj, ii] >= 0:
                            cid = lab[jj, ii]; hallado = True; break
                    if hallado:
                        break
                if hallado:
                    break
        e["comp"] = int(cid)
        if cid >= 0:
            por_comp[int(cid)].append(e)
        info = comps[cid] if cid >= 0 else {}
        print(f"   · {e['nombre'][:28]:28} ({e['x']:.2f},{e['y']:.2f}) comp={cid} borde={info.get('borde')} m2={info.get('n', 0) * RES * RES:.1f}")

    # fragmentos sin nombre (el cierre partió pasillos angostos): se unen al vecino con más borde común
    def pares():
        cnt = collections.Counter()
        for a, b in ((lab[:, :-1], lab[:, 1:]), (lab[:-1, :], lab[1:, :])):
            m = (a >= 0) & (b >= 0) & (a != b)
            for u, v in zip(a[m].ravel(), b[m].ravel()):
                cnt[(int(min(u, v)), int(max(u, v)))] += 1
        return cnt
    cambio = True
    while cambio:
        cambio = False
        cnt = pares()
        cuenta = np.bincount(lab[lab >= 0].ravel(), minlength=len(comps))
        for u in range(len(comps)):
            if u in por_comp or comps[u]["borde"] or cuenta[u] == 0 or cuenta[u] * RES * RES >= 4.0:
                continue
            vec = [(n, b if a == u else a) for (a, b), n in cnt.items() if u in (a, b)]
            vec = [(n, v) for n, v in vec if not comps[v]["borde"]]
            if not vec:
                continue
            n, v = max(vec)
            lab[lab == u] = v; cambio = True
            break
    cuenta = np.bincount(lab[lab >= 0].ravel(), minlength=len(comps))
    for cid, comp in enumerate(comps):
        comp["n"] = int(cuenta[cid])

    resultado = []
    for cid, comp in enumerate(comps):
        area = comp["n"] * RES * RES
        if comp["borde"] or area < 0.8:
            continue
        mask = (lab == cid).astype(float)
        gen = contourpy.contour_generator(x=gx, y=gy, z=mask)
        lines = gen.lines(0.5)
        if not lines:
            continue
        anillo = max(lines, key=len)
        poly = rdp([(float(x), float(y)) for x, y in anillo], 0.05)
        ets = por_comp.get(cid, [])
        if not ets:
            nombre, tipo, area_plano, lp = ("Circulación", "circulacion", None, centroide(poly))
            if area < 1.5:
                continue
            resultado.append(dict(nombre=nombre, tipo=tipo, area_plano=None, area_calc=round(area, 2), poly=poly, etiqueta=lp))
        elif len(ets) == 1:
            e = ets[0]
            resultado.append(dict(nombre=e["nombre"], tipo=e["tipo"], area_plano=e["area"], area_calc=round(area, 2), poly=poly, etiqueta=(e["x"], e["y"])))
        else:  # varios nombres en un mismo espacio: repartir por cercanía
            jj, ii = np.nonzero(lab == cid)
            px, py = gx[ii], gy[jj]
            dist = np.stack([np.hypot(px - e["x"], py - e["y"]) for e in ets])
            dueno = dist.argmin(0)
            for k, e in enumerate(ets):
                m2 = np.zeros((H, W)); m2[jj[dueno == k], ii[dueno == k]] = 1
                g2 = contourpy.contour_generator(x=gx, y=gy, z=m2).lines(0.5)
                if not g2:
                    continue
                poly = rdp([(float(x), float(y)) for x, y in max(g2, key=len)], 0.05)
                resultado.append(dict(nombre=e["nombre"], tipo=e["tipo"], area_plano=e["area"], area_calc=round((dueno == k).sum() * RES * RES, 2), poly=poly, etiqueta=(e["x"], e["y"])))
    return resultado, etiquetas


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    a, b = np.array(pts[0]), np.array(pts[-1])
    ab = b - a; L = np.hypot(*ab)
    P = np.array(pts)
    if L == 0:
        dists = np.hypot(*(P - a).T)
    else:
        dists = np.abs(ab[0] * (P[:, 1] - a[1]) - ab[1] * (P[:, 0] - a[0])) / L
    k = int(dists.argmax())
    if dists[k] > eps:
        return rdp(pts[:k + 1], eps)[:-1] + rdp(pts[k:], eps)
    return [pts[0], pts[-1]]


def centroide(poly):
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def escaleras(pid):
    p = PISOS[pid]; x0, x1, y0, y1 = p["reg"]; out = []
    for a, b, c, e in d["segs"].get("Escalera", []):
        if x0 <= a <= x1 and y0 <= b <= y1:
            A = a_p1(p, a, b); C = a_p1(p, c, e)
            if en(CLIP, *A) and en(CLIP, *C) and not (pid != "p1" and A[0] < 389):
                out.append([round(A[0], 3), round(A[1], 3), round(C[0], 3), round(C[1], 3)])
    return out


def lavamanos(pid):
    p = PISOS[pid]; x0, x1, y0, y1 = p["reg"]; out = []
    for capa, x, y, s in d["txt"]:
        if x0 <= x <= x1 and y0 <= y <= y1 and re.search(r"LAVAMANOS", s, re.I):
            X, Y = a_p1(p, x, y)
            if en(CLIP, X, Y):
                out.append([round(X, 3), round(Y, 3)])
    return out


resultado = {"pisos": []}
for pid, p in PISOS.items():
    segs = segmentos(pid)
    ls = lineas(segs)
    qs = tramos(ls)
    vs = vanos(qs, arcos(pid))
    # El visor ya dibuja recibo, producción 1 (doble altura, llega al piso 2) y la «L» (solo piso 1):
    # se omiten esos muros y vanos del DWG
    zonas = ZONA_PROD if pid == "p1" else ZONA_PROD[:2] if pid == "p2" else []
    qs_vis = [q for q in qs if not en_prod(q["pts"], 0.08, zonas)]
    vs_vis = [v for v in vs if not en_prod([v["p1"], v["p2"]], 0.08, zonas)]
    # Vanos: los de ejes de columnas (pista gruesa) no son huecos reales; correcciones vistas en el plano
    def ajustar(v):
        mx, my = (v["p1"][0] + v["p2"][0]) / 2, (v["p1"][1] + v["p2"][1]) / 2
        if v["esp"] > 0.25:
            return None
        if pid == "p1" and 420.5 < mx < 422.5 and my < -20.3:   # paso entre bloque este y planta eléctrica
            return None
        if pid == "p-1" and not (394.0 < mx < 405.8):           # fuera del sótano (escaleras)
            return None
        if pid == "p-1" and abs(my + 7.75) < 0.4 and (abs(mx - 394.16) < 0.1 or abs(mx - 405.62) < 0.1):
            v["tipo"] = "puerta"                                 # llegada de las escaleras exteriores
        if pid == "p1" and abs(mx - 417.745) < 0.05:
            v["tipo"] = "puerta"                                 # puerta corrediza de baños 2
        if v["ancho"] < 0.75:
            v["tipo"] = "ventana"
        return v
    vs_vis = [w for w in (ajustar(v) for v in vs_vis) if w]
    if pid == "p2":  # columna del alero norte: no es muro del piso 2
        qs_vis = [q for q in qs_vis if sum(pt[1] for pt in q["pts"]) / 4 < -9.5]
        vs_vis = [v for v in vs_vis if (v["p1"][1] + v["p2"][1]) / 2 < -9.5]
    sl, ets = salas(pid, qs_vis, vs_vis)
    # dos «Batería de baños 1» en el DWG: numerar de norte a sur
    banos = sorted([s for s in sl if s["nombre"] == "Batería de baños"], key=lambda s: -s["etiqueta"][1])
    for k, s in enumerate(banos):
        s["nombre"] = f"Batería de baños {k + 1}"
    alto = p["alto"]
    piso = dict(id=pid, nombre=p["nombre"], nivel=p["nivel"], y0=p["y0"], alto=alto,
                muros=[[round(c, 3) for pt in q["pts"] for c in pt] for q in qs_vis],
                vanos=[dict(p1=[round(c, 3) for c in v["p1"]], p2=[round(c, 3) for c in v["p2"]], ancho=v["ancho"], esp=round(v["esp"], 3), tipo=v["tipo"]) for v in vs_vis],
                salas=[dict(nombre=s["nombre"], tipo=s["tipo"], area_plano=s["area_plano"], area_calc=s["area_calc"],
                            poly=[[round(x, 3), round(y, 3)] for x, y in s["poly"]], etiqueta=[round(s["etiqueta"][0], 3), round(s["etiqueta"][1], 3)]) for s in sl],
                escaleras=escaleras(pid), lavamanos=lavamanos(pid))
    resultado["pisos"].append(piso)
    print(f"== {p['nombre']}: {len(segs)} segmentos, {len(ls)} líneas, {len(qs)} tramos ({len(qs_vis)} sin la zona del visor), "
          f"{len(vs)} vanos ({sum(v['tipo']=='puerta' for v in vs)} puertas), {len(sl)} salas, {len(piso['escaleras'])} trazos de escalera")
    for s in sorted(sl, key=lambda s: s["nombre"]):
        ap = s["area_plano"]
        print(f"   {s['nombre'][:30]:30} plano={ap if ap is not None else '-':>6}  calculada={s['area_calc']:7.2f}")

json.dump(resultado, open(salida, "w", encoding="utf-8"), ensure_ascii=False)
print("ok", salida)

if png:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    COLORES = {"produccion": "#cfe3f3", "frio": "#cfeff3", "lavado": "#d4f0dc", "servicios": "#efe3cf", "administrativo": "#e6dcf3", "tecnico": "#e9e2d8", "laboratorio": "#f3dce2", "circulacion": "#eeeeee"}
    fig, axs = plt.subplots(3, 1, figsize=(20, 24), dpi=80)
    for ax, piso in zip(axs, resultado["pisos"]):
        for s in piso["salas"]:
            xs = [p[0] for p in s["poly"]]; ys = [p[1] for p in s["poly"]]
            ax.fill(xs, ys, color=COLORES.get(s["tipo"], "#eee"), ec="#888", lw=0.5)
            ax.text(*s["etiqueta"], f"{s['nombre']}\n{s['area_calc']:.1f}" + (f" ({s['area_plano']})" if s["area_plano"] else ""), fontsize=7, ha="center")
        for m in piso["muros"]:
            ax.fill(m[0::2], m[1::2], color="k")
        for v in piso["vanos"]:
            ax.plot([v["p1"][0], v["p2"][0]], [v["p1"][1], v["p2"][1]], color="tab:red" if v["tipo"] == "puerta" else "tab:blue", lw=2)
        for e in piso["escaleras"]:
            ax.plot([e[0], e[2]], [e[1], e[3]], color="tab:green", lw=0.5)
        ax.set_xlim(378, 431); ax.set_ylim(-22.5, -4); ax.set_aspect("equal"); ax.grid(True, lw=0.3); ax.set_title(piso["nombre"])
    fig.savefig(png, bbox_inches="tight")
