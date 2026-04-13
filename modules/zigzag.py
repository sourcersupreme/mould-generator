from core.pdf_engine import create_canvas, save_canvas
from templates.layout import draw_border, draw_title_block


# Fixed cavity size (tuned to look like your mould)
ZIG_W = 120
ZIG_H = 80


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


# 🔥 CORE: Accurate cavity shape
def draw_zig_cavity(c, x, y, w, h):
    """
    Final accurate industrial zig cavity:
    - vertical dominant edges
    - small step notches
    - matches real mould
    """

    notch = w * 0.10   # inward cut
    step = h / 4

    path = c.beginPath()

    # Start top-left
    path.moveTo(x, y + h)

    # Top edge
    path.lineTo(x + w, y + h)

    # RIGHT SIDE (down)
    path.lineTo(x + w, y + h - step)
    path.lineTo(x + w - notch, y + h - step)

    path.lineTo(x + w - notch, y + h - 2*step)
    path.lineTo(x + w, y + h - 2*step)

    path.lineTo(x + w, y + h - 3*step)
    path.lineTo(x + w - notch, y + h - 3*step)

    path.lineTo(x + w - notch, y)
    path.lineTo(x + w, y)

    # Bottom edge
    path.lineTo(x, y)

    # LEFT SIDE (up mirrored)
    path.lineTo(x, y + step)
    path.lineTo(x + notch, y + step)

    path.lineTo(x + notch, y + 2*step)
    path.lineTo(x, y + 2*step)

    path.lineTo(x, y + 3*step)
    path.lineTo(x + notch, y + 3*step)

    path.lineTo(x + notch, y + h)
    path.lineTo(x, y + h)

    path.close()
    c.drawPath(path)

def draw_plate(c, rows, cols):
    page_w, page_h = c._pagesize

    gap = 6
    padding = 25

    # Plate size auto-calculated
    plate_w = cols * ZIG_W + (cols - 1) * gap + 2 * padding
    plate_h = rows * ZIG_H + (rows - 1) * gap + 2 * padding

    # Center alignment
    start_x = (page_w - plate_w) / 2
    start_y = (page_h - plate_h) / 2 + 60

    # Outer plate
    c.rect(start_x, start_y, plate_w, plate_h)

    # Draw cavities
    for r in range(rows):
        for col in range(cols):
            x = start_x + padding + col * (ZIG_W + gap)
            y = start_y + padding + r * (ZIG_H + gap)

            draw_zig_cavity(c, x, y, ZIG_W, ZIG_H)


def generate_zigzag_mould(filename, cavities):
    c = create_canvas(filename)

    draw_border(c)
    draw_title_block(c)

    rows, cols = get_grid(cavities)
    draw_plate(c, rows, cols)

    save_canvas(c)
