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

# Alta calidad (1080p): -tune animation conserva bordes y colores planos; ipratio/pbratio bajos reparten los bits
# también a los cuadros intermedios (si no, los detalles finos se lavan cuando la cámara se mueve)
X264="ipratio=1.1:pbratio=1.05:aq-mode=3:deblock=-1,-1"
hq() { # $1 carpeta, $2 salida
  ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$1/f_%05d.jpg" -vf "$VF" -c:v libx264 -preset slower -tune animation -crf 16 -g 60 -x264-params "$X264" -maxrate 20000k -bufsize 40000k $COLOR "$2"
}
# Liviana (720p) para WhatsApp y para el artifact de Claude (cada archivo debe quedar por debajo de 20 MB)
liviano() { # $1 carpeta, $2 tasa máxima, $3 salida
  ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$1/f_%05d.jpg" -vf "scale=1280:720:flags=lanczos,$VF" -c:v libx264 -preset slower -tune animation -crf 20 -g 60 -x264-params "$X264" -maxrate "$2" -bufsize "$((${2%k} * 2))k" $COLOR "$3"
}

for v in "${LISTA[@]}"; do
  d="$CUADROS/$v"
  until [ -f "$d/fin.json" ]; do sleep 15; done
  case "$v" in
    planta)
      hq "$d" "$SALIDA/planta-marulanda-planta-completa.mp4"
      liviano "$d" 1500k "$SALIDA/planta-marulanda-planta-completa-liviano.mp4" ;;
    proceso)
      hq "$d" "$SALIDA/planta-marulanda-recorrido.mp4"
      liviano "$d" 2000k "$SALIDA/planta-marulanda-recorrido-liviano.mp4" ;;
    area-*)
      hq "$d" "$SALIDA/areas/planta-marulanda-${v#area-}.mp4" ;;
  esac
  rm -rf "$d"
  echo "$(date +%H:%M:%S) listo: $v"
done
ls -la "$SALIDA" "$SALIDA/areas"
