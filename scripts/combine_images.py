#!/usr/bin/env python3
"""
E-commerce catalog image — image combiner.

Combines two images for catalog use. Four combination modes:

  overlay-logo    Overlays image B (logo / graphic) over image A (product)
  side-by-side    Places A and B side by side at equal height (color variants, before/after)
  grid            Arranges A and B in a 1×2 or 2×2 grid (multi-SKU view)
  lifestyle-scene Places product A centered over background/scene B

Usage:
    python combine_images.py --image-a <path> --image-b <path> --mode <mode> [options]

Common options:
    --output PATH           Output image path
    --platform PLATFORM     google_shopping (default) | mercado_libre | pinterest | instagram | custom

overlay-logo options:
    --position POSITION     center (default) | bottom-right | top-right | top-left | bottom-left
    --logo-scale FLOAT      Logo width as fraction of base image width (default: 0.25)
    --opacity FLOAT         Logo opacity 0.0–1.0 (default: 1.0)

side-by-side / grid options:
    --gap INT               Gap between images in pixels (default: 20)
    --bg-color COLOR        white (default) | gray | light-gray

grid options:
    --cols INT              Grid columns: 1 or 2 (default: 2)

lifestyle-scene options:
    --product-scale FLOAT   Product size as fraction of background (default: 0.50)
    --position POSITION     center (default) | bottom-right | bottom-left

Requirements:
    pip install pillow --break-system-packages
"""

import argparse
import sys
from pathlib import Path


PLATFORM_SPECS = {
    "google_shopping": (1200, 1200),
    "mercado_libre":   (1200, 1200),
    "pinterest":       (1000, 1500),
    "instagram":       (1080, 1080),
    "custom":          None,
}

BG_COLORS = {
    "white":        (255, 255, 255, 255),
    "gray":         (242, 242, 242, 255),
    "light-gray":   (230, 230, 230, 255),
}

POSITIONS = {
    "center":       lambda cw, ch, iw, ih: ((cw - iw) // 2, (ch - ih) // 2),
    "top-left":     lambda cw, ch, iw, ih: (24, 24),
    "top-right":    lambda cw, ch, iw, ih: (cw - iw - 24, 24),
    "bottom-left":  lambda cw, ch, iw, ih: (24, ch - ih - 24),
    "bottom-right": lambda cw, ch, iw, ih: (cw - iw - 24, ch - ih - 24),
}


def check_dependencies():
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("[ERROR] Pillow no está instalado.")
        print("        Instalar con: pip install pillow --break-system-packages")
        sys.exit(1)


def _load(path):
    """Load an image and convert to RGBA."""
    from PIL import Image
    return Image.open(str(path)).convert("RGBA")


def _position(name, canvas_w, canvas_h, img_w, img_h):
    fn = POSITIONS.get(name, POSITIONS["center"])
    return fn(canvas_w, canvas_h, img_w, img_h)


# ── Combination modes ──────────────────────────────────────────────────────────

def mode_overlay_logo(img_a, img_b, position="center", logo_scale=0.25, opacity=1.0):
    """Overlay img_b (logo/graphic) on top of img_a (product). No background change."""
    from PIL import Image

    base = img_a.copy()
    logo = img_b.copy()

    # Scale logo to a fraction of the base image width
    max_dim = int(min(base.width, base.height) * logo_scale)
    logo.thumbnail((max_dim, max_dim), Image.LANCZOS)

    # Apply opacity
    if opacity < 1.0:
        r, g, b, a = logo.split()
        a = a.point(lambda v: int(v * opacity))
        logo = Image.merge("RGBA", (r, g, b, a))

    x, y = _position(position, base.width, base.height, logo.width, logo.height)
    base.paste(logo, (x, y), logo)
    return base


def mode_side_by_side(img_a, img_b, gap=20, bg_rgba=(255, 255, 255, 255)):
    """Place img_a and img_b side by side at equal height."""
    from PIL import Image

    target_h = max(img_a.height, img_b.height)

    def _fit_height(img, h):
        ratio = h / img.height
        return img.resize((int(img.width * ratio), h), Image.LANCZOS)

    a = _fit_height(img_a, target_h)
    b = _fit_height(img_b, target_h)

    total_w = a.width + gap + b.width
    canvas = Image.new("RGBA", (total_w, target_h), bg_rgba)
    canvas.paste(a, (0, 0), a)
    canvas.paste(b, (a.width + gap, 0), b)
    return canvas


def mode_grid(img_a, img_b, cols=2, gap=20, bg_rgba=(255, 255, 255, 255)):
    """Arrange img_a and img_b in a grid (1×2 or 2×2)."""
    from PIL import Image

    images = [img_a, img_b]
    cell_w = max(img.width for img in images)
    cell_h = max(img.height for img in images)
    rows = (len(images) + cols - 1) // cols

    total_w = cols * cell_w + (cols - 1) * gap
    total_h = rows * cell_h + (rows - 1) * gap
    canvas = Image.new("RGBA", (total_w, total_h), bg_rgba)

    for i, img in enumerate(images):
        row = i // cols
        col = i % cols
        # Center each image within its cell
        cell_x = col * (cell_w + gap) + (cell_w - img.width) // 2
        cell_y = row * (cell_h + gap) + (cell_h - img.height) // 2
        canvas.paste(img, (cell_x, cell_y), img)

    return canvas


def mode_lifestyle_scene(img_product, img_background, product_scale=0.50, position="center"):
    """Composite product (A) over a background / scene (B)."""
    from PIL import Image

    scene = img_background.copy()
    product = img_product.copy()

    max_w = int(scene.width * product_scale)
    max_h = int(scene.height * product_scale)
    product.thumbnail((max_w, max_h), Image.LANCZOS)

    x, y = _position(position, scene.width, scene.height, product.width, product.height)
    scene.paste(product, (x, y), product)
    return scene


# ── Platform resize ────────────────────────────────────────────────────────────

def resize_to_platform(img, platform, bg_rgba=(255, 255, 255, 255)):
    """Resize and center a composed image to the target platform canvas."""
    from PIL import Image

    target = PLATFORM_SPECS.get(platform)
    if target is None:
        return img  # custom: no resize

    canvas_w, canvas_h = target
    img_copy = img.copy()
    img_copy.thumbnail((int(canvas_w * 0.90), int(canvas_h * 0.90)), Image.LANCZOS)

    canvas = Image.new("RGBA", (canvas_w, canvas_h), bg_rgba)
    x = (canvas_w - img_copy.width) // 2
    y = (canvas_h - img_copy.height) // 2
    canvas.paste(img_copy, (x, y), img_copy)
    return canvas


# ── Main ───────────────────────────────────────────────────────────────────────

def combine_images(image_a_path, image_b_path, mode, output_path=None,
                   platform="google_shopping", bg_color="white",
                   position="center", logo_scale=0.25, opacity=1.0,
                   gap=20, cols=2, product_scale=0.50):
    """
    Combine two images and save the result.

    Returns the output file path as a string.
    """
    check_dependencies()

    img_a = _load(image_a_path)
    img_b = _load(image_b_path)
    bg_rgba = BG_COLORS.get(bg_color, BG_COLORS["white"])

    print(f"→ Imagen A : {image_a_path}  ({img_a.size[0]}×{img_a.size[1]})")
    print(f"→ Imagen B : {image_b_path}  ({img_b.size[0]}×{img_b.size[1]})")
    print(f"→ Modo     : {mode}")

    if mode == "overlay-logo":
        result = mode_overlay_logo(img_a, img_b, position, logo_scale, opacity)
    elif mode == "side-by-side":
        result = mode_side_by_side(img_a, img_b, gap, bg_rgba)
    elif mode == "grid":
        result = mode_grid(img_a, img_b, cols, gap, bg_rgba)
    elif mode == "lifestyle-scene":
        result = mode_lifestyle_scene(img_a, img_b, product_scale, position)
    else:
        print(f"[ERROR] Modo desconocido: {mode}")
        sys.exit(1)

    # Resize to platform
    if platform != "custom":
        result = resize_to_platform(result, platform, bg_rgba)

    # Determine output path
    if output_path is None:
        p = Path(str(image_a_path))
        output_path = str(p.parent / f"{p.stem}_{mode}_catalog.png")

    result.convert("RGB").save(str(output_path), "PNG")

    print(f"✓ Imagen guardada : {output_path}")
    print(f"  Dimensiones     : {result.size[0]} × {result.size[1]} px")
    print(f"  Plataforma      : {platform}")

    return output_path


if __name__ == "__main__":
    check_dependencies()

    parser = argparse.ArgumentParser(
        description="Combine two images for e-commerce catalog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--image-a", required=True, help="Primary image (product)")
    parser.add_argument("--image-b", required=True, help="Secondary image (logo, variant, scene)")
    parser.add_argument(
        "--mode", required=True,
        choices=["overlay-logo", "side-by-side", "grid", "lifestyle-scene"],
        help="Combination type",
    )
    parser.add_argument("--output", default=None)
    parser.add_argument(
        "--platform", default="google_shopping",
        choices=list(PLATFORM_SPECS.keys()),
    )
    parser.add_argument(
        "--bg-color", default="white",
        choices=list(BG_COLORS.keys()),
    )
    parser.add_argument(
        "--position", default="center",
        choices=list(POSITIONS.keys()),
    )
    parser.add_argument(
        "--logo-scale", type=float, default=0.25,
        help="Logo size as fraction of base image (default: 0.25)",
    )
    parser.add_argument(
        "--opacity", type=float, default=1.0,
        help="Overlay opacity 0.0–1.0 (default: 1.0)",
    )
    parser.add_argument(
        "--gap", type=int, default=20,
        help="Gap between images in pixels (default: 20)",
    )
    parser.add_argument(
        "--cols", type=int, default=2, choices=[1, 2],
        help="Grid columns (default: 2)",
    )
    parser.add_argument(
        "--product-scale", type=float, default=0.50,
        help="Product size as fraction of background (default: 0.50)",
    )

    args = parser.parse_args()
    combine_images(
        args.image_a, args.image_b, args.mode, args.output, args.platform,
        args.bg_color, args.position, args.logo_scale, args.opacity,
        args.gap, args.cols, args.product_scale,
    )
