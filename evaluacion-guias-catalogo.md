# Guías de tallas del catálogo — análisis y transcripción

**Fecha:** 8 de noviembre de 2026
**Estado:** 118 guías transcritas a JSON · 96 de 105 productos cubiertos · 55 tablas únicas.

---

## 1. Corrección del análisis anterior

La conclusión previa ("solo 15 de 105 productos tienen guía; ninguno de 2025-2026") era **incorrecta**. Había mirado la **galería** del producto y el **texto** de la descripción. Las guías están publicadas como **imágenes dentro del HTML de la descripción**, que no aparecen como media del producto ni contienen palabras clave.

**Dato corregido:** 97 de 105 productos (92%) tienen guía, incluidos 15 de los 16 publicados en 2026.

---

## 2. Cobertura

| Fuente | Productos |
|---|---|
| Guía en la galería | 15 / 105 |
| Guía en la descripción (imagen) | 96 / 105 |
| **Cualquier guía** | **97 / 105 (92%)** |
| Sin guía | 8 / 105 |

| Categoría | Con guía transcrita |
|---|---|
| Polerón | 33 / 34 |
| Cortaviento | 12 / 13 |
| Parka | 12 / 13 |
| Conjunto | 11 / 11 |
| Vestido | 8 / 8 |
| Casaca | 6 / 6 |
| Casaca/Parka | 5 / 5 |
| Abrigo | 3 / 4 |
| Pantalón | 1 / 4 |
| Chaqueta | 1 / 2 |
| Camisa | 2 / 2 |

Sin guía: Abrigo Camel Leather, Cortaviento Susurro del Bosque, Chaqueta Denim Jacket, Pantalón Straight Jeans, Polera You Are Lucky, Pantalón Snake Baggy Jeans, Pantalón Black Baggy Jeans, Parka Marquam Peak.

---

## 3. Resultado de la transcripción

| Métrica | Valor |
|---|---|
| Guías transcritas | **118** |
| Tablas únicas (misma tabla repetida en colorways) | **55** |
| Productos cubiertos | **96** |
| Formato tabla técnica (pom) | 105 |
| Formato rango corporal | 8 |
| Formato tabla oscura | 5 |
| Con fila de ancho de hombro | **76 / 118** |
| Confianza alta / media / baja | 114 / 3 / 1 |

**55 tablas para 118 imágenes** confirma que los colorways comparten guía: la transcripción no hay que repetirla por color.

---

## 4. Calidad de los datos (hallazgos verificados contra la imagen)

1. **Errores impresos en las propias guías.** En "Casaca - CAPUCHA POLERON" y "Casaca - Impermeable Collor con Forro Thermaflecee", la fila cadera salta de 132 a **148** en XXL (debería ser 138). Está así en el original; se transcribió tal cual y queda marcado.
2. **Guías que no corresponden al producto.** La guía del Conjunto ABSTRACT FLOWERS es de una **falda asimétrica cruzada**; la del Vestido Samba Rosé se titula **"Vestido Brillo"** y la del Conjunto COPACABANA, **"Top Brillo"**.
3. **Tres formatos incompatibles.** Tabla técnica (filas = medidas), rango corporal (88-92) y tabla oscura (tallas en filas). No son comparables sin normalizar.
4. **Etiquetas inconsistentes.** "Contorno pecho" vs "Contorno Busto"; "Contorno cadera" vs "Contorno ruedo"; "Ancho Hombre" (sic) vs "Ancho Hombro"; "Cortorno" (sic).
5. **Dos largos bajo el mismo SKU** en COLOUR BLOCK/ICONIC (talle 65-70 vs 85-90) y CREAM (76-86 vs 96-106).
6. **42 guías sin ancho de hombro**, incluida la del cortaviento (que solo tiene 4 filas).
7. **Una guía incompleta:** Vestido EOLO trae "……" en largo de manga (transcrito como `null`).
8. **Fila 5 inventada en 3 guías** (Spring Trend): la leyenda lista "Ancho Hombre" pero la tabla solo tiene 4 filas. Detectado por auditoría geométrica y corregido.

---

## 5. Qué cambia para el render

**Antes:** 15 productos con ancla de escala (14%).
**Ahora:** **96 productos con tabla estructurada**, y **76 con ancho de hombro**.

| Ruta | Cobertura real | Qué falta |
|---|---|---|
| **2.5D sobre foto calibrada** | **96 productos** | Solo la calibración de la foto (la tabla ya da el ancho real) |
| **3D paramétrico** | 76 con POM + hombro | Sisa, ancho de manga, puño, cuello y tejido |
| Render de los 8 sin guía | 0 | Medir la prenda |

El cuello de botella ya no es el dato de tallas: **está resuelto para el 92% del catálogo**. Lo que queda es (a) normalizar los 3 formatos, (b) completar sisa/puño/cuello para 3D y (c) el tejido.

---

## 6. Veredicto

1. **El catálogo sí tiene datos de talla, y ahora están en JSON.** 55 tablas únicas cubren 96 productos.
2. **El 2.5D es viable a escala catálogo hoy**: la tabla da el ancla de escala y la prenda se puede deformar por talla sin inventar.
3. **El 3D sigue bloqueado, pero menos**: 76 productos tienen hombro; faltan sisa, puño y tejido, que no están en ninguna guía.
4. **La calidad de las guías es el riesgo**: errores impresos, guías de otro producto y tres formatos. Antes de renderizar hay que corregir y normalizar.

---

## 7. Plan

| # | Acción | Coste | Efecto |
|---|---|---|---|
| 1 | Normalizar los 3 formatos a un esquema único (`pecho, manga, talle, ruedo, hombro`) | 4 h | Datos comparables en el 92% del catálogo |
| 2 | Corregir la errata 148 → 138 y las guías prestadas | 2 h | Evita recomendaciones falsas |
| 3 | Completar hombro en las 42 guías que no lo tienen | 1 día | Habilita patrón 3D |
| 4 | Calibrar y renderizar el hero en 2.5D | 2-3 días | Primer render con dato real |
| 5 | Medir las 8 prendas sin guía | 2 h | Cobertura 100% |

---

## 8. Archivos

| Archivo | Contenido |
|---|---|
| `transcripciones-tallas.json` | 118 guías con producto, imagen, formato, leyenda y 6 valores por medida |
| `catalogo-agrupado.json` | Catálogo completo: productos, variantes, imágenes de galería y descripción, guías enlazadas |
| `evaluacion-guias-catalogo.md` | Este documento |
| `siguiente-fase.md` | Decisión de ruta (3D vs 2.5D) |
| `analisis-render-catalogo.md` | Análisis previo con el catálogo real |

### Esquema de una tabla

```json
{
  "index": 47,
  "product": "Cortaviento - ASHES",
  "image": "8090313162975_0.jpg",
  "format": "pom",
  "sizes": ["XS","S","M","L","XL","XXL"],
  "confidence": "alta",
  "measures": [
    { "label": "Contorno pecho", "canonical": "pecho", "values": [118,124,130,136,142,148] },
    { "label": "Largo manga",    "canonical": "manga", "values": [74,76,78,80,82,84] },
    { "label": "Largo talle",    "canonical": "talle", "values": [63,65,67,69,71,73] },
    { "label": "Contorno Cadera","canonical": "ruedo_o_cadera", "values": [100,106,112,118,124,128] }
  ]
}
```
