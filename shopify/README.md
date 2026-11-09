# Visor de talla en Shopify: qué hacer y cómo

## Recomendación

**Sitio estático en Vercel + iframe embebido en la ficha. Sin redirección.**

El visor ya está construido como un HTML autónomo (`visor-tallas.html` + `visor-data.json`). Lo más rápido y con mejor conversión es:

1. Desplegarlo en Vercel (ya está en `https://mondanosize.vercel.app`).
2. Poner un botón **"Encuentra tu talla"** en la ficha de producto.
3. Abrirlo en un `<dialog>` a pantalla completa con un iframe.
4. Sincronizar la talla elegida con la variante de Shopify.

```
┌────────────────────────────┐        ┌──────────────────────────┐
│  Ficha de producto          │        │  Vercel (estático)        │
│  [ Encuentra tu talla ] ────┼───────▶│  /?sku=cortaviento-...    │
│                             │ iframe │  visor + visor-data.json  │
│  variante ◀── postMessage ──┼────────┤  quiz → talla            │
└────────────────────────────┘        └──────────────────────────┘
```

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
4. Colócala justo debajo del selector de talla.

`shopify theme push` o el editor visual; no hace falta tocar el código del tema.

## 3. Sincronización con la variante

La sección ya lo resuelve:

- El visor avisa `{type:"mondano:size", size:"M"}` al llegar al resultado.
- La sección busca el `variant id` en el mapa que genera Liquid y:
  - cambia el `<select name="id">`, o
  - hace clic en el radio `input[name="id"]`.
- Actualiza la URL con `?variant=<id>`.

- El ✕ del visor envía `{type:"mondano:close"}` y cierra el diálogo.

> El mapa usa `variant.option1`, que en este catálogo es siempre la talla (52 productos usan "Talla" y 40 "Tamaño" como primera opción).

## 4. Analítica

La sección empuja eventos a `dataLayer`:

| Evento | Cuándo |
|---|---|
| `size_guide_open` | se abre el visor |
| `size_selected` | el cliente elige talla y se sincroniza la variante |

Con GA4 configurado en el tema, se leen como eventos personalizados. Permite medir el piloto: aperturas, tallas elegidas y (cruzado con pedidos) conversión y devoluciones.

## 5. Rendimiento

- El iframe **no se carga** hasta que el cliente abre el visor (`src` se asigna al abrir).
- `loading="lazy"` y `visor-data.json` con caché de 5 minutos.
- En móvil, el diálogo ocupa `100dvh` (sin barras del navegador).
- Peso total: ~30 KB de HTML + 71 KB de JSON + 0 imágenes.

---

## Resumen de la decisión

| Pregunta | Respuesta |
|---|---|
| ¿Redirigir a Vercel? | **No.** Embeber el mismo sitio en un iframe. |
| ¿App de Shopify ahora? | No. Sección Liquid primero; app solo si se distribuye a otras tiendas. |
| ¿Dónde vive el visor? | Vercel (`tallas.mondano.cl`). |
| ¿Cómo se actualiza? | `vercel --prod`; la sección no cambia. |
| ¿Cómo se mide? | Eventos `dataLayer` + variante sincronizada. |
