# Limpiador de fondos para catálogo (app de Streamlit)

Versión sin código del **Modo 3** de la skill `ecommerce-catalog-images`: subís fotos reales de productos en lote, elegís la plataforma de destino y descargás todas las imágenes ya procesadas (fondo eliminado, tamaño y relleno correctos) en un `.zip`.

No usa ningún LLM. Todo el procesamiento es Python puro (`rembg` + `Pillow`), corre en memoria y no guarda ninguna imagen en ningún servidor.

## Probarla en tu máquina

```bash
cd streamlit-app
pip install -r requirements.txt
streamlit run app.py
```

Se abre en `http://localhost:8501`. La primera vez que procesás una imagen, `rembg` descarga el modelo (~176 MB) y lo cachea — las siguientes corridas son más rápidas.

## Publicarla gratis (Streamlit Community Cloud)

1. Pusheá este repo a un repositorio **público** de GitHub (Community Cloud lo requiere para el plan gratuito).
2. Entrá a [share.streamlit.io](https://share.streamlit.io) con tu cuenta de GitHub.
3. **New app** → elegí el repo, la rama, y como **Main file path** poné `streamlit-app/app.py`.
4. Deploy. En unos minutos queda con una URL pública para compartir.

### Límites del plan gratuito a tener en cuenta

- **1 GB de RAM** garantizado por app, compartido entre todos los usuarios que la estén usando al mismo tiempo — no por sesión individual.
- La app **se duerme** si nadie la usa por un tiempo; tarda unos segundos en reactivarse con la siguiente visita.
- Si subís lotes muy grandes (cientos de fotos a la vez) o varias personas la usan en simultáneo, puede quedarse sin memoria — en ese caso conviene procesar en lotes más chicos, o migrar a un plan con más recursos.
- No hay ningún costo por imagen procesada ni por uso del modelo: `rembg` corre local, no llama a ninguna API externa de pago.

## Estructura

```
streamlit-app/
├── app.py              ← la app completa
├── requirements.txt
└── README.md           ← este archivo
```
