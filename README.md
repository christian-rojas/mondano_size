# Mondano · Visor de talla

Quiz de talla mobile-first con maniquí neutro, más el análisis de devoluciones que lo justifica.
Todo estático: sin backend, sin imágenes de modelos, sin dependencias.

**Demo local**

```bash
python3 -m http.server 8765
# http://127.0.0.1:8765/visor-tallas.html
```

Con producto: `visor-tallas.html?sku=casaca-capucha-poleron`

---

## Qué hay

### 1. El visor (`visor-tallas.html`)

- **5 pasos**: ¿para quién es? → estatura y peso → tipo de cuerpo → pecho (opcional) → resultado.
- En móvil, una pantalla por paso; en escritorio, maniquí a la izquierda y quiz a la derecha.
- **Maniquí neutro**: no se usa el cuerpo de una modelo; evita lecturas sobre peso o cuerpo ajeno.
- Estima el pecho con `0,55 × estatura + 0,35 × peso − 22,75` más ajustes de persona y tipo de cuerpo.
- Si el cliente sabe su contorno de pecho, se usa ese dato y se ignora la estimación.
- Recomienda la talla de **la tabla real del producto** y la dibuja sobre el maniquí.
- Nada se guarda ni se envía: todo se calcula en el navegador.

### 2. Los datos (`visor-data.json`)

83 de los 96 productos con guía de tallas, normalizados a 4 medidas (pecho, manga, talle, ruedo).
Se regeneran desde las transcripciones:

```bash
python3 build-visor-data.py
```

Fuente: `transcripciones-tallas.json` (118 guías leídas y transcritas) + `catalogo-agrupado.json`.

### 3. Integración con Shopify (`shopify/`)

- `visor-tallas.liquid`: sección validada con Theme Check. Botón "Encuentra tu talla" + diálogo con iframe, sincronización de variante y eventos `dataLayer`.
- `README.md`: decisión (Vercel + iframe, sin redirección), deploy e instalación.

### 4. Informe de devoluciones (local)

El análisis de devoluciones y el informe de una página se mantienen **fuera del repositorio**: contienen facturación, pedidos y datos del negocio, y este repo es público.

- `informe-devoluciones.pdf` / `.html`
- `caso-negocio-devoluciones.md`
- `reversso-pedidos.json`, `reembolsos-2025-2026.json`, `pedidos-resumen.json`

Están en la carpeta local y listados en `.gitignore`.

### 5. Prototipos anteriores

- `simulador-tallas.html`: primer simulador (control deslizante, tabla interactiva).
- `render-hero-M-vs-L.jpg` / `.gif`: render 2.5D calibrado sobre foto real (versión previa, reemplazada por el maniquí).

---

## Archivos

| Archivo | Para qué |
|---|---|
| `visor-tallas.html` | El quiz + maniquí (lo que se despliega) |
| `visor-data.json` | Tablas de los 83 productos |
| `build-visor-data.py` | Regenera el JSON |
| `transcripciones-tallas.json` | 118 guías transcritas (fuente) |
| `catalogo-agrupado.json` | Catálogo con productos e imágenes (fuente) |
| `shopify/visor-tallas.liquid` | Sección de Shopify |
| `shopify/README.md` | Deploy e instalación |
| `vercel.json` / `.vercelignore` | Publican solo el visor y su JSON |
| `siguiente-fase.md` | Decisión de ruta (3D vs 2D) |
| `analisis-render-catalogo.md` | Análisis del catálogo |
| `evaluacion-guias-catalogo.md` | Guías de tallas: cobertura y calidad |
| `shopify-productos.json` | Catálogo crudo (105 productos) |

---

## Desplegar

```bash
npx vercel --prod
npx vercel domains add tallas.mondano.cl
```

`.vercelignore` deja fuera todo excepto `visor-tallas.html`, `visor-data.json` y la configuración.

## Límites

- La estimación es antropométrica aproximada; el dato exacto es el contorno de pecho.
- La holgura de diseño es 30 cm en el cortaviento y 16 cm por defecto (la marca no declara la del resto).
- Solo prendas superiores: pantalones, faldas y vestidos necesitan otra plantilla.
- El render es una proyección 2D calibrada, no una simulación de tejido.
