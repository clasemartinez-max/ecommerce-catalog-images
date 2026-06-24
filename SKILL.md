---
name: ecommerce-catalog-images
description: "Genera imágenes de catálogo de e-commerce en tres modos. Modo 1 — crear imagen desde cero: genera prompts optimizados para ChatGPT/DALL-E, Gemini/Imagen y Midjourney a partir de descripciones de producto, para cualquier rubro. Modo 2 — combinar imágenes: une dos imágenes existentes (logo + producto, variantes de color, side-by-side, grilla de SKUs, lifestyle scene) usando Python/Pillow. Modo 3 — mejorar foto real: elimina el fondo de una foto de producto y la adapta a specs de Google Shopping o Mercado Libre con rembg + Pillow. Usar cuando el usuario mencione: prompt para imagen de producto, imagen para catálogo, foto de producto sin fondo, fondo blanco, imagen para Google Shopping, imagen para MercadoLibre, combinar imágenes, unir fotos, packshot, imagen e-commerce, mejorar foto de producto, quitar fondo, variantes de color en una imagen. Las imágenes de output nunca llevan logos, texto, marcas de agua ni tags, incluso si el usuario no lo menciona: es un requisito implícito de toda imagen de catálogo."
---

# E-commerce Catalog Images

Producción de imágenes de catálogo de producto. Tres modos de operación. Sin logos, sin texto, sin marcas de agua en ningún output.

---

## 0. Entorno de ejecución

Esta skill funciona tanto en **Claude.ai** (Projects, con Code Execution / Artifacts habilitado) como en **Claude Code**. Las rutas de archivos cambian según el entorno. Los comandos de los Modos 2 y 3 usan estas tres variables — resolverlas antes de ejecutar cualquier comando:

| Variable | Claude.ai (Projects) | Claude Code |
|----------|----------------------|-------------|
| `[SKILL_DIR]` — carpeta de la skill | `/mnt/skills/user/ecommerce-catalog-images` | la ruta donde esté instalada la skill en el repo (p. ej. `.claude/skills/ecommerce-catalog-images` o `~/.claude/skills/ecommerce-catalog-images`) |
| `[UPLOADS_DIR]` — imágenes de entrada | `/mnt/user-data/uploads/` | la carpeta donde el usuario tenga las imágenes; si no es obvia, preguntar la ruta |
| `[OUTPUTS_DIR]` — carpeta de salida | `/mnt/user-data/outputs/` | la carpeta de salida que indique el usuario, o el directorio de trabajo actual |

En Claude.ai, entregar el archivo final con la herramienta `present_files`. En Claude Code, indicar la ruta del archivo generado al terminar (no hay equivalente a `present_files`).

---

## 1. Detección del modo

Analizar el pedido del usuario:

| Señal | Modo |
|-------|------|
| Describe un producto pero no adjunta imágenes | **Modo 1 — Crear desde cero** |
| Adjunta 2 imágenes, o menciona "combinar / unir / superponer / logo sobre / variantes" | **Modo 2 — Combinar imágenes** |
| Adjunta 1 imagen real y menciona "fondo blanco / Google Shopping / MercadoLibre / mejorar / quitar fondo" | **Modo 3 — Mejorar foto real** |

Si el modo no es claro, preguntar directamente:
> "¿Querés generar prompts para crear una imagen desde cero en ChatGPT/Gemini/Midjourney, combinar dos imágenes existentes, o mejorar una foto real del producto con fondo blanco?"

**Importante sobre los modos:** Modo 1 produce prompts de texto (Claude no puede generar píxeles). Modos 2 y 3 producen archivos de imagen reales (.png) directamente.

---

## 2. Inputs requeridos por modo

Verificar que tenés todo antes de ejecutar. Si falta algo, preguntar.

### Modo 1 — Crear desde cero
- **Descripción del producto**: nombre, tipo, color, material, rasgos clave
- **Categoría / rubro**: para cargar vocabulario específico si es necesario
- **Estilo**: `packshot` · `editorial` · `flat-lay` · `lifestyle`
- **Herramienta destino**: `chatgpt` · `gemini` · `midjourney` · `todas`
- **Plataforma**: `google_shopping` · `mercado_libre` · `instagram` · `pinterest` · otra

### Modo 2 — Combinar imágenes
- **Imagen A**: producto principal
- **Imagen B**: elemento secundario (logo, variante, fondo/escena)
- **Tipo de combinación**: `overlay-logo` · `side-by-side` · `grid` · `lifestyle-scene`
- **Plataforma destino**

### Modo 3 — Mejorar foto real
- **Imagen del producto**: foto real adjunta
- **Plataforma**: `google_shopping` · `mercado_libre` · otra
- **Fondo**: `white` (default) · `gray` · `transparent`

---

## 3. Modo 1 — Crear desde cero

### Proceso

1. Cargar `references/prompt-templates.md`
2. Si el rubro es específico (moda, electrónica, cosmética, calzado, etc.), cargar `references/industry-vocabulary.md` para enriquecer la descripción
3. Generar prompts para las herramientas solicitadas
4. Sugerir nombre de archivo SEO

### Nombre de archivo SEO

Formato: `[categoria]-[producto]-[variante]-[contexto].png`
- Todo en minúsculas
- Guiones, sin tildes ni caracteres especiales
- Sin el nombre de marca (es imagen de catálogo genérica)

Ejemplos correctos:
- `zapatillas-running-blancas-mujer.png`
- `auriculares-inalambricos-negros-packshot.png`
- `crema-hidratante-tarro-vidrio-50ml.png`

### Regla universal para todos los prompts

Siempre incluir estas restricciones, sin excepción:
> No text, no logos, no watermarks, no brand marks, no price tags, no labels, no overlays.

---

## 4. Modo 2 — Combinar imágenes

**Este modo produce el archivo de imagen final. Claude debe ejecutar los pasos, no mostrarlos.**

### Pasos a ejecutar

**Paso 1** — Instalar dependencia (bash_tool):
```bash
pip install pillow --break-system-packages
```

**Paso 2** — Verificar rutas de las imágenes adjuntas (bash_tool):
```bash
ls [UPLOADS_DIR]
```

**Paso 3** — Elegir parámetros según el tipo de combinación:

| Tipo pedido | `--mode` | Parámetros adicionales |
|-------------|----------|------------------------|
| Logo / estampa sobre producto | `overlay-logo` | `--position center --logo-scale 0.25 --opacity 1.0` |
| Dos variantes de color / antes-después | `side-by-side` | `--gap 20` |
| Grilla de SKUs | `grid` | `--cols 2 --gap 20` |
| Producto sobre fondo o escena | `lifestyle-scene` | `--product-scale 0.50 --position center` |

**Paso 4** — Ejecutar el script con valores reales (bash_tool). Reemplazar `[SKILL_DIR]`, `[UPLOADS_DIR]` y `[OUTPUTS_DIR]` según la tabla de la sección 0:
```bash
python3 [SKILL_DIR]/scripts/combine_images.py \
  --image-a [UPLOADS_DIR][NOMBRE_IMAGEN_A] \
  --image-b [UPLOADS_DIR][NOMBRE_IMAGEN_B] \
  --mode [MODO] \
  --platform [google_shopping|mercado_libre|instagram|pinterest|custom] \
  --output [OUTPUTS_DIR][nombre-seo].png
```

**Paso 5** — Entregar el resultado. En Claude.ai, usar `present_files`; en Claude Code, indicar la ruta del archivo generado. No describir el proceso: entregar el archivo.

Si el script falla, informar el error exacto y ofrecer alternativa con prompts para DALL-E 3 o Firefly.

---

## 5. Modo 3 — Mejorar foto real

**Este modo produce el archivo de imagen final. Claude debe ejecutar los pasos, no mostrarlos.**

### Pasos a ejecutar

**Paso 1** — Instalar dependencias (bash_tool):
```bash
pip install rembg pillow --break-system-packages
```

**Paso 2** — Verificar el nombre exacto del archivo subido (bash_tool):
```bash
ls [UPLOADS_DIR]
```

**Paso 3** — Ejecutar el script con valores reales (bash_tool). Reemplazar `[SKILL_DIR]`, `[UPLOADS_DIR]` y `[OUTPUTS_DIR]` según la tabla de la sección 0:
```bash
python3 [SKILL_DIR]/scripts/remove_background.py \
  --input [UPLOADS_DIR][NOMBRE_ARCHIVO] \
  --platform [google_shopping|mercado_libre|instagram|pinterest|custom] \
  --bg-color [white|gray|light-gray|transparent] \
  --output [OUTPUTS_DIR][nombre-seo].png
```

**Paso 4** — Entregar el resultado. En Claude.ai, usar `present_files`; en Claude Code, indicar la ruta del archivo generado. No describir el proceso: entregar el archivo.

### Output por plataforma

| Plataforma | Canvas | Fondo | Fill |
|------------|--------|-------|------|
| `google_shopping` | 1200×1200 px | #FFFFFF | 85% |
| `mercado_libre` | 1200×1200 px | #FFFFFF | 85% |
| `pinterest` | 1000×1500 px | #FFFFFF | 80% |
| `instagram` | 1080×1080 px | #FFFFFF | 85% |

Si el script produce artefactos visibles en los bordes del producto, informarlo al usuario y ofrecer un prompt de refinamiento para Adobe Firefly o DALL-E 3 como alternativa.

---

## 6. Reglas de calidad — todos los modos

Aplican siempre, incluso si el usuario no las menciona:

- Sin logos propios ni de terceros
- Sin texto superpuesto: precios, descuentos, etiquetas, tags, SKU, nombres de marca
- Sin marcas de agua ni overlays promocionales
- Sin marcos ni bordes decorativos
- Fondo limpio, sin objetos que distraigan del producto
- Colores fieles al producto real (no sobre-saturar ni alterar el tono)
- Producto siempre reconocible, nítido, bien encuadrado

---

## 7. Reference files

| Archivo | Cuándo cargarlo |
|---------|----------------|
| `references/prompt-templates.md` | Siempre en Modo 1 |
| `references/industry-vocabulary.md` | Modo 1 cuando la categoría es específica (moda, electrónica, cosmética, calzado, joyería, alimentos, deporte) |
| `references/platform-specs.md` | Modo 2 o 3 cuando se necesitan dimensiones exactas de una plataforma no contemplada en este archivo |
