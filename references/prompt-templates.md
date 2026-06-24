# Prompt Templates — Imágenes de Catálogo E-commerce

## Cómo construir un buen prompt de catálogo

Un prompt efectivo tiene 4 bloques:
1. **Tipo de foto** — qué clase de imagen es
2. **Descripción del producto** — qué es, color, material, detalles clave
3. **Contexto visual** — fondo, iluminación, ángulo, estilo
4. **Restricciones** — qué NO debe aparecer (siempre obligatorio)

**Guía de descripción de producto** — más específico = mejor resultado:
```
[tipo de producto] + [material principal] + [color exacto] + [características clave] + [uso o contexto si aplica]
```

| Rubro | Vago ❌ | Preciso ✓ |
|-------|---------|-----------|
| Moda | "remera blanca" | "white 100% cotton crew-neck t-shirt, regular fit, short sleeves" |
| Electrónica | "auriculares" | "matte black over-ear wireless headphones, folding ear cups, USB-C port visible" |
| Hogar | "lámpara" | "modern minimalist desk lamp, matte white metal, flexible gooseneck arm, round base" |
| Cosmética | "crema" | "white frosted glass moisturizing jar, 50ml, gold metal lid, minimalist label" |
| Calzado | "zapatillas" | "white leather low-top sneakers, chunky rubber sole, gold metal eyelets" |

---

## ChatGPT / DALL-E 3

> Entiende instrucciones en lenguaje natural. Maneja bien las restricciones negativas con "do not include". Los prompts en inglés producen mejores resultados que en español.

### Packshot — fondo neutro (más usado para catálogo)

```
Professional product photography of [DESCRIPCIÓN DEL PRODUCTO], centered on a clean [white / light gray] background.
The product fills approximately 80% of the frame.
Soft, even studio lighting with no harsh shadows and no reflections on the background.
[Front view / Three-quarter angle / Top-down view].
Crisp focus on the entire product.
No text, no logos, no watermarks, no brand marks, no price tags, no people, no props.
High resolution, professional e-commerce catalog style.
```

### Editorial — composición más artística

```
Editorial product photograph of [DESCRIPCIÓN DEL PRODUCTO].
Clean [white / light gray / cream / off-white] background.
[Three-quarter angle / Front view / Side profile].
Elegant studio lighting, soft and directional, subtle shadow on one side.
Product fills 75-85% of frame, well centered.
No text, no logos, no watermarks, no models, no props.
High-end catalog aesthetic, fashion or lifestyle editorial style.
```

### Flat-lay — vista cenital

```
Flat lay product photo of [DESCRIPCIÓN DEL PRODUCTO], photographed directly from above.
Clean [white / light gray / marble texture / wood grain] surface.
Product neatly arranged and centered in frame, straight horizontal alignment.
Soft, even overhead lighting, minimal shadows.
No text, no logos, no watermarks, no people.
Minimalist e-commerce flat lay style.
```

### Lifestyle — producto en contexto de uso

```
Lifestyle product photography of [DESCRIPCIÓN DEL PRODUCTO] shown in a natural, realistic usage environment.
[CONTEXTO: "placed on a clean wooden desk" / "on white marble kitchen counter" / "on neatly folded white linen"].
Soft natural or diffused studio lighting. Product is the clear focal point.
No visible logos, no text overlays, no watermarks, no price tags.
Clean, aspirational e-commerce lifestyle style.
```

---

## Gemini / Imagen 3

> Excelente con texturas y materiales. Acepta prompts en español, aunque inglés produce mejores resultados. Agregar "photorealistic, 8k, product photography" al final mejora la calidad notablemente.

### Packshot — fondo neutro

```
Product catalog photography. [PRODUCT DESCRIPTION].
Pure white background, product centered and filling about 80% of the frame.
Soft studio lighting, no harsh shadows, no reflections on background.
[Front / Three-quarter / Top-down] view.
No text, no logos, no watermarks, no brand marks, no price tags, no people, no props.
Professional e-commerce catalog. Photorealistic, 8k resolution, product photography.
```

### Editorial

```
Editorial e-commerce product photograph. [PRODUCT DESCRIPTION].
Clean [white / light gray / cream] background.
Professional studio lighting, soft and even.
[Front / Three-quarter] angle, product fills 80% of frame.
No text, no logos, no watermarks, no models, no props, no price tags.
High-end fashion catalog aesthetic. Photorealistic, 8k resolution.
```

### Flat-lay

```
Flat lay overhead product photography. [PRODUCT DESCRIPTION] photographed from directly above.
[White / light gray / marble / light wood] surface.
Even top-down lighting, no hard shadows. Product centered and neatly arranged.
No text, no logos, no watermarks, no people.
Minimalist e-commerce style. Photorealistic, high resolution.
```

### Lifestyle

```
Lifestyle product photo for e-commerce. [PRODUCT DESCRIPTION] shown in a realistic usage context.
[LIFESTYLE CONTEXT: "on a clean wooden desk" / "on white marble surface" / "in a kitchen setting"].
Natural soft lighting. Product is the main subject, environment is secondary.
No visible brand names, no text overlays, no watermarks, no price tags.
High quality, aspirational lifestyle catalog. Photorealistic, 8k resolution.
```

---

## Midjourney

> El mejor para estética editorial y fotografía de moda. Usa sintaxis propia. `--style raw` es clave para resultados fotorrealistas en lugar de artísticos. Los parámetros van siempre al final.

### Sintaxis base

```
/imagine [descripción del prompt] --ar [ratio] --style raw --q 2 --no [cosas a excluir]
```

> **`--no` siempre incluir:** `text, logo, watermark, brand mark, price tag, label`

### Packshot — fondo neutro

```
/imagine professional product photography, [DESCRIPCIÓN DEL PRODUCTO], 
clean [white/light gray] background, centered composition, 
soft even studio lighting, crisp sharp focus, commercial catalog style 
--ar [RATIO] --style raw --q 2 
--no text, logo, watermark, brand mark, label, people, props, shadows
```

### Editorial

```
/imagine editorial catalog photo, [DESCRIPCIÓN DEL PRODUCTO], 
[white/light gray/cream] background, elegant studio lighting, 
[front/three-quarter] angle, high-end commercial catalog aesthetic 
--ar [RATIO] --style raw --q 2 
--no text, logo, watermark, brand mark, price tag, models, clutter
```

### Flat-lay

```
/imagine flatlay product photography, [DESCRIPCIÓN DEL PRODUCTO] arranged on flat surface, 
top-down overhead shot, [white/gray/marble/wood] surface, 
even soft lighting, clean minimal styling, e-commerce catalog 
--ar [RATIO] --style raw --q 2 
--no text, logo, watermark, brand, shadows, people
```

### Lifestyle

```
/imagine lifestyle product photography, [DESCRIPCIÓN DEL PRODUCTO] in natural usage context, 
[CONTEXTO: "on wooden desk" / "on marble kitchen counter" / "on white linen"], 
soft natural lighting, product as main subject, aspirational e-commerce aesthetic 
--ar [RATIO] --style raw --q 2 
--no text, logo, watermark, brand mark, label, price tag
```

### Ratios por plataforma (`--ar`)

| Plataforma | `--ar` |
|------------|--------|
| Google Shopping | `1:1` |
| Mercado Libre | `1:1` |
| Instagram cuadrado | `1:1` |
| Instagram portrait | `4:5` |
| Pinterest | `2:3` |
| Landing page hero | `16:9` |
| Packshot vertical moda | `3:4` |

### Parámetros clave de Midjourney

| Parámetro | Valor | Efecto |
|-----------|-------|--------|
| `--style raw` | Siempre para catálogo | Fotorrealista, menos "AI-look" |
| `--q 2` | Calidad máxima | Más detalle, más créditos |
| `--no` | Lista separada por comas | Excluye elementos del output |
| `--ar` | Ratio de aspecto | Define la proporción de la imagen |

---

## Combinar herramientas — estrategia recomendada

Para cada producto, generar primero en **ChatGPT o Gemini** para validar el prompt y ver si la descripción es suficientemente precisa. Si el resultado es bueno pero se quiere mayor calidad estética o editorial, usar ese mismo prompt adaptado a **Midjourney** con `--style raw`.
