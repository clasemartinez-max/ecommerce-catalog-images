#!/usr/bin/env python3
"""
E-commerce catalog image — background removal.

Removes the background from a real product photo and places it on a clean
background sized to the target platform specs.

Usage:
    python remove_background.py --input <path> [options]

Options:
    --input PATH            Input image path (required)
    --output PATH           Output path (default: <input_stem>_catalog.png)
    --platform PLATFORM     google_shopping (default) | mercado_libre | pinterest | instagram | custom
    --bg-color COLOR        white (default) | gray | light-gray | transparent
    --product-fill FLOAT    Product fill ratio 0.0–1.0 (default: platform-specific, usually 0.85)

Requirements:
    pip install rembg pillow --break-system-packages
"""

import argparse
import io
import sys
from pathlib import Path


PLATFORM_SPECS = {
    "google_shopping": {"size": (1200, 1200), "fill": 0.85},
    "mercado_libre":   {"size": (1200, 1200), "fill": 0.85},
    "pinterest":       {"size": (1000, 1500), "fill": 0.80},
    "instagram":       {"size": (1080, 1080), "fill": 0.85},
    "custom":          {"size": None,         "fill": 0.85},
}

BG_COLORS = {
    "white":        (255, 255, 255, 255),
    "gray":         (242, 242, 242, 255),
    "light-gray":   (230, 230, 230, 255),
    "transparent":  (0, 0, 0, 0),
}


def check_dependencies():
    missing = []
    try:
        import rembg  # noqa: F401
    except ImportError:
        missing.append("rembg")
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        missing.append("pillow")
    if missing:
        print(f"[ERROR] Dependencias faltantes: {', '.join(missing)}")
        print(f"        Instalar con: pip install {' '.join(missing)} --break-system-packages")
        sys.exit(1)


def remove_background(input_path, output_path=None, platform="google_shopping",
                      bg_color="white", product_fill=None):
    """
    Remove background from a product photo and place it on a catalog-ready canvas.

    Returns the output file path as a string.
    """
    from rembg import remove
    from PIL import Image

    specs = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["google_shopping"])
    bg_rgba = BG_COLORS.get(bg_color, BG_COLORS["white"])
    fill = product_fill if product_fill is not None else specs["fill"]

    # ── 1. Load and remove background ───────────────────────────────────────
    print(f"→ Cargando imagen: {input_path}")
    input_path = str(input_path)
    with open(input_path, "rb") as f:
        raw = f.read()

    print("→ Eliminando fondo (rembg)...")
    result_bytes = remove(raw)
    img = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

    # ── 2. Crop to tightest bounding box (remove empty transparent border) ──
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # ── 3. Compose on canvas ─────────────────────────────────────────────────
    target_size = specs["size"]

    if target_size:
        canvas_w, canvas_h = target_size
        max_w = int(canvas_w * fill)
        max_h = int(canvas_h * fill)
        img.thumbnail((max_w, max_h), Image.LANCZOS)

        is_transparent = bg_rgba[3] == 0
        canvas = Image.new("RGBA", (canvas_w, canvas_h),
                           (0, 0, 0, 0) if is_transparent else bg_rgba)

        offset_x = (canvas_w - img.width) // 2
        offset_y = (canvas_h - img.height) // 2
        canvas.paste(img, (offset_x, offset_y), img)
        result = canvas
    else:
        # Custom: keep original canvas size, just replace background
        is_transparent = bg_rgba[3] == 0
        if is_transparent:
            result = img
        else:
            bg = Image.new("RGBA", img.size, bg_rgba)
            bg.paste(img, (0, 0), img)
            result = bg

    # ── 4. Save ───────────────────────────────────────────────────────────────
    if output_path is None:
        p = Path(input_path)
        output_path = str(p.parent / f"{p.stem}_catalog.png")

    save_mode = "RGBA" if bg_rgba[3] == 0 else "RGB"
    result.convert(save_mode).save(output_path, "PNG")

    # ── 5. Summary ────────────────────────────────────────────────────────────
    print(f"✓ Imagen guardada: {output_path}")
    print(f"  Dimensiones : {result.size[0]} × {result.size[1]} px")
    print(f"  Plataforma  : {platform}")
    print(f"  Fondo       : {bg_color}")
    print(f"  Fill        : {int(fill * 100)}% del frame")

    return output_path


if __name__ == "__main__":
    check_dependencies()

    parser = argparse.ArgumentParser(
        description="Remove background for e-commerce catalog images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--output", default=None, help="Output image path")
    parser.add_argument(
        "--platform", default="google_shopping",
        choices=list(PLATFORM_SPECS.keys()),
        help="Target platform (default: google_shopping)",
    )
    parser.add_argument(
        "--bg-color", default="white",
        choices=list(BG_COLORS.keys()),
        help="Background color (default: white)",
    )
    parser.add_argument(
        "--product-fill", type=float, default=None,
        help="Product fill ratio 0.0–1.0 (default: platform-specific)",
    )

    args = parser.parse_args()
    remove_background(
        args.input,
        args.output,
        args.platform,
        args.bg_color,
        args.product_fill,
    )
