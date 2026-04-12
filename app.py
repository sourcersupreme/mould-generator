from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

# Template data (can expand later)
TEMPLATES = {
    "brick": {
        "length": 230,
        "width": 110,
        "gap": 20,
        "margin": 40
    },
    "zigzag": {
        "length": 230,
        "width": 110,
        "gap": 20,
        "margin": 40
    },
    "ishape": {
        "length": 200,
        "width": 100,
        "gap": 20,
        "margin": 40
    }
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mould_type = request.form["mould"]
        cavities = int(request.form["cavities"])
        layout = request.form["layout"]

        rows, cols = map(int, layout.split("x"))

        # Validation
        if rows * cols != cavities:
            return "❌ Layout does not match cavity count"

        template = TEMPLATES[mould_type]

        pdf_path = generate_pdf(mould_type, cavities, rows, cols, template)

        return send_file(pdf_path, as_attachment=True)

    return render_template("index.html")


def generate_pdf(mould_type, cavities, rows, cols, template):
    file_path = "mould_design.pdf"

    c = canvas.Canvas(file_path)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "MOULD DESIGN")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Type: {mould_type}")
    c.drawString(50, 740, f"Cavities: {cavities}")
    c.drawString(50, 720, f"Layout: {rows} x {cols}")

    # Drawing parameters
    length = template["length"]
    width = template["width"]
    gap = template["gap"]
    margin = template["margin"]

    start_x = 50
    start_y = 500

    # Draw cavities
    for r in range(rows):
        for col in range(cols):
            x = start_x + col * (length + gap)
            y = start_y - r * (width + gap)

            c.rect(x, y, length, width)

    c.save()
    return file_path


if __name__ == "__main__":
    app.run(debug=True)
