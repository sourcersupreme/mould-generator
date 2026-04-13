def draw_zig_cavity(c, x, y, w, h):
    """
    Draw ONE cavity like real mould:
    - straight top & bottom
    - zig on left & right sides
    """

    step = h / 4

    path = c.beginPath()

    # Start top-left
    path.moveTo(x, y + h)

    # Top edge
    path.lineTo(x + w, y + h)

    # Right zig (DOWN)
    path.lineTo(x + w - w*0.2, y + h - step)
    path.lineTo(x + w, y + h - 2*step)
    path.lineTo(x + w - w*0.2, y + h - 3*step)
    path.lineTo(x + w, y)

    # Bottom edge
    path.lineTo(x, y)

    # Left zig (UP)
    path.lineTo(x + w*0.2, y + step)
    path.lineTo(x, y + 2*step)
    path.lineTo(x + w*0.2, y + 3*step)
    path.lineTo(x, y + h)

    path.close()
    c.drawPath(path)
