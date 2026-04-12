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
    # Create zig pattern inside rectangle
    step = w / 6

    points = [
        (x, y),
        (x + step, y + h*0.3),
        (x + 2*step, y),
        (x + 3*step, y + h*0.3),
        (x + 4*step, y),
        (x + 5*step, y + h*0.3),
        (x + w, y),
        (x + w, y + h),
        (x + 5*step, y + h*0.7),
        (x + 4*step, y + h),
        (x + 3*step, y + h*0.7),
        (x + 2*step, y + h),
        (x + step, y + h*0.7),
        (x, y + h),
    ]

    path = c.beginPath()
    path.moveTo(*points[0])

    for p in points[1:]:
        path.lineTo(*p)

    path.close()
    c.drawPath(path)


def draw_plate(c, rows, cols):
    page_w, page_h = c._pagesize

    plate_w = 700
    plate_h = 350

    start_x = (page_w - plate_w) / 2
    start_y = (page_h - plate_h) / 2 + 100

    c.rect(start_x, start_y, plate_w, plate_h)

    padding = 25
    gap = 12

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
