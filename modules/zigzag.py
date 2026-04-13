from core.pdf_engine import create_canvas, save_canvas
from templates.layout import draw_border, draw_title_block


# Fixed cavity size (tuned to look like your mould)
zig = w * 0.08
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
    FINAL PRODUCTION-LEVEL zig cavity
    Matches real mould geometry closely
    """

    zig = w * 0.10   # very shallow like real mould
    step = h / 4

    path = c.beginPath()

    # START top-left
    path.moveTo(x, y + h)

    # TOP edge
    path.lineTo(x + w, y + h)

    # RIGHT SIDE (controlled industrial zig)
    path.lineTo(x + w, y + h - step*0.6)
    path.lineTo(x + w - zig, y + h - step)

    path.lineTo(x + w - zig, y + h - step*2 + step*0.6)
    path.lineTo(x + w, y + h - step*2)

    path.lineTo(x + w, y + step*0.6)
    path.lineTo(x + w - zig, y + step)

    path.lineTo(x + w - zig, y + step*2 - step*0.6)
    path.lineTo(x + w, y)

    # BOTTOM edge
    path.lineTo(x, y)

    # LEFT SIDE (perfect mirror)
    path.lineTo(x, y + step*0.6)
    path.lineTo(x + zig, y + step)

    path.lineTo(x + zig, y + step*2 - step*0.6)
    path.lineTo(x, y + step*2)

    path.lineTo(x, y + h - step*0.6)
    path.lineTo(x + zig, y + h - step)

    path.lineTo(x + zig, y + h - step*2 + step*0.6)
    path.lineTo(x, y + h)

    path.close()
    c.drawPath(path)

def draw_plate(c, rows, cols):
    page_w, page_h = c._pagesize

    gap = 4
    padding = 20

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
