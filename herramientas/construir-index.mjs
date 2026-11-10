// Genera las páginas que publica Vercel:
//   index.html  <- portada.html           (portada del proyecto)
//   visor.html  <- sala3d-marulanda.html  (visor 3D y plano 2D)
//
//   node herramientas/construir-index.mjs
//
// Correrlo cada vez que se cambie una de las dos fuentes o un archivo de documentos/, antes de hacer commit.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { documento } from './documento.mjs';

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
for (const [fuente, destino] of [['portada.html', 'index.html'], ['sala3d-marulanda.html', 'visor.html']]) {
  fs.writeFileSync(path.join(raiz, destino), documento(fs.readFileSync(path.join(raiz, fuente), 'utf8'), raiz));
  console.log(`${destino} generado desde ${fuente}`);
}
