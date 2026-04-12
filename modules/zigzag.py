from core.pdf_engine import create_canvas, save_canvas
from templates.layout import draw_border, draw_title_block


ZIG_W = 140
ZIG_H = 65


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


def draw_zig(c, x, y, w, h):
    """
    Accurate 2-peak zig-zag (matches your PDF style)
    """

    step = w / 4  # divide into 4 segments

    path = c.beginPath()

    # Bottom edge with TWO peaks
    path.moveTo(x, y)
    path.lineTo(x + step, y + h * 0.35)
    path.lineTo(x + 2 * step, y)
    path.lineTo(x + 3 * step, y + h * 0.35)
    path.lineTo(x + w, y)

    # Right side
    path.lineTo(x + w, y + h)

    # Top edge mirrored (inverse peaks)
    path.lineTo(x + 3 * step, y + h * 0.65)
    path.lineTo(x + 2 * step, y + h)
    path.lineTo(x + step, y + h * 0.65)
    path.lineTo(x, y + h)

    path.close()
    c.drawPath(path)

def draw_plate(c, rows, cols):
    page_w, page_h = c._pagesize

    gap = 10
    padding = 20

    plate_w = cols * ZIG_W + (cols - 1) * gap + 2 * padding
    plate_h = rows * ZIG_H + (rows - 1) * gap + 2 * padding

    start_x = (page_w - plate_w) / 2
    start_y = (page_h - plate_h) / 2 + 80

    # Outer plate
    c.rect(start_x, start_y, plate_w, plate_h)

    # Draw zig cavities
    for r in range(rows):
        for col in range(cols):
            x = start_x + padding + col * (ZIG_W + gap)
            y = start_y + padding + r * (ZIG_H + gap)

            draw_single_zig(c, x, y, ZIG_W, ZIG_H)


def generate_zigzag_mould(filename, cavities):
    c = create_canvas(filename)

    draw_border(c)
    draw_title_block(c)

    rows, cols = get_grid(cavities)
    draw_plate(c, rows, cols)

    save_canvas(c)
