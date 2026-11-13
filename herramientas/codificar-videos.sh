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

dos_pasadas() { # $1 carpeta, $2 tasa, $3 salida
  ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$1/f_%05d.jpg" -vf "$VF" -c:v libx264 -preset medium -b:v "$2" -maxrate "$((${2%k} * 2))k" -bufsize "$((${2%k} * 4))k" -pass 1 -passlogfile "$1/x264" -an -f mp4 /dev/null
  ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$1/f_%05d.jpg" -vf "$VF" -c:v libx264 -preset medium -b:v "$2" -maxrate "$((${2%k} * 2))k" -bufsize "$((${2%k} * 4))k" -pass 2 -passlogfile "$1/x264" $COLOR "$3"
}

for v in "${LISTA[@]}"; do
  d="$CUADROS/$v"
  until [ -f "$d/fin.json" ]; do sleep 15; done
  case "$v" in
    planta)
      dos_pasadas "$d" 1400k "$SALIDA/planta-marulanda-planta-completa.mp4" ;;
    proceso)
      ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$d/f_%05d.jpg" -vf "$VF" -c:v libx264 -preset slow -crf 20 $COLOR "$SALIDA/planta-marulanda-recorrido.mp4"
      dos_pasadas "$d" 1300k "$SALIDA/planta-marulanda-recorrido-liviano.mp4" ;;
    area-*)
      ffmpeg -hide_banner -loglevel error -y -framerate 30 -i "$d/f_%05d.jpg" -vf "$VF" -c:v libx264 -preset medium -crf 24 -maxrate 1200k -bufsize 2400k $COLOR "$SALIDA/areas/planta-marulanda-${v#area-}.mp4" ;;
  esac
  rm -rf "$d"
  echo "$(date +%H:%M:%S) listo: $v"
done
ls -la "$SALIDA" "$SALIDA/areas"
