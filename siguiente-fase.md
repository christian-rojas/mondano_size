# Siguiente fase: ¿pipeline 3D o iterar el simulador?

**Producto:** cortavientos oversize color block · 6 tallas (XS–XXL) · tabla oficial de 4 medidas.
**Fecha:** 8 de noviembre de 2026 · **Insumos:** `portada-1-otono.jpeg`, `tallas.webp`, `simulador-tallas.html`.

---

## 1. Veredicto

**No arranques el pipeline 3D todavía. Itera el simulador hacia una guía de tallas embebible y, en paralelo, pide el tech pack.** El 3D es la fase 3, no la fase 1.

La razón no es el costo: es que **el 3D no resuelve la pregunta del cliente**. El comprador necesita decidir entre dos tallas adyacentes ("¿M o L?") y entender dónde le cae el ruedo. Para eso pesan tres datos: contorno de pecho, **ancho de hombro** y **largo de talle con su punto de medida**. Hoy falta el hombro, falta la sisa, falta el puño y falta la definición del punto de medida del talle. Un avatar simulado sobre datos incompletos produce una imagen más convincente pero **no más certera**: se vuelve precisión falsa.

Tres hechos del propio producto lo confirman:

1. **La prenda es holgada por diseño** (XS = 118 cm de pecho, ~+30 cm de holgura). En un oversize, la talla perdona: entre tallas hay 6 cm de contorno (~3 cm por lado). El error de elegir una talla arriba o abajo se siente, pero no arruina el uso. El riesgo real es el **largo** (68–78 cm), y el largo se comunica muy bien con foto real + referencia de estatura.
2. **Una sola foto frontal, con brazos doblados, no permite reconstruir silueta ni espalda.** No se conoce la estatura de la modelo ni qué talla lleva. Cualquier "silueta real" derivada de esa foto sería otra ficción, no una medición.
3. **La tabla tiene un hueco y un error.** La leyenda anuncia "5.- Ancho Hombro" pero la fila no existe; el ruedo rompe el grading (+6 cm por talla, +4 cm en XXL: 128 en vez de 130). Publicar un comparador encima de eso amplifica la errata.

**Criterio de decisión:** ¿qué le sirve al cliente final para decidir su talla? Ver la prenda sobre un cuerpo de proporciones conocidas, con la holgura explicada y la posibilidad de **comparar dos tallas lado a lado**. Eso lo entrega la ruta B en semanas; la ruta A lo entrega en meses y solo si antes existe el patrón digitalizado.

---

## 2. Comparativa de rutas

Costos y plazos son **estimaciones de orden de magnitud, no cotizaciones**. Precisión: *alta* ≈ coincide con un fit expert en ≥80% de casos; *media* ≈ 60–80%; *baja* <60% (definición de trabajo, no estándar de industria).

| | **A. Pipeline 3D completo** | **B. Iterar simulador 2D/2.5D** | **C. Híbrida (recomendada como fase 3)** |
|---|---|---|---|
| **Qué necesitas de la marca** | Tech pack con puntos de medida, patrón en DXF/AAMA, prenda física para medir, muestra de tejido para el Fabric Analyzer, confirmación de errata XXL, 6 avatares o tabla antropométrica | Tabla corregida, ancho de hombro, puño y sisa, fotos flat lay frente/espalda, 360, estatura y talla de la modelo, 3–5 fotos on-model calibradas | Todo lo de B + tech pack + tejido + patrón; el 3D se construye **sobre** el dato ya validado en B |
| **Esfuerzo** | Alto: patronista + especialista CLO/Browzwear + technical artist web (retopo, UV, bake) | Bajo-medio: 1 dev front-end + 1 sesión de foto + revisión de patronista | Medio-alto: reutiliza B y añade 3D optimizado |
| **Costo estimado** | Freelance €5.000–11.000 (agencia €15.000–35.000) + software (CLO $50/mes, MD $39/mes, Blender gratis) | €3.000–9.000 (fotos €1.000–3.000 + iteración €1.500–4.000 + integración €800–2.500) | €6.000–15.000, con el 3D acotado a 1–2 tallas "hero" |
| **Tiempo** | 6–10 semanas (más si falta tech pack) | 3–6 semanas | 6–10 semanas |
| **Precisión real de talla** | Media. Alta en caída/drape si el tejido está ensayado; **baja en "¿me queda?"** sin cuerpo del usuario | Media-alta para elegir talla y ver largo; baja para "cómo se siente" | Media-alta en talla; alta en percepción visual |
| **Riesgo principal** | Gastar antes de tener el dato base; 6 GLB que mantener; el 3D no mejora la decisión sin medición del cliente | Que la "silueta real" sea otro dibujo si la foto no está calibrada | Dos sistemas que mantener y divergen si cambia la tabla |

**Sobre proveedores SaaS de recomendación (Sizekick, 3DLOOK):** son una alternativa real, no un atajo. Sizekick combina BodyFinder (forma corporal) y BodyScanner (escaneo por video) y reporta integración vía botón/web app; 3DLOOK ofrece escaneo de 2 fotos con ~80 puntos. Precios públicos escasos: referencias de terceros ubican Sizekick desde ~$115/mes + uso y 3DLOOK en $499–999/mes. **Ninguno arregla la falta de hombro/sisa en tu ficha**: el motor necesita el dato del producto para mapear la talla.

---

## 3. Secuencia recomendada (3 pasos)

### Paso 1 — Quick win (2–3 semanas): "guía de tallas honesta y embebible"
Objetivo: que el cliente elija talla en <20 s y entienda la holgura.
- Completar el modelo de datos (hombro, puño, sisa, punto de medida del talle) y **corregir la errata del ruedo XXL** con confirmación de marca.
- Reemplazar la heurística `talle/estatura` por un **landmark**: hombro ≈ 0,82 × estatura, cadera ≈ 0,53 ×, entrepierna ≈ 0,47 × (ratios antropométricos aproximados, con aviso). Así el simulador dice "el ruedo cae 4 cm bajo tu cadera", no "va bien".
- Comparador **M vs L** lado a lado, con la diferencia en cm y una frase de fit ("+6 cm de pecho, +2 cm de largo").
- Fotos reales: flat lay frontal y espalda + 2 detalles (capucha, puño). Sin 360 todavía.
- Embeber en Shopify (app block o sección Liquid) y medir eventos.
- **Gate para pasar:** 5 usuarios eligen la misma talla que un fit expert (≥4/5); el tiempo hasta la recomendación es <20 s; los usuarios de la guía no devuelven más que el control a 8 semanas.

### Paso 2 — Medio (4–6 semanas): "silueta calibrada + comparador de tallas"
- Reshoot con **estatura y talla de la modelo declaradas**, cámara fija, fondo neutro, frente/lado/espalda, misma distancia focal. Añadir 360 (turntable) y flat lay de cada talla si el presupuesto lo permite.
- Overlay paramétrico alineado a la foto real (no un muñeco nuevo): el esquema actual se sustituye por la silueta de la modelo con la prenda encima.
- Selector de forma corporal (3–5 arquetipos) en vez de precisión fingida; el resultado se etiqueta como referencia visual.
- Diferenciador clave: **"qué cambia entre tallas"** (pecho, largo, ruedo, manga) con un control de dos tallas.

### Paso 3 — Completo (8–14 semanas): "3D/AR, solo con tech pack"
- Digitalizar patrón (DXF/AAMA), grading contra la tabla corregida, simulación de tejido con parámetros medidos (CLO Fabric Analyzer o Browzwear), avatares por talla.
- Exportar **GLB nativo desde CLO** (`File > Export > glTF 2.0`), optimizar (Draco/KTX2, ~4 MB), publicar con `<model-viewer>` y AR (`ar`, `ar-modes="webxr scene-viewer quick-look"`, `ios-src` opcional). En Shopify basta GLB: acepta hasta 500 MB, auto-optimiza >15 MB y **convierte GLB→USDZ** para iOS.
- Try-on generativo (FASHN, 3DLOOK) **solo como contenido/marketing**, nunca como respuesta de talla: los modelos generativos producen un ajuste verosímil aunque la prenda no cierre. Google cerró Doppl el 30-abr-2026 y movió la función a Search/Shopping; no hay API de marca.

---

## 4. Especificación técnica del Paso 1

**Stack:** HTML/CSS/JS sin framework (o Vite + Preact si se prevé crecer), SVG para el esquema, **un JSON como única fuente de verdad**, hosting estático (Cloudflare Pages / Netlify / Vercel), imágenes AVIF/WebP con `<picture>`. Cero dependencias 3D en esta fase.

**Modelo de datos (`size-guide.v1.json`):**
```json
{
  "schema": "mondano.sizeguide/1.0",
  "sku": "MND-CORT-OT26",
  "unit": "cm",
  "fit": "oversize",
  "fitProfiles": { "tight": 12, "regular": 18, "oversize": 30 },
  "measurePoints": { "bodyLength": "HPS", "sleeve": "shoulder-seam", "chest": "1cm below armhole" },
  "sizes": [
    { "id": "XS", "chest": 118, "shoulder": null, "sleeve": 74, "bodyLength": 68, "hem": 100, "cuff": null }
  ],
  "grading": { "chest": 6, "sleeve": 2, "bodyLength": 2, "hem": [6, 6, 6, 6, 4] },
  "flags": [{ "size": "XXL", "field": "hem", "issue": "grading +4 vs +6", "status": "pending-brand-confirmation" }],
  "assets": { "front": "/img/flat-front.avif", "back": "/img/flat-back.avif", "detailHood": "/img/hood.avif" }
}
```
`null` es deliberado: la UI debe decir "dato no disponible" en vez de inventar hombro o puño.

**Arquitectura de integración:**
- Bundle estático en `size.mondano.com` (o `/pages/guia-de-tallas`).
- **Fase 1:** `<iframe src="https://size.mondano.com/?sku=...&locale=es" loading="lazy" title="Guía de tallas">` dentro de un app block de Shopify o de `sections/size-guide.liquid`. Rápido de instalar y aislado del theme.
- **Contrato `postMessage`:** entrar `{type:"mondano:set", chest, height, fit}`; salir `{type:"mondano:recommendation", size, ease}` y `{type:"mondano:size-selected", size}`. Auto-altura con `ResizeObserver`. Validar `event.origin`.
- **Fase 2:** Web Component `<mondano-size-guide>` con Shadow DOM (mejor SEO/CSP, sin iframe). Mismo JSON.
- **Datos por producto:** metafield `custom.size_guide` (JSON) con fallback al JSON por defecto; nunca duplicar la tabla en el theme.
- **Analítica:** `dataLayer` + GA4: `sizeguide_open`, `measurement_set`, `size_recommended`, `size_compared`, `size_selected`. Sin PII; consentimiento previo.
- **Presupuesto:** <60 KB JS gzip, sin CLS (reservar alto del bloque), tabla estática en `<noscript>`, teclado y `aria-live` en el resultado.

---

## 5. Lo que hay que pedirle a la marca

1. **Tech pack / ficha técnica** con definición de cada punto de medida (HPS, centro espalda, desde cuello) y tolerancias.
2. **Ancho de hombro por talla** (la fila que la leyenda promete y no existe).
3. **Sisa** (profundidad y recorrido), **ancho de manga**, **puño** (contorno relajado y estirado, alto), **ruedo elástico** (relajado vs estirado).
4. **Largo delantero vs espalda**, geometría de capucha (alto, ancho, punto de unión) y alto de cuello.
5. **Tejido:** composición, gramaje, elasticidad, laminado/impermeable, caída; muestra física si se va a simular.
6. **Confirmación de la errata XXL** (ruedo 128 vs 130) y criterio de grading.
7. **Estatura de la modelo y talla que viste** en `portada-1-otono.jpeg`.
8. **Fotos:** flat lay frente/espalda, detalles (cremallera, capucha, puño, ruedo), 360, y on-model frente/lado/espalda con cámara fija.
9. **Intención de fit:** ¿hasta dónde debe caer el ruedo? ¿La holgura de 30 cm es la deseada en todas las tallas?
10. **Datos de retorno por talla** (si existen) y mercado principal (EU/UK/US) para el tallaje.
11. **Permiso de imagen** y política de privacidad si en el futuro se pide foto o medidas.

---

## 6. Riesgos

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Datos incompletos → precisión aparente | Alto | `null` visible, avisos explícitos, no recomendar sin hombro |
| Sobreingeniería 3D sin tech pack | Alto | Gate del Paso 1 antes de comprar software o encargar patrón |
| Try-on generativo "alucina" el ajuste | Medio-alto | Usarlo como visual, nunca como recomendación de talla |
| Errata XXL publicada | Medio | Corregir o marcar antes de embeber; versión del JSON |
| Mantener 6 GLB + USDZ + AR | Medio | Limitar 3D a 1–2 tallas hero; el resto, fotos |
| Privacidad (foto/medidas) | Medio | No pedir foto en fase 1; GDPR y consentimiento si se pide |
| Dependencia de SaaS y cambios de precio | Medio | Abstraer el recomendador detrás del JSON propio |
| Iframe bloqueado por CSP/theme | Bajo-medio | Probar en theme de staging; plan B Web Component |

---

## 7. Fuentes

**Estándar y visores**
- three.js r187 (0.187.0, 30-oct-2026) — https://www.npmjs.com/package/three · https://threejs.org/changelog/?r187
- `<model-viewer>` 4.4.0 — https://www.npmjs.com/package/@google/model-viewer · AR y `ios-src`: https://modelviewer.dev/examples/augmentedreality/
- Shopify: GLB/USDZ hasta 500 MB, auto-optimiza >15 MB, GLB→USDZ — https://www.shopify.com/blog/3d-ecommerce · https://help.shopify.com/en/partners/manage-clients-stores/creating-media/3d-models/creating-3d-models
- CLO exporta glTF 2.0/GLB — https://support.clo3d.com/hc/en-us/articles/360051525034 · límites de materiales: https://www.vntana.com/resource/clo3d

**Software de simulación**
- CLO pricing ($50/mes, $450/año) — https://www.clo3d.com/en/pricing
- Browzwear VStitcher (Freelancer $750/año; VStitcher 2026.2.x) — https://browzwear.com/pricing-plans · https://browzwear.com/blog/vstitcher-2026.2.0-and-stylezone-7.4-whats-new
- Marvelous Designer ($39/mes, $280/año; export USDZ) — https://www.marvelousdesigner.com/pricing

**Recomendación de talla / try-on**
- Sizekick (BodyFinder + BodyScanner, SaaS) — https://www.sizekick.io/blog-posts/sizekick-launches-size-recommendation-ai-based-on-online-shoppers-exact-body-measurements
- 3DLOOK (2 fotos, ~80 puntos) — https://3dlook.ai/pricing · https://3dlook.ai/content-hub/mobile-tailor-is-here
- FASHN API ($0.075/crédito; v1.6 1 crédito) — https://fashn.ai/products/api · https://fashn.ai/blog/pricing-update-for-developer-api
- Doppl cerrado el 30-abr-2026, absorbido por Search/Shopping — https://jetstream.blog/en/google-doppl-shut-down-end-of-april-2026

**Evidencia técnica**
- Simulación 3D vs fit físico: coincidencia alta con tejido ensayado, discrepancias en detalle — https://proc.3dbody.tech/papers/2020/2021zangue.pdf
- El VTO generativo produce un ajuste verosímil con independencia de la talla real — https://fashn.ai/blog/google-research-and-uws-fit-what-it-means-for-virtual-try-on
