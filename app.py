from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import math

app = Flask(__name__)

TEMPLATES = {
    "brick": {"length": 230, "width": 110},
    "zigzag": {"length": 230, "width": 110},
    "ishape": {"length": 200, "width": 100}
}

GAP = 20
MARGIN = 40
BOLT_OFFSET = 25


def auto_layout(cavities):
    cols = math.ceil(math.sqrt(cavities))
    rows = math.ceil(cavities / cols)
    return rows, cols


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mould_type = request.form["mould"]
        cavities = int(request.form["cavities"])

        template = TEMPLATES[mould_type]
        rows, cols = auto_layout(cavities)

        pdf_path = generate_pdf(mould_type, cavities, rows, cols, template)

        return send_file(pdf_path, as_attachment=True)

    return render_template("index.html")


def generate_pdf(mould_type, cavities, rows, cols, template):
    from reportlab.pdfgen import canvas

    file_path = "mould_design.pdf"
    c = canvas.Canvas(file_path)

    # -----------------------------
    # FIXED TEMPLATE SETTINGS
    # -----------------------------
    FRAME_WIDTH = 800
    FRAME_HEIGHT = 400
    MARGIN = 60

    CAVITY_L = template["length"]
    CAVITY_W = template["width"]

    GAP = 20
    PLATE = 12

    start_x = 50
    start_y = 700

    # -----------------------------
    # TITLE
    # -----------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, 800, "MOULD DESIGN (TEMPLATE BASED)")

    # -----------------------------
    # TOP VIEW (LIKE YOUR PDF STYLE)
    # -----------------------------
    c.drawString(start_x, start_y + 20, "TOP VIEW")

    # Outer Frame
    c.setLineWidth(2)
    c.rect(start_x, start_y - FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)

    # Inner working area
    inner_x = start_x + MARGIN
    inner_y = start_y - MARGIN

    # Auto spacing inside fixed frame
    available_w = FRAME_WIDTH - 2 * MARGIN
    available_h = FRAME_HEIGHT - 2 * MARGIN

    step_x = available_w / cols
    step_y = available_h / rows

    # -----------------------------
    # DRAW CAVITIES (REALISTIC GRID)
    # -----------------------------
    count = 0

    for r in range(rows):
        for col in range(cols):
            if count >= cavities:
                break

            cx = inner_x + col * step_x + (step_x - CAVITY_L) / 2
            cy = inner_y - r * step_y - (step_y - CAVITY_W) / 2

            # cavity box
            c.setLineWidth(1.5)
            c.rect(cx, cy, CAVITY_L, CAVITY_W)

            count += 1

    # -----------------------------
    # INTERNAL PARTITION WALLS
    # -----------------------------
    c.setLineWidth(1)

    for col in range(1, cols):
        x = inner_x + col * step_x
        c.line(x, start_y - MARGIN, x, start_y - FRAME_HEIGHT + MARGIN)

    for r in range(1, rows):
        y = inner_y - r * step_y
        c.line(inner_x, y, start_x + FRAME_WIDTH - MARGIN, y)

    # -----------------------------
    # BOLT HOLES (FIXED TEMPLATE)
    # -----------------------------
    bolt_r = 5

    bolts = [
        (start_x + 40, start_y - 40),
        (start_x + FRAME_WIDTH - 40, start_y - 40),
        (start_x + 40, start_y - FRAME_HEIGHT + 40),
        (start_x + FRAME_WIDTH - 40, start_y - FRAME_HEIGHT + 40),
    ]

    for bx, by in bolts:
        c.circle(bx, by, bolt_r)

    # -----------------------------
    # FRONT VIEW (SIMPLE BUT REAL)
    # -----------------------------
    front_y = 250

    c.drawString(start_x, front_y + 20, "FRONT VIEW")

    # bottom plate
    c.rect(start_x, front_y, FRAME_WIDTH, PLATE)

    # cavity depth block
    c.rect(start_x, front_y + PLATE, FRAME_WIDTH, 120)

    # top plate
    c.rect(start_x, front_y + PLATE + 120, FRAME_WIDTH, PLATE)

    # vertical divisions
    for col in range(1, cols):
        x = start_x + col * (FRAME_WIDTH / cols)
        c.line(x, front_y + PLATE, x, front_y + PLATE + 120)

    # -----------------------------
    # INFO TEXT
    # -----------------------------
    c.setFont("Helvetica", 10)
    c.drawString(50, 100, f"Type: {mould_type}")
    c.drawString(50, 85, f"Cavities: {cavities}")
    c.drawString(50, 70, f"Auto Layout: {rows} x {cols}")

    c.save()
    return file_path

if __name__ == "__main__":
    app.run(debug=True)
