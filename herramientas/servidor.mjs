// Servidor local para trabajar el visor sin publicarlo.
//
//   node herramientas/servidor.mjs [puerto]
//
// GET /                 -> la portada (portada.html envuelta en su documento, igual que index.html)
// GET /visor            -> el visor (sala3d-marulanda.html, igual que visor.html)
// GET /<archivo>        -> cualquier archivo del repositorio (documentos/, etc.)
// POST /guardar-glb     -> guarda el modelo exportado en documentos/modelo/planta-marulanda-sala.glb
// POST /guardar?nombre= -> guarda un archivo de apoyo en herramientas/salida/ (por ejemplo el plano en SVG)
// POST /cuadro?i=N      -> guarda un cuadro JPEG del video en la carpeta temporal de cuadros
// POST /prueba?t=S      -> guarda un cuadro de prueba
// POST /fin             -> marca el final de la grabación (fin.json)
import http from 'node:http';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { documento } from './documento.mjs';

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const puerto = Number(process.argv[2] || 5178);
const cuadros = process.env.CUADROS_DIR || path.join(os.tmpdir(), 'planta-marulanda-cuadros');
const salida = path.join(raiz, 'herramientas', 'salida');
fs.mkdirSync(cuadros, { recursive: true });
fs.mkdirSync(salida, { recursive: true });

const TIPOS = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.ico': 'image/x-icon', '.pdf': 'application/pdf', '.mp4': 'video/mp4',
  '.glb': 'model/gltf-binary', '.zip': 'application/zip', '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.txt': 'text/plain; charset=utf-8',
};

const leer = (req) => new Promise((ok) => { const p = []; req.on('data', (c) => p.push(c)); req.on('end', () => ok(Buffer.concat(p))); });
const json = (res, obj) => { res.writeHead(200, { 'content-type': 'application/json' }); res.end(JSON.stringify(obj)); };
const seguro = (n) => path.basename(String(n || '')).replace(/[^\w.\-]/g, '_');

http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x');
  if (req.method === 'POST') {
    const buf = await leer(req);
    if (url.pathname === '/guardar-glb') {
      const f = path.join(raiz, 'documentos', 'modelo', 'planta-marulanda-sala.glb');
      fs.writeFileSync(f, buf);
      return json(res, { ok: true, bytes: buf.length, archivo: path.relative(raiz, f) });
    }
    if (url.pathname === '/guardar') {
      const f = path.join(salida, seguro(url.searchParams.get('nombre')));
      fs.writeFileSync(f, buf);
      return json(res, { ok: true, bytes: buf.length, archivo: path.relative(raiz, f) });
    }
    if (url.pathname === '/cuadro') {
      const i = Number(url.searchParams.get('i'));
      fs.writeFileSync(path.join(cuadros, `f_${String(i).padStart(5, '0')}.jpg`), buf);
      if (i % 150 === 0) console.log(`cuadro ${i}`);
      return json(res, { ok: true });
    }
    if (url.pathname === '/prueba') {
      fs.writeFileSync(path.join(cuadros, `prueba_${seguro(url.searchParams.get('t'))}.jpg`), buf);
      return json(res, { ok: true });
    }
    if (url.pathname === '/fin') {
      fs.writeFileSync(path.join(cuadros, 'fin.json'), buf);
      console.log('fin de la grabación');
      return json(res, { ok: true });
    }
    res.writeHead(404); return res.end('no encontrado');
  }
  const paginas = { '/': 'portada.html', '/index.html': 'portada.html', '/visor': 'sala3d-marulanda.html', '/visor.html': 'sala3d-marulanda.html' };
  if (paginas[url.pathname]) {
    res.writeHead(200, { 'content-type': TIPOS['.html'], 'cache-control': 'no-store' });
    return res.end(documento(fs.readFileSync(path.join(raiz, paginas[url.pathname]), 'utf8'), raiz));
  }
  const f = path.join(raiz, decodeURIComponent(url.pathname));
  if (!f.startsWith(raiz) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('no encontrado'); }
  res.writeHead(200, { 'content-type': TIPOS[path.extname(f).toLowerCase()] || 'application/octet-stream', 'cache-control': 'no-store' });
  fs.createReadStream(f).pipe(res);
}).listen(puerto, '127.0.0.1', () => console.log(`Visor en http://127.0.0.1:${puerto} · cuadros en ${cuadros}`));
