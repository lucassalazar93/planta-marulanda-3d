// Envuelve el contenido del visor (sala3d-marulanda.html, sin <html>/<head>/<body>) en un documento completo.
// Lo usan el servidor local y construir-index.mjs, para que lo que se prueba sea lo mismo que se publica.
// También deja en window.TAMANOS el peso de cada archivo de documentos/, que el visor muestra junto a cada descarga.
import fs from 'node:fs';
import path from 'node:path';

export function tamanos(raiz) {
  const out = {};
  const recorrer = (dir) => {
    if (!fs.existsSync(dir)) return;
    for (const n of fs.readdirSync(dir)) {
      const f = path.join(dir, n), st = fs.statSync(f);
      if (st.isDirectory()) recorrer(f);
      else out[path.relative(raiz, f).split(path.sep).join('/')] = st.size;
    }
  };
  recorrer(path.join(raiz, 'documentos'));
  return out;
}

export function documento(contenido, raiz) {
  const tam = raiz ? tamanos(raiz) : {};
  return `<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="Visor 3D y plano 2D de la sala de recibo y producción de la planta de lácteos de Marulanda (Caldas), con recorrido por el proceso, video y documentación descargable.">
<meta property="og:title" content="Sala 3D Marulanda">
<meta property="og:description" content="Recorrido 3D, plano 2D y documentación de la sala de recibo y producción de la planta de lácteos de Marulanda.">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0b6d8e">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
<script>window.TAMANOS = ${JSON.stringify(tam)};</script>
</head>
<body>
${contenido}
</body>
</html>
`;
}
