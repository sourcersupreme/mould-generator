from core.pdf_engine import create_canvas, save_canvas
from templates.layout import draw_border, draw_title_block


def get_grid(cavities):
    mapping = {
        4: (2, 2),
        6: (2, 3),
        8: (2, 4),
        9: (3, 3),
        10: (2, 5),
        12: (3, 4),
        14: (2, 7),
        24: (4, 6)
    }
    return mapping.get(cavities, (2, 4))


def draw_top_view(c, cavities):
    rows, cols = get_grid(cavities)

    plate_w = 600
    plate_h = 300

    start_x = 200
    start_y = 350

    # Outer plate
    c.rect(start_x, start_y, plate_w, plate_h)

    # Dynamic cavity size
    padding = 20
    gap = 10

    cell_w = (plate_w - 2*padding - (cols-1)*gap) / cols
    cell_h = (plate_h - 2*padding - (rows-1)*gap) / rows

    for r in range(rows):
        for col in range(cols):
            x = start_x + padding + col * (cell_w + gap)
            y = start_y + padding + r * (cell_h + gap)
            c.rect(x, y, cell_w, cell_h)


def draw_front_view(c):
    c.rect(200, 250, 600, 80)


def draw_side_view(c):
    c.rect(100, 350, 80, 300)


def generate_brick_mould(filename, cavities):
    c = create_canvas(filename)

    draw_border(c)
    draw_title_block(c)

    draw_top_view(c, cavities)
    draw_front_view(c)
    draw_side_view(c)

    save_canvas(c)
