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

    # SETTINGS
    length = template["length"]
    width = template["width"]
    wall = 10  # wall thickness
    gap = 20
    margin = 50

    start_x = 50
    start_y = 650

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(160, 800, "MOULD DESIGN")

    # Calculate total frame
    total_width = cols * (length + 2*wall) + (cols - 1) * gap + 2 * margin
    total_height = rows * (width + 2*wall) + (rows - 1) * gap + 2 * margin

    # Draw outer frame
    c.setLineWidth(2)
    c.rect(start_x, start_y - total_height, total_width, total_height)

    count = 0

    for r in range(rows):
        for col in range(cols):
            if count >= cavities:
                break

            x = start_x + margin + col * (length + 2*wall + gap)
            y = start_y - margin - r * (width + 2*wall + gap)

            # OUTER cavity (mould steel)
            c.setLineWidth(1.5)
            c.rect(x, y, length + 2*wall, width + 2*wall)

            # INNER cavity (actual brick space)
            c.setLineWidth(1)
            c.rect(x + wall, y + wall, length, width)

            # SPECIAL SHAPES
            if mould_type == "zigzag":
                # draw zigzag line
                for i in range(5):
                    c.line(
                        x + wall + i*40,
                        y + wall,
                        x + wall + (i+1)*40,
                        y + wall + width
                    )

            elif mould_type == "ishape":
                # draw I shape
                cx = x + wall + length/2
                cy = y + wall + width/2

                c.setLineWidth(1)
                c.line(cx, y + wall, cx, y + wall + width)
                c.line(cx - 20, cy, cx + 20, cy)

            count += 1

    c.save()
    return file_path


if __name__ == "__main__":
    app.run(debug=True)
