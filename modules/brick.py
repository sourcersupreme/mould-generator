from core.pdf_engine import create_canvas, save_canvas
from templates.layout import draw_border, draw_title_block


# Realistic brick ratio (based on your PDFs)
BRICK_W = 120
BRICK_H = 70


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


def draw_plate(c, rows, cols):
    page_w, page_h = c._pagesize

    gap = 8
    padding = 18

    # Plate auto-size from bricks
    plate_w = cols * BRICK_W + (cols - 1) * gap + 2 * padding
    plate_h = rows * BRICK_H + (rows - 1) * gap + 2 * padding

    # Perfect center
    start_x = (page_w - plate_w) / 2
    start_y = (page_h - plate_h) / 2 + 60

    # Outer plate
    c.rect(start_x, start_y, plate_w, plate_h)

    # Draw bricks
    for r in range(rows):
        for col in range(cols):
            x = start_x + padding + col * (BRICK_W + gap)
            y = start_y + padding + r * (BRICK_H + gap)

            c.rect(x, y, BRICK_W, BRICK_H)


def generate_brick_mould(filename, cavities):
    c = create_canvas(filename)

    draw_border(c)
    draw_title_block(c)

    rows, cols = get_grid(cavities)
    draw_plate(c, rows, cols)

    save_canvas(c)
