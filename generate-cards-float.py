from reportlab.lib.pagesizes import A6, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Flowable
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
import random

def generate_pdf(titles, a, b, output_file):
    # Create a PDF document with landscape A6 size
    pdf = SimpleDocTemplate(output_file, pagesize=landscape(A6))
    elements = []

    # Define styles for the title and float value
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=40,
        leading=30,
        alignment=TA_CENTER,
        spaceAfter=20,
        spaceBefore=10
    )
    
    value_style = ParagraphStyle(
        name="ValueStyle",
        fontSize=28,
        leading=20,
        alignment=TA_CENTER,
    )

    # Add a title and a random float value to each page
    for title in titles:
        value = f"{random.uniform(a, b):.2f}"
        elements.append(Paragraph("~", value_style))
        elements.append(Paragraph(title, title_style))
        elements.append(Paragraph(value, value_style))
        elements.append(PageBreak())  # Ensure each title-value pair is on a separate page

    # Build the PDF
    pdf.build(elements)

# Splitting the text into a Python array
operation_names = [
    "HAMMER",
    "OVERLOAD",
    "OMAHA",
    "SWORD",
    "WHISKY",
    "JUNO",
    "CITADEL",
    "BEAU",
    "NEPTUNE",
    "OLYMPIC",
    "BACKER",
    "FOXTROT",
    "MARINE",
    "BARBAROSSA",
    "THOR",
    "PATRIOT",
    "VICTOR",
    "DRAGON",
    "SPARTAN",
    "TRIDENT",
    "TITAN",
    "VIKING",
    "PHOENIX",
    "REAPER",
    "HORIZON",
    "RAPTOR",
    "STORM",
    "HERCULES",
    "SENTINEL",
    "VORTEX",
    "FALCON",
    "HAWK",
    "TUNDRA"
]

a = 10.0  # Lower bound for random float
b = 50.0  # Upper bound for random float
output_file = "output.pdf"

generate_pdf(operation_names, a, b, output_file)
