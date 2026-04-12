from core.pdf_engine import create_canvas, save_canvas
from templates.layout import draw_border, draw_title_block


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


def draw_zigzag_shape(c, x, y, w, h):
    mid_x = x + w / 2

    path = c.beginPath()

    # Bottom edge
    path.moveTo(x, y)
    path.lineTo(mid_x, y + h * 0.4)   # SINGLE PEAK
    path.lineTo(x + w, y)

    # Right side
    path.lineTo(x + w, y + h)

    # Top edge (mirror)
    path.lineTo(mid_x, y + h * 0.6)
    path.lineTo(x, y + h)

    # Close
    path.close()

    c.drawPath(path)


def draw_plate(c, rows, cols):
    page_w, page_h = c._pagesize

    plate_w = 750
    plate_h = 300

    start_x = (page_w - plate_w) / 2
    start_y = (page_h - plate_h) / 2 + 100

    c.rect(start_x, start_y, plate_w, plate_h)

    padding = 15
    gap = 8

    cell_w = (plate_w - 2*padding - (cols-1)*gap) / cols
    cell_h = (plate_h - 2*padding - (rows-1)*gap) / rows

    for r in range(rows):
        for col in range(cols):
            x = start_x + padding + col * (cell_w + gap)
            y = start_y + padding + r * (cell_h + gap)

            draw_zigzag_shape(c, x, y, cell_w, cell_h)


def generate_zigzag_mould(filename, cavities):
    c = create_canvas(filename)

    draw_border(c)
    draw_title_block(c)

    rows, cols = get_grid(cavities)
    draw_plate(c, rows, cols)

    save_canvas(c)
