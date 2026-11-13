# Sala 3D · Planta de lácteos de Marulanda

Visor 3D y plano 2D de la planta de lácteos de Marulanda (Caldas): el edificio completo piso a piso (piso −1, piso 1, piso 2 y cubierta) para recorrerlo sala por sala, y la sala de recibo y producción con sus equipos, el recorrido por el proceso, video y documentación descargable.

**Proyecto de [Industrias Equinox Colombia](https://indequinoxcol.com)** · diseñado y desarrollado por **[Lukbyte · Soluciones digitales](https://lukbyte-my-website.vercel.app/)**.

| Página | Dirección |
| --- | --- |
| Portada del proyecto | https://planta-marulanda-3d.vercel.app |
| Visor 3D y plano 2D (abre en el edificio, piso 1) | https://planta-marulanda-3d.vercel.app/visor |
| Visor caminando por el edificio | https://planta-marulanda-3d.vercel.app/visor#caminar |
| Visor en la sala de producción | https://planta-marulanda-3d.vercel.app/visor#sala |
| Visor con el recorrido de la planta completa | https://planta-marulanda-3d.vercel.app/visor#recorrido-planta |
| Visor con el recorrido del proceso | https://planta-marulanda-3d.vercel.app/visor#recorrido |
| Visor abierto en el plano 2D de la sala | https://planta-marulanda-3d.vercel.app/visor#plano |

> Modelado preliminar. Las medidas de los equipos salen de la lista de dimensiones de la planta (10 de noviembre de 2026); donde la lista no trae el alto se usó el del catálogo o uno estimado. La página no aparece en buscadores (`noindex`): la abre quien tenga el enlace.

---

## Portada

La portada presenta el proyecto a nombre de Industrias Equinox Colombia: logo, imagen del modelo, accesos al visor, al plano y al recorrido, las 8 etapas del proceso, la documentación descargable y los datos de contacto de Equinox. Al final va la firma de Lukbyte, que diseñó y desarrolló el proyecto. El video del recorrido se ve ahí mismo, en una ventana.

Las dos páginas se adaptan a celular, tablet y computador.

## Qué hay en el visor

Arriba a la izquierda se elige qué ver: **Edificio** (toda la infraestructura) o **Sala de producción** (la sala con sus equipos, como antes).

### Edificio, piso a piso

| Parte | Qué hace |
| --- | --- |
| **Pisos** | Exterior (con cubierta), Piso 2, Piso 1 y Piso −1. Al elegir un piso se ocultan los de arriba y los muros se cortan a 1,2 m para ver la planta. |
| **Separar pisos** | Abre el edificio como una maqueta: cada piso a su altura con la cubierta encima, para ver todo a la vez. |
| **Salas** | 33 recintos leídos del DWG con su nombre, área del plano y área medida entre muros. Al tocar una sala (en el 3D, en el plano o en la lista) se ve su ficha: piso, nivel, alto libre, equipos que tiene y nota. Las que aún no tienen máquinas aparecen como «por definir». |
| **Zonas de lavado** | Cuarto de lavado, tres lavamanos de pedal y el lavado de botas en el paso del vestuario a producción, en el 3D, en el plano y en su propia lista. |
| **Caminar** | Recorrido a pie en primera persona: arrastrar para mirar, flechas o WASD para caminar (Mayús para ir más rápido). Choca con muros y equipos; junto a cada escalera aparece el botón para subir o bajar de piso. Arriba se ve en qué sala y piso se está. Esc para salir. |
| **Plano 2D** | La planta del piso elegido con salas coloreadas por uso, muros, puertas, ventanas, escaleras, lavamanos y áreas. En el piso 1 se ven además los equipos y las líneas de la sala de producción. |
| **Recorridos guiados** | El botón «▶ Recorrido» abre el menú: **planta completa** (exterior, los tres pisos y cada zona, 1:45), **proceso de producción** (las 8 etapas, 1:18), **zonas de lavado** (0:41), **por piso** (sala por sala, de occidente a oriente) o **una sala** escogida de la lista. La ficha de cada sala también tiene «▶ Recorrer esta sala». Mientras avanza, la ficha del panel muestra la sala en la que va y el plano sigue la cámara en un recuadro. |

### Sala de producción

| Parte | Qué hace |
| --- | --- |
| **Vista 3D** | La sala completa: muros del DWG, 26 equipos y 7 líneas de proceso con el producto en movimiento. Los muros que tapan la vista se bajan solos. |
| **Plano 2D** | Plano de arquitectura dibujado con los mismos datos: muros, puertas, ventanas, columnas, equipos, líneas, tomas y cotas en metros. |
| **3D + 2D** | Las dos vistas lado a lado; al tocar un equipo en el plano, la cámara 3D va hasta él. |
| **Recorrido** | 80 segundos por las 8 etapas: recibo, enfriamiento, descremado y pasteurización, tinas, queso, mantequilla, arequipe y yogurt. La vista que no es la principal aparece en un recuadro de la esquina. |
| **Camión y operario** | El camión de leche está donde lo ubica el plano (bloque del DWG, 6,85 × 2,20 m), junto a la plataforma de recibo, cargado de cantinas. Un operario baja una cantina, la sube al volcador, la vacía al tanque recibidor y regresa con la vacía; el ciclo se repite y coincide con la etapa «Recibo de leche» del recorrido. La carga y el operario son ilustrativos. |
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
- **Edificio completo:** plantas de los pisos −1, 1 y 2 y cortes del mismo DWG, alineadas por los ejes A a F. Niveles N −2,85, N +0,15 y N +3,19; aleros a N +5,93 y cumbrera a N +7,23 (cortes). Las salas se calculan rellenando el espacio entre muros, así que su área «modelo» puede diferir unas décimas de la del plano. Escaleras, lavamanos y lavado de botas tienen la posición del plano y una forma simplificada; el lavado de botas sale del plano de implantación general.
- **Medidas de los equipos:** lista de dimensiones de la planta del 10 de noviembre de 2026. Volcador, compresores y carro de canastas no están en la lista y quedan estimados.
- **Flujo del proceso:** revisado sobre el plano de distribución de equipos. La tubería de agua helada del chiller al fermentador de yogurt quedó proyectada con los ingenieros en la visita.
- **Tomas eléctricas (220 V) y de agua (1/2"):** posición aproximada leída del plano.

### Supuestos por confirmar

- La tina **AT** es la semiautomática y la **S** la sencilla (por el orden de la lista).
- Compresores 1 y 2 al TQ 5000 y el 3 al TQ 3000.
- Puerta entre la zona de recibo y la plataforma.
- Número de canastas por carro y de carros.
- Uso del espacio sobre la zona de producción 2 en el piso 2: el plano lo marca con aspa y el corte D-D' muestra losa.
- Equipos de las salas que aún no los tienen definidos.
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
  edificio/
    dxf_cache.py            Lee el DXF (convertido del DWG) una sola vez y guarda líneas, textos y bloques en JSON
    construir_edificio.py   Muros, vanos y salas de los tres pisos -> edificio.json (y un PNG de control)
    edificio.json           Datos del edificio que usa el visor
    incrustar.py            Copia edificio.json dentro de sala3d-marulanda.html
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

### Volver a generar los datos del edificio

```bash
python herramientas/edificio/dxf_cache.py <ARQ_PLANTA LACTEOS.dxf> <cache.json>
python herramientas/edificio/construir_edificio.py <cache.json> herramientas/edificio/edificio.json <control.png>
python herramientas/edificio/incrustar.py herramientas/edificio/edificio.json sala3d-marulanda.html
```

Necesita Python con ezdxf, numpy, matplotlib y contourpy. El DXF sale del DWG con LibreDWG (`dwg2dxf`).

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

Modelado preliminar, 10 de noviembre de 2026; edificio completo, 13 de noviembre de 2026.
