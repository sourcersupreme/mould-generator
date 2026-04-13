from core.pdf_engine import create_canvas, save_canvas
from templates.layout import draw_border, draw_title_block


# Fixed cavity size (same as brick for consistency)
ZIG_W = 120
ZIG_H = 70


def get_grid(cavities):
    mapping = {
        4: (2, 2),
        6: (2, 3),
        8: (2, 4),
        9: (3, 3),
        10: (2, 5),
        12: (3, 4)
    }
    return mapping.get(cavities, (2, 4))


# 🔥 CORE FUNCTION (IMPORTANT)
def draw_zig_row(c, start_x, y, cols, w, h, gap):
    """
    Draw one continuous zig-zag row (matches real mould design)
    """

    step = w / 4
    path = c.beginPath()

    x = start_x

    # Start point
    path.moveTo(x, y)

    # Bottom zig (continuous across row)
    for _ in range(cols):
        path.lineTo(x + step, y + h * 0.35)
        path.lineTo(x + 2 * step, y)
        path.lineTo(x + 3 * step, y + h * 0.35)
        path.lineTo(x + w, y)

        x += w + gap

    # Right vertical
    path.lineTo(x - gap, y + h)

    # Top zig (reverse direction)
    for _ in range(cols):
        x -= (w + gap)

        path.lineTo(x + 3 * step, y + h * 0.65)
        path.lineTo(x + 2 * step, y + h)
        path.lineTo(x + step, y + h * 0.65)
        path.lineTo(x, y + h)

    path.close()
    c.drawPath(path)


def draw_plate(c, rows, cols):
    page_w, page_h = c._pagesize

    gap = 8
    padding = 18

    # Plate auto-size
    plate_w = cols * ZIG_W + (cols - 1) * gap + 2 * padding
    plate_h = rows * ZIG_H + (rows - 1) * gap + 2 * padding

    # Center placement
    start_x = (page_w - plate_w) / 2
    start_y = (page_h - plate_h) / 2 + 60

    # Outer plate
    c.rect(start_x, start_y, plate_w, plate_h)

    # Draw rows (IMPORTANT: row-based, not cell-based)
    for r in range(rows):
        y = start_y + padding + r * (ZIG_H + gap)

        draw_zig_row(
            c,
            start_x + padding,
            y,
            cols,
            ZIG_W,
            ZIG_H,
            gap
        )


def generate_zigzag_mould(filename, cavities):
    c = create_canvas(filename)

    draw_border(c)
    draw_title_block(c)

    rows, cols = get_grid(cavities)
    draw_plate(c, rows, cols)

    save_canvas(c)
