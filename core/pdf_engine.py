from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3

def create_canvas(filename):
    c = canvas.Canvas(filename, pagesize=A3)
    return c

def save_canvas(c):
    c.save()
