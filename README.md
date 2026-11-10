# Sala 3D · Planta de lácteos de Marulanda

Visor 3D y plano 2D de la sala de recibo y producción de la planta de lácteos de Marulanda (Caldas), con recorrido por el proceso, video y documentación descargable.

**Proyecto de [Industrias Equinox Colombia](https://indequinoxcol.com)** · diseñado y desarrollado por **[Lukbyte · Soluciones digitales](https://lukbyte-my-website.vercel.app/)**.

| Página | Dirección |
| --- | --- |
| Portada del proyecto | https://planta-marulanda-3d.vercel.app |
| Visor 3D y plano 2D | https://planta-marulanda-3d.vercel.app/visor |
| Visor con el recorrido en marcha | https://planta-marulanda-3d.vercel.app/visor#recorrido |
| Visor abierto en el plano 2D | https://planta-marulanda-3d.vercel.app/visor#plano |

> Modelado preliminar. Las medidas de los equipos salen de la lista de dimensiones de la planta (10 de noviembre de 2026); donde la lista no trae el alto se usó el del catálogo o uno estimado. La página no aparece en buscadores (`noindex`): la abre quien tenga el enlace.

---

## Portada

La portada presenta el proyecto a nombre de Industrias Equinox Colombia: logo, imagen del modelo, accesos al visor, al plano y al recorrido, las 8 etapas del proceso, la documentación descargable y los datos de contacto de Equinox. Al final va la firma de Lukbyte, que diseñó y desarrolló el proyecto. El video del recorrido se ve ahí mismo, en una ventana.

Las dos páginas se adaptan a celular, tablet y computador.

## Qué hay en el visor

| Parte | Qué hace |
| --- | --- |
| **Vista 3D** | La sala completa: muros del DWG, 26 equipos y 7 líneas de proceso con el producto en movimiento. Los muros que tapan la vista se bajan solos. |
| **Plano 2D** | Plano de arquitectura dibujado con los mismos datos: muros, puertas, ventanas, columnas, equipos, líneas, tomas y cotas en metros. |
| **3D + 2D** | Las dos vistas lado a lado; al tocar un equipo en el plano, la cámara 3D va hasta él. |
| **Recorrido** | 78 segundos por las 8 etapas: recibo, enfriamiento, descremado y pasteurización, tinas, queso, mantequilla, arequipe y yogurt. La vista que no es la principal aparece en un recuadro de la esquina. |
| **Fichas** | Al tocar un equipo: qué es, capacidad, medidas, de dónde salen, qué recibe y a dónde envía, y lo que falta confirmar. |
| **Color por estado** | Pinta cada equipo según qué tan segura es su medida (lista de la planta, catálogo, referencia web, estimado). |
| **Documentación** | Descarga de planos, medidas, modelo 3D y video, uno por uno o todo en un ZIP. |

### Cómo moverse en el 3D

- **Mouse:** arrastrar para girar · rueda para acercar hacia donde apunta · clic derecho para deslizar sobre el piso · doble clic para centrar un punto.
- **Controles en pantalla** (abajo a la derecha): mover, girar, inclinar y zoom; se pueden mantener presionados. La barra «Controles» se arrastra para llevarlos a otro lugar, el botón − los oculta y el doble clic en la barra los devuelve a la esquina.
- **Teclado** (con el 3D seleccionado): flechas o WASD para mover, Q/E para girar, R/F para inclinar, + / − para el zoom y 0 para volver a la vista general.
- **Vistas rápidas:** General, Planta, Recibo, Producción y Yogurt y arequipe.

---

## Documentación descargable

| Archivo | Formato | Contenido |
| --- | --- | --- |
| `documentos/planos/planta-marulanda-plano-2d-sala.pdf` | PDF, A3 | Plano 2D a escala 1:75 con cotas, líneas de proceso, tomas, leyenda y notas. |
| `documentos/planos/planta-marulanda-planos-arquitectonicos.pdf` | PDF | Versión de lectura del DWG arquitectónico: plantas, cubierta, fachadas y cortes. |
| `documentos/medidas/planta-marulanda-medidas-equipos.xlsx` | Excel | Cada equipo con su medida, fuente, estado y pendiente; otros equipos de la planta y notas de la visita. |
| `documentos/modelo/planta-marulanda-sala.glb` | GLB | Modelo 3D. Abre en Blender, SketchUp (con complemento para GLB) o el Visor 3D de Windows. |
| `documentos/video/planta-marulanda-recorrido.mp4` | MP4, 1080p | Recorrido en alta calidad (78 s, sin audio). |
| `documentos/video/planta-marulanda-recorrido-liviano.mp4` | MP4, 1080p | El mismo recorrido, liviano para WhatsApp. |
| `documentos/planta-marulanda-documentacion.zip` | ZIP | Todo lo anterior con el video liviano y un LEAME. |

---

## De dónde sale cada dato

- **Muros, puertas, ventanas y columnas:** DWG arquitectónico `ARQ_PLANTA LACTEOS.dwg`, planta piso 1, en metros (convertido con LibreDWG y leído con ezdxf).
- **Zona de recibo y plataforma:** el plano de distribución de equipos no trae cotas; su ancho (4,25 m) se leyó a escala.
- **Alturas libres:** corte C-C' (zona de producción 1, unos 5,7 m) y corte D-D' (la «L», unos 2,8 m bajo losa).
- **Medidas de los equipos:** lista de dimensiones de la planta del 10 de noviembre de 2026. Volcador, compresores y carro de canastas no están en la lista y quedan estimados.
- **Flujo del proceso:** revisado sobre el plano de distribución de equipos. La tubería de agua helada del chiller al fermentador de yogurt quedó proyectada con los ingenieros en la visita.
- **Tomas eléctricas (220 V) y de agua (1/2"):** posición aproximada leída del plano.

### Supuestos por confirmar

- La tina **AT** es la semiautomática y la **S** la sencilla (por el orden de la lista).
- Compresores 1 y 2 al TQ 5000 y el 3 al TQ 3000.
- Puerta entre la zona de recibo y la plataforma.
- Número de canastas por carro y de carros.
- Altos de los equipos que la lista no trae.

---

## Estructura del repositorio

```
index.html                  Portada publicada (se genera desde portada.html, no se edita a mano)
visor.html                  Visor publicado (se genera desde sala3d-marulanda.html)
portada.html                Fuente de la portada
sala3d-marulanda.html       Fuente del visor: estilos, datos de equipos y código (también se publica como artifact de Claude)
favicon.svg  robots.txt  vercel.json  .vercelignore
assets/                     Logos de Equinox y Lukbyte, e imágenes del modelo para la portada y las vistas previas
documentos/                 Todo lo que se descarga desde el sitio
herramientas/
  servidor.mjs              Servidor local para probar, exportar el GLB y grabar el video
  documento.mjs             Envuelve el visor en su documento HTML (lo usan el servidor y el generador)
  construir-index.mjs       Genera index.html y visor.html
  plano-pdf.mjs             Arma el plano 2D en PDF (A3, 1:75) con Chrome sin ventana
  codificar-video.sh        Convierte los cuadros grabados en los dos MP4
  LEAME-documentacion.txt   Texto que va dentro del ZIP
```

La página es HTML estático, sin paso de compilación. Three.js 0.160 se carga desde jsDelivr y las fuentes desde Google Fonts.

---

## Trabajar en local

Requiere Node 18 o superior.

```bash
node herramientas/servidor.mjs 5178
```

Abrir http://127.0.0.1:5178 (portada) y http://127.0.0.1:5178/visor (visor). El servidor arma las páginas desde `portada.html` y `sala3d-marulanda.html` en cada recarga.

### Después de cambiar la portada o el visor

```bash
node herramientas/construir-index.mjs
```

Así `index.html` y `visor.html` quedan iguales a lo que se probó. Hacer commit de las fuentes y de las páginas generadas.

### Volver a generar los documentos

Con el servidor local abierto, desde la consola del navegador en el visor:

| Documento | Paso en el navegador | Paso en la terminal |
| --- | --- | --- |
| Modelo 3D (GLB) | `await window.__sala.exportGLB()` | — |
| Imágenes de la portada | `await window.__sala.capturaLimpia('portada.jpg', {p: [...], t: [...]}, 2000, 1125)` | mover de `herramientas/salida/` a `assets/` |
| Plano 2D (PDF) | `await window.__sala.exportarPlanoSVG()` | `node herramientas/plano-pdf.mjs` |
| Video | `window.__sala.grabarVideo()` (unos minutos; deja los cuadros en la carpeta temporal) | `bash herramientas/codificar-video.sh` (necesita ffmpeg) |

El ZIP se arma con los archivos de `documentos/` (planos, medidas, modelo y video liviano) más `herramientas/LEAME-documentacion.txt` renombrado a `LEAME.txt`. Al terminar, correr `construir-index.mjs` para actualizar los pesos que muestra el visor.

---

## Publicar en Vercel

1. En Vercel: **Add New → Project → Import** el repositorio `planta-marulanda-3d`.
2. **Framework Preset:** Other. Sin comando de build ni carpeta de salida.
3. **Deploy.**

Cada push a `main` publica una versión nueva. `vercel.json` agrega `noindex` a todas las respuestas, y `.vercelignore` deja fuera del sitio este README, las herramientas y la fuente del visor.

---

## Créditos

**Industrias Equinox Colombia** presenta el proyecto. Fabrica en Copacabana, Antioquia, equipos en acero inoxidable para la industria láctea: los diseña, los fabrica y los instala.
WhatsApp de ventas +57 310 725 0200 · ventas@indequinoxcol.com · [indequinoxcol.com](https://indequinoxcol.com)

**Lukbyte · Soluciones digitales** diseñó y desarrolló el modelo 3D, el plano 2D, el recorrido, el video y el sitio. Software a medida que crece con tu empresa, desde Medellín.
[lukbyte-my-website.vercel.app](https://lukbyte-my-website.vercel.app/) · WhatsApp +57 315 039 9322

Las marcas aparecen en la portada, el visor, el video (apertura, encabezado, firma y cierre) y el cajetín del plano en PDF.

Modelado preliminar, 10 de noviembre de 2026.
