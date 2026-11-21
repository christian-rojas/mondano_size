# Visor de talla en Shopify: qué hacer y cómo

## Recomendación

**Sitio estático en Vercel + visor embebido en la ficha, justo debajo del selector de tallas. Sin redirección.**

El visor ya está construido como un HTML autónomo (`visor-tallas.html` + `visor-data.json`). Lo más rápido y con mejor conversión es:

1. Desplegarlo en Vercel (ya está en `https://mondanosize.vercel.app`).
2. Poner el bloque **"Encuentra tu talla"** justo debajo del selector de tallas.
3. Al pulsarlo, el visor se despliega **en línea** (iframe) o se abre en un `<dialog>`.
4. Sincronizar la talla elegida con la variante de Shopify.

```
┌────────────────────────────┐        ┌──────────────────────────┐
│  Ficha de producto          │        │  Vercel (estático)        │
│  Talla:  XS S M L XL        │        │  /?sku=cortaviento-...    │
│  [ Encuentra tu talla ] ◀───┼──┐     │  visor + visor-data.json  │
│  ┌────────────────────────┐  │  │     │  quiz → talla            │
│  │ visor en línea (iframe)│  │  │     └──────────────────────────┘
│  └────────────────────────┘  │  │                  ▲
│  Cantidad   [Agregar…]       │  └──┘  postMessage ───┘
└────────────────────────────┘
```

> La colocación no depende del tema: el bloque se **mueve con JS** al nodo siguiente al selector de tallas, así que funciona en Wokiee, Dawn y cualquier otro sin tocar el código del tema.

---

## Por qué no redirigir

| | Redirigir a otra web | Iframe en la ficha |
|---|---|---|
| El cliente sale del producto | **Sí** | No |
| Volver al carrito / variante | Manual | Automático (`postMessage`) |
| Pérdida de conversión | Alta (pierdes la sesión de compra) | Nula |
| Dominio | Otro (menos confianza) | El tuyo |
| Analítica | Se corta | Continua |
| Esfuerzo | Bajo | Bajo (igual) |

La redirección solo tiene sentido para campañas (Instagram/ads) o si el visor fuera un producto independiente. Para la ficha, el iframe da el mismo resultado sin sacar al cliente.

## Por qué no una "app embebida" de Shopify todavía

En Shopify, "app embebida" significa una app que vive **dentro del admin** (App Bridge), no en la tienda. Lo que se instala en la ficha es una **theme app extension** (app block) o una **sección** del tema.

- **Sección Liquid** (lo que dejamos en `visor-tallas.liquid`): 10 minutos, sin app, sin revisión. Ideal ahora.
- **Theme app extension**: empaqueta la misma sección dentro de una app (custom app para una sola tienda, sin revisión pública). Tiene sentido cuando quieras instalarlo en varias tiendas o versionarlo como producto.
- **App pública**: revisión de Shopify, semanas. Solo si vas a vender la herramienta a otras marcas.

---

## 1. Desplegar en Vercel

El proyecto ya trae `vercel.json` y `.vercelignore` para publicar **solo** el visor y su JSON.

```bash
cd /Users/christianrojas/Desktop/mondano_3d
npx vercel login
npx vercel --prod
```

Queda en `https://mondanosize.vercel.app` (ya desplegado). Para el subdominio:

```bash
npx vercel domains add tallas.mondano.cl
```

DNS: `CNAME tallas → cdn.vercel.com`.

**Comprobación:**
- `https://tallas.mondano.cl/` → abre el visor.
- `https://tallas.mondano.cl/?sku=cortaviento-purple-spring-trend` → producto correcto.

## 2. Instalar la sección en el tema

1. Copia `shopify/visor-tallas.liquid` a `sections/visor-tallas.liquid` del tema (o súbelo con Shopify CLI: `shopify theme push --only sections/visor-tallas.liquid`).
2. Editor de temas → **Producto** → *Añadir sección* → **Visor de talla**.
3. En los ajustes de la sección, pon la URL: `https://mondanosize.vercel.app` (o el subdominio cuando exista).
4. Listo: no hay que colocarla a mano, la sección se sitúa sola bajo el selector de tallas.

`shopify theme push` o el editor visual; no hace falta tocar el código del tema.

### Ajustes de la sección

| Ajuste | Valores | Qué hace |
|---|---|---|
| **Colocación** | `Debajo del selector de tallas` (por defecto) · `En el lugar de la sección` | Con JS mueve el bloque al selector de tallas. |
| **Presentación** | `En línea` (por defecto) · `En línea siempre visible` · `Ventana modal` | En línea = se despliega bajo el selector; modal = a pantalla completa. |
| **Alto del visor en línea** | 520 / 620 / 720 px | Alto inicial; después el visor **se ajusta solo** al contenido de cada paso. |
| **Ocultar en estos productos** | lista de handles | Fichas sin guía de tallas (ver §3.1). |

## 3. Sincronización con la variante

La sección ya lo resuelve:

- El visor avisa `{type:"mondano:size", size:"M"}` cuando el cliente pulsa **"Seleccionar M"** en el último paso (y `{type:"mondano:close"}` para cerrar el visor).
- La sección busca la talla en el selector del tema y la marca:
  - **radios** `input[type=radio][name="Talla"|"Tamaño"]` (Wokiee, Dawn 2.0…),
  - o `<select name="id">` (temas con lista desplegable),
  - o `input[name="id"][value="<variant id>"]`.
- El tema actualiza el input oculto del formulario y la URL `?variant=<id>`.
- La sección confirma con un aviso bajo el botón: *"Talla M aplicada a la variante"*.

> El mapa de Liquid usa la opción de talla del producto (la primera en este catálogo: 52 productos usan "Talla" y 40 "Tamaño"), así que sirve también con productos que tengan color + talla.

### 3.1 Ocultar el botón en productos sin tabla

La sección trae el ajuste **"Ocultar en estos productos (handles)"**: una lista separada por comas. Si el handle del producto está ahí, la sección no renderiza nada.

Hoy incluye los **22 productos sin tabla** (pantalones, vestidos, faldas, algunos conjuntos y prendas sin guía). Se edita desde Personalizar → Visor de talla, sin tocar código.

> Si un producto nuevo aún no tiene tabla, añade su handle a la lista hasta que se transcriba la guía.

## 4. Analítica

La sección empuja eventos a `dataLayer`:

| Evento | Cuándo |
|---|---|
| `size_guide_open` | se abre el visor |
| `size_selected` | el cliente elige talla y se sincroniza la variante |

Con GA4 configurado en el tema, se leen como eventos personalizados. Permite medir el piloto: aperturas, tallas elegidas y (cruzado con pedidos) conversión y devoluciones.

## 5. Rendimiento

- En modo **en línea**, el iframe **no se carga** hasta que el cliente pulsa el botón (`src` se asigna al abrir).
- En modo **en línea siempre visible** se carga con `loading="lazy"`: el navegador lo pide solo cuando entra en pantalla.
- `loading="lazy"` y `visor-data.json` con caché de 5 minutos.
- En móvil, el diálogo ocupa `100dvh` (sin barras del navegador).
- Peso total: ~30 KB de HTML + 71 KB de JSON + 0 imágenes.

## 6. Cambios hechos en el tema (Wookiee)

El tema es de terceros (`Mondano SEO Fix v3`, esquema Wookiee). Estos cambios se hicieron
con Shopify CLI sobre el tema; el repo no guarda los archivos del tema, solo queda el
registro de qué se tocó y cómo revertirlo.

### 6.1 Quitar el enlace "Guía de tallas" de las fichas (2026-11-21)

**Archivo:** `snippets/snippet-main-product-sidebar.liquid` (caso `variant_picker`).

Se eliminó el bloque que enlazaba a `/pages/guia-de-tallas` desde cada ficha:

```liquid
{%- assign guia_tallas_handle = 'guia-de-tallas' -%}
{%- assign guia_tallas = pages[guia_tallas_handle] -%}
{%- if guia_tallas != blank -%}
  <p class="product__size-guide body3 mt--small">
    <a class="link link__base-to-accent-color clear-underline" href="{{ guia_tallas.url }}">
      Guía de tallas
    </a>
  </p>
{%- endif -%}
```

**Motivo:** esa guía es una tabla general de la marca y no corresponde a la prenda que
el cliente está viendo; con el visor (que usa la tabla real de cada producto) confunde
más que ayuda. La página **no se borra**: sigue enlazada desde el texto del home y
sigue sirviéndose en `/pages/guia-de-tallas`.

**Revertir:** restaurar el bloque anterior en el snippet y volver a subirlo con
`shopify theme push --live --only snippets/snippet-main-product-sidebar.liquid --nodelete --allow-live`.

### 6.2 Sección "Visor de talla" (2026-11-21)

Sección nueva (`sections/visor-tallas.liquid`, en este repo) añadida a la plantilla de
producto. Ver §2.

---

## Resumen de la decisión

| Pregunta | Respuesta |
|---|---|
| ¿Redirigir a Vercel? | **No.** Embeber el mismo sitio en un iframe. |
| ¿Dónde va el visor? | **Debajo del selector de tallas**, en línea. |
| ¿App de Shopify ahora? | No. Sección Liquid primero; app solo si se distribuye a otras tiendas. |
| ¿Dónde vive el visor? | Vercel (`tallas.mondano.cl`). |
| ¿Cómo se actualiza? | `vercel --prod`; la sección no cambia. |
| ¿Cómo se mide? | Eventos `dataLayer` + variante sincronizada. |

