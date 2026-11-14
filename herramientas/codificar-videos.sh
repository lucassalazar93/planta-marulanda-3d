#!/usr/bin/env bash
# Convierte en MP4 los videos que grabó el visor con window.__sala.grabarVarios(window.__sala.LISTA_VIDEOS).
# Cada video queda en su subcarpeta de cuadros (planta, proceso, area-<id>); el script espera a que cada una
# tenga su fin.json, la codifica y borra los cuadros.
#
#   bash herramientas/codificar-videos.sh [carpeta-de-cuadros] [subcarpeta ...]
#
# Sin subcarpetas, procesa planta, proceso y todas las area-* que encuentre o que vayan apareciendo.
# Necesita ffmpeg con libx264.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
CUADROS="${1:-${TMPDIR:-${TEMP:-/tmp}}/planta-marulanda-cuadros}"; shift || true
SALIDA="$RAIZ/documentos/video"
mkdir -p "$SALIDA/areas"
VF="scale=out_range=tv:out_color_matrix=bt709,format=yuv420p"
COLOR="-pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart"
LISTA=("$@")
[ ${#LISTA[@]} -gt 0 ] || LISTA=(planta proceso area-calderas area-entrega area-vestuario area-laboratorio area-administracion area-banos area-electrica area-sotano area-piso2 area-lavado)

# Alta calidad (1080p): tune animation conserva bordes y colores planos; tope alto para los movimientos de cámara
hq() { # $1 carpeta, $2 crf, $3 salida
  ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$1/f_%05d.jpg" -vf "$VF" -c:v libx264 -preset slow -tune animation -crf "$2" -g 60 -maxrate 6000k -bufsize 12000k $COLOR "$3"
}
# Liviana (720p) para WhatsApp y para el artifact de Claude (cada archivo debe quedar por debajo de 20 MB)
liviano() { # $1 carpeta, $2 salida
  ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$1/f_%05d.jpg" -vf "scale=1280:720:flags=lanczos,$VF" -c:v libx264 -preset slow -tune animation -crf 22 -g 60 -maxrate 2200k -bufsize 4400k $COLOR "$2"
}

for v in "${LISTA[@]}"; do
  d="$CUADROS/$v"
  until [ -f "$d/fin.json" ]; do sleep 15; done
  case "$v" in
    planta)
      hq "$d" 21 "$SALIDA/planta-marulanda-planta-completa.mp4"
      liviano "$d" "$SALIDA/planta-marulanda-planta-completa-liviano.mp4" ;;
    proceso)
      hq "$d" 20 "$SALIDA/planta-marulanda-recorrido.mp4"
      liviano "$d" "$SALIDA/planta-marulanda-recorrido-liviano.mp4" ;;
    area-*)
      hq "$d" 22 "$SALIDA/areas/planta-marulanda-${v#area-}.mp4" ;;
  esac
  rm -rf "$d"
  echo "$(date +%H:%M:%S) listo: $v"
done
ls -la "$SALIDA" "$SALIDA/areas"
