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

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, 800, "MOULD DESIGN DRAWING")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Type: {mould_type}")
    c.drawString(50, 740, f"Cavities: {cavities}")
    c.drawString(50, 720, f"Layout Auto: {rows} x {cols}")

    length = template["length"]
    width = template["width"]

    # Calculate frame size
    total_width = cols * length + (cols - 1) * GAP + 2 * MARGIN
    total_height = rows * width + (rows - 1) * GAP + 2 * MARGIN

    start_x = 50
    start_y = 600

    # Draw outer frame
    c.setLineWidth(2)
    c.rect(start_x, start_y - total_height, total_width, total_height)

    # Draw cavities
    c.setLineWidth(1)
    count = 0

    for r in range(rows):
        for col in range(cols):
            if count >= cavities:
                break

            x = start_x + MARGIN + col * (length + GAP)
            y = start_y - MARGIN - r * (width + GAP)

            c.rect(x, y, length, width)

            # Dimension text inside cavity
            c.setFont("Helvetica", 8)
            c.drawString(x + 5, y + width / 2, f"{length}x{width}")

            count += 1

    # Draw bolt holes (4 corners)
    c.setLineWidth(1)
    bolt_r = 5

    bolts = [
        (start_x + BOLT_OFFSET, start_y - BOLT_OFFSET),
        (start_x + total_width - BOLT_OFFSET, start_y - BOLT_OFFSET),
        (start_x + BOLT_OFFSET, start_y - total_height + BOLT_OFFSET),
        (start_x + total_width - BOLT_OFFSET, start_y - total_height + BOLT_OFFSET),
    ]

    for bx, by in bolts:
        c.circle(bx, by, bolt_r)

    # Outer dimensions
    c.setFont("Helvetica", 10)
    c.drawString(start_x, start_y + 10, f"Width: {total_width} mm")
    c.drawString(start_x + total_width + 10, start_y - total_height / 2, f"Height: {total_height} mm")

    c.save()
    return file_path


if __name__ == "__main__":
    app.run(debug=True)
