# Platform Specs — Imágenes de Catálogo E-commerce

## Google Shopping

| Spec | Requerimiento |
|------|--------------|
| **Fondo** | Blanco puro (#FFFFFF) o transparente. Sin colores, sin patrones, sin degradados. |
| **Dimensiones mínimas** | 100 × 100 px |
| **Dimensiones recomendadas** | 800 × 800 px o mayor |
| **Dimensiones óptimas** | 1200 × 1200 px — 1500 × 1500 px |
| **Ratio de aspecto** | Cuadrado (1:1) recomendado |
| **Formato** | JPEG, PNG, WebP, BMP, TIFF |
| **Tamaño de archivo** | Máx. 16 MB |
| **Cobertura del producto** | Debe ocupar 75–90% del frame |
| **Texto en imagen** | Prohibido: precios, descuentos, texto promocional, teléfonos, URLs |
| **Logos y marcas de agua** | Prohibido |
| **Frames y bordes decorativos** | Prohibido |
| **Overlays y badges** | Prohibido (incluye "Oferta", "Nuevo", "-30%") |
| **Imágenes placeholder** | Prohibido |
| **Swatches de color** | No aceptados como imagen principal |
| **Varias vistas en una imagen** | Prohibido como imagen principal |

> **Output del script:** 1200 × 1200 px · Fondo #FFFFFF · Producto al 85% del frame

---

## Mercado Libre

| Spec | Requerimiento |
|------|--------------|
| **Fondo** | Blanco puro (#FFFFFF). No se permiten fondos de color, patrones ni degradados. |
| **Dimensiones mínimas** | 500 × 500 px |
| **Dimensiones recomendadas** | 1200 × 1200 px |
| **Dimensiones óptimas** | 2000 × 2000 px |
| **Ratio de aspecto** | Cuadrado (1:1) |
| **Formato** | JPEG, PNG |
| **Tamaño de archivo** | Máx. 5 MB |
| **Cobertura del producto** | Debe ocupar al menos el 70% de la imagen |
| **Texto en imagen** | No recomendado en imagen principal |
| **Logos de terceros** | Prohibido si son visibles en la imagen (no aplica a logos del propio producto) |
| **Marcas de agua** | Prohibido |
| **Número de imágenes adicionales** | Hasta 12 imágenes en total por publicación |

> **Output del script:** 1200 × 1200 px · Fondo #FFFFFF · Producto al 85% del frame

---

## Pinterest

| Spec | Requerimiento |
|------|--------------|
| **Ratio recomendado** | 2:3 (1000 × 1500 px) |
| **Ratio máximo** | 1:2.1 |
| **Dimensiones mínimas** | 200 px de ancho |
| **Formato** | JPEG, PNG |
| **Tamaño de archivo** | Máx. 32 MB |
| **Fondo** | Libre, pero fondo limpio funciona mejor para productos |

---

## Instagram

| Formato | Dimensiones | Ratio |
|---------|-------------|-------|
| Cuadrado (feed) | 1080 × 1080 px | 1:1 |
| Portrait (feed) | 1080 × 1350 px | 4:5 |
| Stories / Reels | 1080 × 1920 px | 9:16 |

---

## TiendaNube

| Spec | Requerimiento |
|------|--------------|
| **Dimensiones mínimas** | 800 × 800 px |
| **Dimensiones recomendadas** | 1200 × 1200 px |
| **Formato** | JPEG, PNG, WebP |
| **Ratio** | Cuadrado (1:1) recomendado |
| **Fondo** | Libre, blanco recomendado para coherencia visual |

---

## Tabla de conversión rápida

| Dimensión de salida | Sirve para... |
|--------------------|---------------|
| 1200 × 1200 px | Google Shopping ✓ · MercadoLibre ✓ · Instagram ✓ · TiendaNube ✓ |
| 1500 × 1500 px | Google Shopping ✓ · MercadoLibre ✓ · Instagram (recorte leve) |
| 1000 × 1500 px | Pinterest ✓ · Instagram portrait (recorte leve) |
| 1080 × 1920 px | Stories ✓ · TikTok ✓ · Reels ✓ |
| 2000 × 2000 px | MercadoLibre óptimo ✓ · Todos los cuadrados ✓ |

> **Regla práctica:** Una imagen 1200 × 1200 px en fondo blanco cubre el 90% de los casos de catálogo. Generarla primero y luego recortar o agregar padding para las otras plataformas.
