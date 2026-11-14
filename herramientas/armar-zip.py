"""Arma documentos/planta-marulanda-documentacion.zip con los planos, las medidas, el modelo 3D,
el video de la planta completa y el LEAME.

    python herramientas/armar-zip.py

Después correr node herramientas/construir-index.mjs para que el visor muestre los pesos nuevos.
"""
import os, zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(RAIZ, "documentos")
ARCHIVOS = [
    "planos/planta-marulanda-plano-2d-sala.pdf",
    "planos/planta-marulanda-planos-arquitectonicos.pdf",
    "medidas/planta-marulanda-medidas-equipos.xlsx",
    "modelo/planta-marulanda-sala.glb",
    "video/planta-marulanda-planta-completa-liviano.mp4",
]
destino = os.path.join(DOC, "planta-marulanda-documentacion.zip")
tmp = destino + ".tmp"
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
    for a in ARCHIVOS:
        tipo = zipfile.ZIP_STORED if a.endswith((".mp4", ".pdf")) else zipfile.ZIP_DEFLATED
        z.write(os.path.join(DOC, a), f"planta-marulanda-documentacion/{a}", compress_type=tipo)
    z.write(os.path.join(RAIZ, "herramientas", "LEAME-documentacion.txt"), "planta-marulanda-documentacion/LEAME.txt")
os.replace(tmp, destino)
print(f"{destino}: {os.path.getsize(destino) / 1048576:.1f} MB")
