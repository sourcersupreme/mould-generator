from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3

def create_canvas(filename):
    return canvas.Canvas(filename, pagesize=A3)

def save_canvas(c):
    c.save()
