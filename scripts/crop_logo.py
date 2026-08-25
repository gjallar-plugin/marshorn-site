from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "img"
SRC = ROOT / "company_logo.png"


def bbox(mask: np.ndarray) -> tuple[int, int, int, int]:
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def pad(box: tuple[int, int, int, int], pad_px: int, size: tuple[int, int]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    w, h = size
    return max(0, x0 - pad_px), max(0, y0 - pad_px), min(w, x1 + pad_px), min(h, y1 + pad_px)


def square_around(box: tuple[int, int, int, int], size: tuple[int, int]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    side = max(x1 - x0, y1 - y0)
    half = side / 2
    sx0, sy0 = int(round(cx - half)), int(round(cy - half))
    sx1, sy1 = sx0 + int(round(side)), sy0 + int(round(side))
    w, h = size
    if sx0 < 0:
        sx1 -= sx0
        sx0 = 0
    if sy0 < 0:
        sy1 -= sy0
        sy0 = 0
    if sx1 > w:
        sx0 -= sx1 - w
        sx1 = w
    if sy1 > h:
        sy0 -= sy1 - h
        sy1 = h
    return max(0, sx0), max(0, sy0), min(w, sx1), min(h, sy1)


def main() -> None:
    im = Image.open(SRC).convert("RGB")
    arr = np.asarray(im)
    lum = arr.mean(axis=2)
    bright = lum > 80

    # Stacked lockup: ram above MARSHORN, with margin like the brand sheet.
    x0, y0, x1, y1 = bbox(bright)
    lockup = (
        max(0, x0 - 68),
        max(0, y0 - 81),
        min(im.width, x1 + 68),
        min(im.height, y1 + 81),
    )
    lockup_im = im.crop(lockup)
    lockup_im.save(ROOT / "company_logo_web.png", optimize=True)

    icon_mask = bright.copy()
    icon_mask[401:] = False
    mark = square_around(pad(bbox(icon_mask), 12, im.size), im.size)
    mark_im = im.crop(mark)
    mark_im.resize((128, 128), Image.Resampling.LANCZOS).save(ROOT / "company_mark.png", optimize=True)
    mark_im.resize((64, 64), Image.Resampling.LANCZOS).save(ROOT / "favicon.png", optimize=True)
    print("lockup", lockup, "->", lockup_im.size)
    print("mark", mark)


if __name__ == "__main__":
    main()
