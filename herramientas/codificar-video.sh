#!/usr/bin/env bash
# Convierte los cuadros grabados por el visor (window.__sala.grabarVideo()) en los dos MP4 de documentos/video/.
#
#   bash herramientas/codificar-video.sh [carpeta-de-cuadros]
#
# La carpeta por defecto es la que usa herramientas/servidor.mjs: <temporal del sistema>/planta-marulanda-cuadros.
# Necesita ffmpeg con libx264.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
CUADROS="${1:-${TMPDIR:-${TEMP:-/tmp}}/planta-marulanda-cuadros}"
SALIDA="$RAIZ/documentos/video"
VF="scale=out_range=tv:out_color_matrix=bt709,format=yuv420p"
COLOR="-pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart"
[ -f "$CUADROS/fin.json" ] || { echo "No encuentro $CUADROS/fin.json: la grabación no terminó"; exit 1; }
cd "$CUADROS"
# Alta calidad
ffmpeg -hide_banner -loglevel error -y -framerate 30 -i f_%05d.jpg -vf "$VF" -c:v libx264 -preset slow -crf 20 $COLOR "$SALIDA/planta-marulanda-recorrido.mp4"
# Liviana para WhatsApp (dos pasadas, unos 12 MB)
ffmpeg -hide_banner -loglevel error -y -framerate 30 -i f_%05d.jpg -vf "$VF" -c:v libx264 -preset medium -b:v 1300k -maxrate 2600k -bufsize 5200k -pass 1 -passlogfile "$CUADROS/x264" -an -f mp4 /dev/null
ffmpeg -hide_banner -loglevel error -y -framerate 30 -i f_%05d.jpg -vf "$VF" -c:v libx264 -preset medium -b:v 1300k -maxrate 2600k -bufsize 5200k -pass 2 -passlogfile "$CUADROS/x264" $COLOR "$SALIDA/planta-marulanda-recorrido-liviano.mp4"
ls -la "$SALIDA"
