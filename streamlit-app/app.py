"""
Limpiador de fondos para catálogo — app de Streamlit.

Sube fotos reales de productos, elige la plataforma de destino (Google Shopping,
Mercado Libre, TiendaNube, Pinterest, Instagram u otra) y descarga todas las
imágenes ya procesadas: fondo eliminado y recompuesto según las specs de esa
plataforma, en un solo .zip.

Todo corre en memoria, sin LLM y sin guardar las imágenes en ningún servidor:
el procesamiento es 100% Python (rembg + Pillow). No se usan claves de API ni
servicios de pago.
"""

import io
import zipfile
from pathlib import Path

import streamlit as st
from PIL import Image
from rembg import new_session, remove

# ────────────────────────────────────────────────────────────────────────────
# Specs por plataforma (mismos valores que scripts/remove_background.py)
# ────────────────────────────────────────────────────────────────────────────

PLATFORM_SPECS = {
    "Google Shopping": {"size": (1200, 1200), "fill": 0.85},
    "Mercado Libre": {"size": (1200, 1200), "fill": 0.85},
    "TiendaNube": {"size": (1200, 1200), "fill": 0.85},
    "Pinterest": {"size": (1000, 1500), "fill": 0.80},
    "Instagram": {"size": (1080, 1080), "fill": 0.85},
    "Otra plataforma / tamaño original": {"size": None, "fill": 0.85},
}

BG_COLORS = {
    "Blanco": (255, 255, 255, 255),
    "Gris claro": (242, 242, 242, 255),
    "Transparente": (0, 0, 0, 0),
}

MAX_PREVIEW_DIM = 600  # para que las miniaturas no pesen al renderizar


# ────────────────────────────────────────────────────────────────────────────
# Modelo de rembg — se carga una sola vez y se reutiliza para todo el lote
# ────────────────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def get_session():
    return new_session("u2net")


# ────────────────────────────────────────────────────────────────────────────
# Lógica de procesamiento (idéntica a remove_background.py, pero en memoria)
# ────────────────────────────────────────────────────────────────────────────

def process_image(raw_bytes: bytes, session, size, fill: float, bg_rgba) -> Image.Image:
    """Quita el fondo de una imagen y la recompone sobre el canvas de la plataforma."""
    result_bytes = remove(raw_bytes, session=session)
    img = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    is_transparent = bg_rgba[3] == 0

    if size:
        canvas_w, canvas_h = size
        max_w, max_h = int(canvas_w * fill), int(canvas_h * fill)
        img.thumbnail((max_w, max_h), Image.LANCZOS)

        canvas = Image.new(
            "RGBA", (canvas_w, canvas_h), (0, 0, 0, 0) if is_transparent else bg_rgba
        )
        offset_x = (canvas_w - img.width) // 2
        offset_y = (canvas_h - img.height) // 2
        canvas.paste(img, (offset_x, offset_y), img)
        return canvas

    if is_transparent:
        return img

    bg = Image.new("RGBA", img.size, bg_rgba)
    bg.paste(img, (0, 0), img)
    return bg


def image_to_png_bytes(img: Image.Image, transparent: bool) -> bytes:
    buf = io.BytesIO()
    img.convert("RGBA" if transparent else "RGB").save(buf, format="PNG")
    return buf.getvalue()


# ────────────────────────────────────────────────────────────────────────────
# UI
# ────────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Limpiador de fondos para catálogo", page_icon="🖼️", layout="wide")

st.title("🖼️ Limpiador de fondos para catálogo")
st.caption(
    "Subí las fotos que sacaste con el celular en tu tienda y descargalas listas "
    "para publicar, con el fondo eliminado y el tamaño correcto para tu plataforma."
)

with st.sidebar:
    st.header("Configuración")

    plataforma = st.selectbox("¿Para qué plataforma son las imágenes?", list(PLATFORM_SPECS.keys()))
    color_fondo = st.selectbox("Color de fondo", list(BG_COLORS.keys()), index=0)

    specs = PLATFORM_SPECS[plataforma]
    if specs["size"]:
        st.caption(
            f"Salida: **{specs['size'][0]}×{specs['size'][1]}px** · "
            f"producto al **{int(specs['fill'] * 100)}%** del frame"
        )
    else:
        st.caption("Se mantiene el tamaño original de cada foto; solo se cambia el fondo.")

    st.divider()
    st.caption(
        "🔒 Las imágenes se procesan en memoria durante esta sesión. "
        "No se guardan en ningún servidor ni se usan para entrenar ningún modelo."
    )

archivos = st.file_uploader(
    "Subí las fotos de tus productos (podés seleccionar varias a la vez)",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
)

if archivos and len(archivos) > 30:
    st.info(
        f"Subiste {len(archivos)} imágenes. Lotes grandes pueden tardar varios minutos "
        "y, en hosting gratuito, consumir bastante memoria — si la app se cuelga, "
        "probá en lotes más chicos."
    )

if not archivos:
    st.info("Subí al menos una foto para empezar.")
else:
    st.write(f"**{len(archivos)} imagen(es) cargada(s).**")

    if st.button("Procesar todas", type="primary"):
        session = get_session()
        size = PLATFORM_SPECS[plataforma]["size"]
        fill = PLATFORM_SPECS[plataforma]["fill"]
        bg_rgba = BG_COLORS[color_fondo]
        transparent = bg_rgba[3] == 0

        resultados = []  # (nombre_archivo, bytes_png)
        progreso = st.progress(0.0, text="Procesando...")
        columnas = st.columns(4)

        for i, archivo in enumerate(archivos):
            try:
                raw_bytes = archivo.getvalue()
                procesada = process_image(raw_bytes, session, size, fill, bg_rgba)
                nombre_salida = f"{Path(archivo.name).stem}_catalogo.png"
                png_bytes = image_to_png_bytes(procesada, transparent)
                resultados.append((nombre_salida, png_bytes))

                with columnas[i % 4]:
                    preview = procesada.convert("RGB") if not transparent else procesada
                    preview.thumbnail((MAX_PREVIEW_DIM, MAX_PREVIEW_DIM))
                    st.image(preview, caption=nombre_salida, use_container_width=True)

            except Exception as e:
                st.error(f"No se pudo procesar **{archivo.name}**: {e}")

            progreso.progress((i + 1) / len(archivos), text=f"Procesando... ({i + 1}/{len(archivos)})")

        progreso.empty()

        if resultados:
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for nombre, data in resultados:
                    zf.writestr(nombre, data)
            zip_buf.seek(0)

            st.success(f"✅ Listo: {len(resultados)} de {len(archivos)} imagen(es) procesada(s).")
            st.download_button(
                "⬇️ Descargar todas (.zip)",
                data=zip_buf,
                file_name=f"catalogo_{plataforma.lower().replace(' ', '_')}.zip",
                mime="application/zip",
                type="primary",
            )
        else:
            st.warning("No se pudo procesar ninguna imagen del lote.")

# ────────────────────────────────────────────────────────────────────────────
# Footer
# ────────────────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray; font-size:0.9em;'>"
    "Plataforma creada por <b>clasemartinez</b> · "
    "<a href='https://www.linkedin.com/in/claudiomartinez1/' target='_blank'>LinkedIn</a>"
    "</div>",
    unsafe_allow_html=True,
)
