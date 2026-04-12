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
    file_path = "mould_design.pdf"
    c = canvas.Canvas(file_path)

    # PARAMETERS (based on your real drawings)
    L = template["length"]
    W = template["width"]
    WALL = 10
    GAP = 15
    MARGIN = 40
    DEPTH = 100
    PLATE = 12

    # ---------- TITLE ----------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(180, 800, "MOULD DESIGN DRAWING")

    # ---------- TOP VIEW ----------
    start_x = 50
    start_y = 650

    total_w = cols * (L + WALL) + (cols - 1) * GAP + 2 * MARGIN
    total_h = rows * (W + WALL) + (rows - 1) * GAP + 2 * MARGIN

    c.drawString(start_x, start_y + 20, "TOP VIEW")

    # Outer frame
    c.setLineWidth(2)
    c.rect(start_x, start_y - total_h, total_w, total_h)

    # Continuous cavity walls (IMPORTANT CHANGE)
    c.setLineWidth(1)

    for r in range(rows):
        for col in range(cols):
            x = start_x + MARGIN + col * (L + GAP)
            y = start_y - MARGIN - r * (W + GAP)

            c.rect(x, y, L, W)

    # Internal partition walls (connect cavities)
    for col in range(1, cols):
        x = start_x + MARGIN + col * (L + GAP) - GAP/2
        c.setLineWidth(2)
        c.line(x, start_y - MARGIN, x, start_y - total_h + MARGIN)

    for r in range(1, rows):
        y = start_y - MARGIN - r * (W + GAP) + GAP/2
        c.line(start_x + MARGIN, y, start_x + total_w - MARGIN, y)

    # ---------- FRONT VIEW ----------
    front_x = 50
    front_y = 300

    c.drawString(front_x, front_y + 20, "FRONT VIEW")

    width_total = total_w

    # Bottom plate
    c.setLineWidth(2)
    c.rect(front_x, front_y, width_total, PLATE)

    # Cavity depth
    c.rect(front_x, front_y + PLATE, width_total, DEPTH)

    # Top plate
    c.rect(front_x, front_y + PLATE + DEPTH, width_total, PLATE)

    # Vertical divisions (match cavities)
    for col in range(1, cols):
        x = front_x + col * (width_total / cols)
        c.line(x, front_y + PLATE, x, front_y + PLATE + DEPTH)

    # ---------- BOLT PATTERN (REALISTIC) ----------
    bolt_y = front_y + PLATE + DEPTH + PLATE/2

    for i in range(6):
        bx = front_x + 50 + i * 80
        c.circle(bx, bolt_y, 4)

    # ---------- TEXT ----------
    c.setFont("Helvetica", 10)
    c.drawString(50, 100, f"Type: {mould_type}")
    c.drawString(50, 85, f"Cavities: {cavities}")
    c.drawString(50, 70, f"Layout: {rows} x {cols}")

    c.save()
    return file_path

if __name__ == "__main__":
    app.run(debug=True)
