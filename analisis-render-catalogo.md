# Factibilidad del render — contraste con el catálogo real

**Fecha:** 8 de noviembre de 2026
**Fuente:** catálogo público de `mondano.cl` (`/products.json`), 105 productos, 691 variantes, 649 imágenes.
**Datos crudos:** `shopify-productos.json` (productos, tallas, variantes, URLs de imagen).
**Complementa:** `siguiente-fase.md` (decisión de ruta). Este documento responde otra pregunta: *¿aguanta el catálogo real lo que propusimos?*

---

## 1. Qué se pudo recuperar

| Dato | Resultado |
|---|---|
| Productos publicados | **105** |
| Variantes | **691** (83 productos con exactamente 6) |
| Imágenes | **649** (0 con texto alternativo) |
| Tallas | 6 por producto en 83 de 105 casos |
| Guías de tallas en descripciones | **0** (solo 1 descripción roza el tema y es marketing) |
| Acceso Admin API | **Bloqueado**: la app solo tiene `read_orders, read_all_orders`. `read_products` requiere aprobación del comerciante. Se usó el endpoint público del catálogo. |

---

## 2. Radiografía del catálogo

### 2.1 Las tallas no están normalizadas

Cinco notaciones conviven en la misma tienda:

| Conjunto | Productos |
|---|---|
| `XS/S/M/L/XL/XXL` | 49 |
| `XS/S/M/L/XL/2XL` | 40 |
| `XS/S/M/XL/L/2XL` (orden roto) | 6 |
| `S/L/M/XS/XL` y variantes (orden roto) | 5 |
| `S/M/L/XL` | 2 |
| `Talla única` | 3 |

Además la opción se llama **"Talla"** en 52 productos y **"Tamaño"** en 40 (y hay 8 con una segunda opción "Estilo"/"Color"/"Accesorio"). Cualquier sistema de recomendación que lea el catálogo va a fallar si no se normaliza antes: `2XL` y `XXL` son la misma talla, y el orden de los valores no es alfabético ni consistente.

**Coste de arreglarlo: horas, no semanas.** Es el quick win más barato de todo el proyecto y también mejora la conversión sin render.

### 2.2 La fotografía no es homogénea

Clasifiqué la foto principal de los 105 productos por el color del borde (estudio limpio vs escena):

| Fondo de la foto principal | Productos |
|---|---|
| Escena / exterior | **66** |
| Gris de estudio | **38** |
| Blanco puro | **1** |

Por categoría, el reparto es muy desigual:

- **Cortaviento:** 8 gris estudio, 1 blanco, 4 exterior → la mejor base del catálogo.
- **Casaca/Parka (COLOUR BLOCK, ICONIC…):** 5 de 5 en gris estudio.
- **Vestido, Pantalón, Chaqueta, Camisa, Falda, Polera:** 100% escena.
- **Polerón:** 21 escena vs 13 estudio.

Y dentro de una misma ficha las tomas no son un set controlado: la modelo cambia, el encuadre cambia (a la rodilla, a la cintura, primer plano), la pose cambia (manos en el bolsillo, brazos cruzados, de espaldas), y la luz también. Hay 314 imágenes a 1500×1500, 178 a ≥2000 px, y 35 por debajo de 1000 px. Solo **39 de 105** productos tienen al menos una imagen ≥2000 px.

### 2.3 No existe una imagen por talla

En los 105 productos, las imágenes son por producto y color. **Ningún producto tiene fotos distintas por talla.** Por tanto, del catálogo no se puede extraer "cómo se ve la M vs la L": esa información no está en la tienda.

### 2.4 La prenda de la foto ya está publicada

La imagen de `portada-1-otono.jpeg` corresponde a **`cortaviento-purple-spring-trend`** (misma modelo, mismo color block rosa/amarillo/morado; su tercera imagen es la misma pose con las manos en el cuello). Ese producto tiene:

- **6 tallas** XS–XXL y 6 variantes.
- **8 imágenes a 1500×1500** sobre fondo gris de estudio: frontal, espalda a 3/4, detalle de capucha.
- **La misma modelo** que las otras dos variantes de la familia.

Es el mejor activo del catálogo para un render: set controlado, fondo limpio, frente y espalda, y la tabla de medidas que ya tenemos.

### 2.5 Los colorways comparten bloque

Los 13 cortavientos no son necesariamente 13 patrones distintos: **al menos dos bloques se repiten en colorways** (Spring Trend ×3, Urban ×2). Es decir, 5 de los 13 SKU comparten 2 bloques; el resto parece tener bloque propio, por confirmar.

| Familia | Productos | Patrón | Modelo |
|---|---|---|---|
| Spring Trend | Purple, Orange, Pistachio | 1 bloque | La misma |
| Urban | Fuchsia, Purple | 1 bloque | La misma |
| Color Block | Expedition | 1 bloque | Propia |
| Resto (7) | Crop Pinkadelic, Crop Lavender, Ashes, Vintage, Trail Traveler, Pistachio Beach, Susurro del Bosque | Bloque propio (por confirmar) | Varias |

Esto es lo que hace viable la ruta paramétrica: **calibrar una vez sirve para 3 productos**, no para uno. Y el coste de modelado se divide entre los colorways de cada bloque.

---

## 3. Qué cambia en el análisis

El análisis anterior concluía "el 3D no resuelve la talla sin tech pack". El catálogo real **confirma el diagnóstico y añade el orden de magnitud**:

| Suposición previa | Realidad del catálogo |
|---|---|
| "Hay que hacerlo para la prenda" | Son **105 prendas** y 691 variantes |
| "La foto no permite reconstruir la talla" | Cierto, y además **66 de 105** ni siquiera tienen fondo limpio |
| "Falta el ancho de hombro" | Falta en **todas**; no hay guía de tallas en ninguna descripción |
| "El reto es el render" | El reto es **el dato**: 104 de 105 productos no tienen ni una medida publicada |

La conclusión no es "el render es inviable". Es que **el render es la fase equivocada para empezar**, y ahora sabemos exactamente por qué: el cuello de botella no es la tecnología de render, es que no hay medidas que renderizar.

**El dato que desbloquea todo cuesta días, no meses:** medir las 105 prendas físicas con cinta (pecho, hombro, sisa, manga, talle, ruedo) son ~10-15 min por prenda ≈ **20-25 horas de trabajo de patronista**. Eso es dos órdenes de magnitud más barato que modelar 105 prendas en 3D, y hace posible tanto la guía de tallas como el render futuro.

---

## 4. Las tres rutas, con los números del catálogo real

| | **A. 3D por producto** | **B. 2.5D sobre foto calibrada** | **C. Paramétrico por tipo de prenda** |
|---|---|---|---|
| Unidades a producir | 105 prendas × 6 tallas = **630 simulaciones** | 105 productos (1 por talla base) | **2 bloques para 5 SKU** (comprobado); ~10 para los 13 cortavientos (estimado) |
| Requiere | Tech pack de 105 prendas + tejido de cada una | 1 medida real por foto (estatura de la modelo o pecho de la prenda) | Medidas por tipo + tabla de grading |
| Se puede hoy | Solo el cortaviento (tenemos su tabla) | Solo en los 39 productos con foto ≥2000 px y fondo limpio | Sí, si se miden las prendas |
| Esfuerzo | 6-12 meses de especialista | 26-52 días | 3-4 semanas para la primera familia |
| Coste orientativo | €30k-90k a escala catálogo | €6k-15k | €3k-8k |
| Precisión de talla | Media (si el dato existe) | Media | Media-alta |
| Riesgo | Terminar con 630 modelos y sin datos de origen | Sobreinterpretar una foto mal calibrada | Que los colorways no compartan patrón y se multiplique |

**La ruta C es la única que escala a 105 SKU**, pero el catálogo solo demuestra reutilización en dos familias: Spring Trend (3 SKU) y Urban (2 SKU). Para los 13 cortavientos, eso reduce el modelado a ~10 bloques; extenderlo a todo el catálogo exige verificar antes qué SKU comparten patrón. Sin esa verificación, "10 patrones para 105 productos" es una hipótesis, no un hecho.

---

## 5. Veredicto actualizado

1. **El render sigue siendo viable, pero no a escala catálogo y no como primer paso.** La tecnología no es el límite; el límite es que 104 de 105 productos no tienen una sola medida publicada.
2. **Prioridad 1 (días):** normalizar tallas (`2XL→XXL`, ordenar) y unificar "Talla"/"Tamaño". Impacto inmediato, cero riesgo.
3. **Prioridad 2 (semanas):** medir las prendas. Con la tabla en mano, la guía de tallas del catálogo entero es un problema de datos resuelto, no de render.
4. **Prioridad 3 (un producto, no 105):** llevar **`cortaviento-purple-spring-trend`** a render como *hero*. Es el único con tabla propia, tiene 8 imágenes de estudio a 1500×1500 (frontal y espalda), y sus dos colorways hermanos comparten bloque y modelo: una sola calibración sirve para tres productos.
5. **El render por producto para los 105 no se justifica** hasta que exista el dato y hasta comprobar que el 3D mejora la decisión de talla más que una foto calibrada. Hoy no hay evidencia de eso, y la ruta B lo consigue con una fracción del coste.

**El único dato que falta para calibrar el hero** es la estatura de la modelo (o el ancho de pecho de la prenda que viste). Con ese número, las 8 imágenes dejan de ser un dibujo y pasan a tener escala real. Es una pregunta, no un proyecto.

---

## 6. Riesgos técnicos detectados en el catálogo

| Riesgo | Evidencia | Mitigación |
|---|---|---|
| Extracción automática de silueta | 66/105 fotos con fondo de escena; poses y encuadres distintos | Limitar la automatización a las 38 de estudio; el resto, segmentación manual o SAM con revisión |
| Escala desconocida | No se sabe la estatura de ninguna modelo ni la talla que visten | Declararla en el reshoot; sin eso, cualquier superposición es estimación |
| Catálogo heterogéneo | 6 tallas, 5 notaciones, 2 nombres de opción | Normalizar en un JSON único antes de cualquier render |
| Datos por producto | 0 guías de tallas en descripciones | Medir la prenda física; no hay atajo |
| Imágenes pobres | 35 imágenes <1000 px; 649 sin alt | Reshoot solo del hero; no re-renderizar lo que no se va a vender |
| Admin API sin `read_products` | Scope actual: `read_orders, read_all_orders` | Pedir aprobación del scope si se quiere automatizar el catálogo |

---

## 7. Anexo: cómo se obtuvo

- `GET https://mondano.cl/products.json?limit=250&page=1` → 105 productos con variantes, opciones e imágenes.
- Clasificación de fondo: media de color del 6% del borde de la imagen principal, descargada a 300 px (`thumbs/`).
- Dimensiones: metadatos `width`/`height` que entrega el propio catálogo.
- Búsqueda de guías de tallas: `body_html` de los 105 productos, buscando `<table>`, "pecho", "contorno", "medidas", "cm".
- No se usaron credenciales: el endpoint público solo expone productos publicados, que es exactamente lo que ve el cliente.
