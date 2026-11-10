// Genera index.html (lo que publica Vercel) a partir de sala3d-marulanda.html.
//
//   node herramientas/construir-index.mjs
//
// Correrlo cada vez que se cambie sala3d-marulanda.html, antes de hacer commit.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { documento } from './documento.mjs';

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const contenido = fs.readFileSync(path.join(raiz, 'sala3d-marulanda.html'), 'utf8');
fs.writeFileSync(path.join(raiz, 'index.html'), documento(contenido, raiz));
console.log('index.html generado');
