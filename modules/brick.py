from core.pdf_engine import create_canvas, save_canvas
from templates.layout import draw_border, draw_title_block


def draw_top_view(c):
    # Outer plate
    c.rect(200, 300, 600, 300)

    # Inner cavities (grid)
    x_start = 220
    y_start = 320
    width = 120
    height = 120

    for row in range(2):
        for col in range(4):
            x = x_start + col * 140
            y = y_start + row * 140
            c.rect(x, y, width, height)


def draw_front_view(c):
    c.rect(200, 200, 600, 80)


def draw_side_view(c):
    c.rect(100, 300, 80, 300)


def generate_brick_mould(filename):
    c = create_canvas(filename)

    # Layout
    draw_border(c)
    draw_title_block(c)

    # Views
    draw_top_view(c)
    draw_front_view(c)
    draw_side_view(c)

    save_canvas(c)
