// Arma el plano 2D imprimible (A3 horizontal, escala 1:75) y lo convierte a PDF con Chrome sin ventana.
//
//   1. Con el servidor local abierto, en la consola del visor: await window.__sala.exportarPlanoSVG()
//      (deja herramientas/salida/plano-2d.svg)
//   2. node herramientas/plano-pdf.mjs
//
// Variable opcional CHROME con la ruta de chrome.exe o msedge.exe.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const salida = path.join(raiz, 'herramientas', 'salida');
const svg = fs.readFileSync(path.join(salida, 'plano-2d.svg'), 'utf8')
  .replace(/<svg\b/, '<svg class="dibujo" preserveAspectRatio="xMidYMid meet"');
const pdf = path.join(raiz, 'documentos', 'planos', 'planta-marulanda-plano-2d-sala.pdf');

const LINEAS = [
  ['Leche', '#2f7fc4', ''], ['Queso (traslado a mano)', '#d4851a', '6 4'], ['Crema', '#d6b11f', ''], ['Arequipe', '#9a5a2b', ''],
  ['Yogurt', '#c23d7d', ''], ['Refrigeración de tanques', '#18a9bf', ''], ['Agua helada del chiller', '#118a70', ''],
];
const linea = ([n, c, d]) => `<li><svg width="34" height="10"><line x1="1" y1="5" x2="33" y2="5" stroke="${c}" stroke-width="3" ${d ? `stroke-dasharray="${d}"` : ''}/></svg>${n}</li>`;

const html = `<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Barlow+Condensed:wght@500;600;700&display=swap">
<style>
@page { size: 420mm 297mm; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: Barlow, "Segoe UI", sans-serif; color: #15202a; }
.hoja { width: 420mm; height: 297mm; padding: 9mm 10mm; display: grid; grid-template-rows: 222mm 1fr; gap: 4mm; }
.marco { border: 0.5mm solid #15202a; display: grid; place-items: center; overflow: hidden; background: #fff; }
.dibujo { width: 400mm; height: 216mm; display: block; }
.cajetin { border: 0.5mm solid #15202a; display: grid; grid-template-columns: 120mm 1fr 118mm; }
.cajetin > div { padding: 3mm 4mm; border-right: 0.3mm solid #15202a; }
.cajetin > div:last-child { border-right: 0; }
.ceja { font-family: "Barlow Condensed", sans-serif; font-weight: 600; font-size: 8.5pt; letter-spacing: 0.12em; text-transform: uppercase; color: #586773; }
h1 { margin: 1mm 0 0; font-family: "Barlow Condensed", sans-serif; font-weight: 700; font-size: 20pt; line-height: 1; }
.sub { font-size: 9.5pt; color: #33414c; margin-top: 1.5mm; }
.datos { display: grid; grid-template-columns: auto 1fr; gap: 0.6mm 4mm; margin-top: 2.5mm; font-size: 8.5pt; }
.datos dt { color: #586773; } .datos dd { margin: 0; font-weight: 600; }
ul { list-style: none; margin: 1.5mm 0 0; padding: 0; columns: 2; column-gap: 6mm; font-size: 8.5pt; }
li { display: flex; align-items: center; gap: 2mm; margin-bottom: 1mm; break-inside: avoid; }
.sim { display: inline-block; width: 3mm; height: 3mm; }
.notas { font-size: 8pt; color: #33414c; margin: 1.5mm 0 0; padding-left: 4mm; }
.notas li { display: list-item; list-style: disc; margin-bottom: 0.8mm; }
</style></head>
<body><div class="hoja">
  <div class="marco">${svg}</div>
  <div class="cajetin">
    <div>
      <div class="ceja">Planta de lácteos · Marulanda, Caldas</div>
      <h1>Sala de recibo y producción</h1>
      <div class="sub">Plano 2D de equipos y líneas de proceso · modelado preliminar</div>
      <dl class="datos">
        <dt>Escala</dt><dd>1:75 en A3 · cotas interiores en metros</dd>
        <dt>Fecha</dt><dd>10 de noviembre de 2026</dd>
        <dt>Visor</dt><dd>planta-marulanda-3d.vercel.app</dd>
      </dl>
    </div>
    <div>
      <div class="ceja">Líneas de proceso y tomas</div>
      <ul>
        ${LINEAS.map(linea).join('')}
        <li><span class="sim" style="background:#e9b949;border-radius:50%;border:0.2mm solid #8a6a12"></span>Toma eléctrica 220 V</li>
        <li><span class="sim" style="background:#3b8fd1;border:0.2mm solid #1d5585"></span>Toma de agua 1/2"</li>
      </ul>
    </div>
    <div>
      <div class="ceja">Notas</div>
      <ul class="notas" style="columns:1">
        <li>Muros, puertas, ventanas y columnas: DWG arquitectónico, planta piso 1.</li>
        <li>Equipos: lista de dimensiones de la planta (10-nov-2026). Donde la lista no trae el alto se usó el del catálogo o uno estimado.</li>
        <li>Zona de recibo y plataforma: leídas a escala del plano de distribución de equipos.</li>
        <li>Tomas eléctricas y de agua: posición aproximada.</li>
      </ul>
    </div>
  </div>
</div></body></html>`;

const htmlPath = path.join(salida, 'plano-2d.html');
fs.writeFileSync(htmlPath, html);
const chrome = process.env.CHROME || ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'].find((p) => fs.existsSync(p));
if (!chrome) throw new Error('No encontré Chrome ni Edge; define la variable CHROME');
execFileSync(chrome, ['--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=8000', `--print-to-pdf=${pdf}`, pathToFileURL(htmlPath).href], { stdio: 'inherit' });
console.log('PDF:', path.relative(raiz, pdf), fs.statSync(pdf).size, 'bytes');
