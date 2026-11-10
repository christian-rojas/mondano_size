# Visor de talla — quiz por pasos (mobile-first)

**Archivos:**
- `visor-tallas.html` — el quiz + maniquí (sin dependencias; solo las 3 fotos del paso de calce).
- `visor-data.json` — 83 productos con su tabla normalizada.
- `fits/` — ajustado.jpg, regular.jpg, oversize.jpg (misma modelo y prenda, generadas con IA).
- `build-visor-data.py` — regenera el JSON.

---

## 1. Cómo funciona

Seis pasos, uno por pantalla. En móvil ocupa la pantalla completa; en escritorio se ve el maniquí a la izquierda y el quiz a la derecha.

| Paso | Pregunta | Obligatorio |
|---|---|---|
| 1 | ¿Para quién es? (mujer / hombre / unisex) | Sí |
| 2 | Estatura y peso | Sí |
| 3 | Calce deseado (ajustado / regular / oversize) | Sí |
| 4 | Tipo de cuerpo (recta / curva / redondeada) | Sí |
| 5 | Contorno de pecho | **No** |
| 6 | Resultado: talla + maniquí + medidas | — |

- **Progreso** en 6 barras, botón atrás y ✕ para reiniciar.
- **Nada se guarda ni se envía**: todo se calcula en el navegador.
- Deep link: `visor-tallas.html?sku=casaca-capucha-poleron`.
- Navegación con ← → (fuera de los sliders).

## 2. Cómo se calcula la talla

1. **Estimar el pecho** desde estatura, peso y tipo de cuerpo:

```
pecho ≈ 0,55 × estatura + 0,35 × peso − 22,75 + ajuste_persona + ajuste_tipo
```

| ¿Para quién? | Ajuste pecho |
|---|---|
| Mujer | 0 cm |
| Unisex / prefiero no decir | +3 cm |
| Hombre | +6 cm |

| Tipo de cuerpo | Ajuste pecho | Ajuste cadera |
|---|---|---|
| Recta | −2 cm | −2 cm |
| Curva | 0 | +1 cm |
| Redondeada | +3 cm | +4 cm |

El paso "¿Para quién es?" no cambia el precio ni la disponibilidad: solo corrige la estimación antropométrica del pecho.

2. Si el cliente **ingresa su contorno de pecho** en el paso 5, se usa ese valor y se ignora la estimación.
3. Se elige la talla de la tabla cuyo pecho quede más cerca de la **holgura elegida** en el paso 3: ajustado 8 cm, regular 16 cm, oversize 30 cm.
4. El maniquí se dibuja con el pecho estimado y la talla elegida: el ancho y el largo cambian de verdad.

> La estimación es antropométrica aproximada, no una medición. El paso 5 existe justamente para corregirla; el paso 3 ajusta cuánto abrigo sobra según cómo le gusta usar la prenda.

## 3. Embeber

```html
<iframe
  src="https://tudominio.com/visor-tallas.html?sku={{ product.handle }}"
  title="Encuentra tu talla"
  loading="lazy"
  style="width:100%;height:100dvh;border:0;border-radius:16px"
></iframe>
```

Sugerencia: `height:100dvh` en móvil y 780 px en escritorio. El quiz ya trae su propio fondo y layout.

### API

```js
// el visor avisa al cerrar (✕)
{ type: "mondano:close" }

// la página puede abrir una talla concreta
iframe.contentWindow.postMessage({ type: "mondano:set", size: "L" }, "*");
```

## 4. Qué productos entran

`visor-data.json` tiene **83 de los 96** productos con guía. Entran los que tienen pecho, manga, talle y ruedo en la misma tabla. Quedan fuera pantalones, faldas, vestidos y algunos conjuntos (13), porque su tabla mide otras cosas.

## 5. Regenerar

```bash
python3 build-visor-data.py
```

## 6. Límites

| Punto | Detalle |
|---|---|
| Estimación | Fórmula aproximada; el dato exacto es el contorno de pecho del paso 3. |
| Precisión | Proyección 2D calibrada con la tabla; no es simulación de tejido. |
| Holgura | 8 / 16 / 30 cm según el calce elegido (ajustado / regular / oversize). |
| Productos | Solo prendas superiores (83). |
| Privacidad | Estatura, peso y tipo de cuerpo no salen del navegador. |
| `file://` | El `fetch` de `visor-data.json` no funciona sin servidor: cae al producto de ejemplo. |
