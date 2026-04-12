def draw_border(c):
    width, height = c._pagesize
    margin = 20
    c.rect(margin, margin, width - 2*margin, height - 2*margin)


def draw_title_block(c):
    c.setFont("Helvetica", 10)

    c.rect(800, 20, 300, 120)

    c.drawString(810, 120, "SHREE CHAMUNDA DIE & ENGINEERS")
    c.drawString(810, 100, "MOULD DESIGN")
    c.drawString(810, 80, "DRAWING TYPE: BRICK MOULD")
    c.drawString(810, 60, "UNIT: MM")
