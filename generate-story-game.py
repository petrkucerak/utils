from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph

input_file = "story-game.txt"
output_file = "story-game.pdf"

# Load file
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
    # Load keys from header line
    keys = lines[0].replace("\n", "").split("\t")
    lines.pop(0)

    # Load values
    data = []
    for line in lines:
        line = line.replace("\n", "").split("\t")
        card_data = {}
        for i in range(len(keys)):
            card_data[keys[i]] = line[i]
        data.append(card_data)

# Register font
pdfmetrics.registerFont(TTFont('Roboto', 'assets/fonts/Roboto/Roboto-Regular.ttf'))
pdfmetrics.registerFont(TTFont('RobotoMedium', 'assets/fonts/Roboto/Roboto-Medium.ttf'))
pdfmetrics.registerFont(TTFont('RobotoBold', 'assets/fonts/Roboto/Roboto-Bold.ttf'))

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(name='Title', fontName='RobotoBold', fontSize=30, leading=40)
text_style = ParagraphStyle(name='Normal', fontName='Roboto', fontSize=18, leading=26)
instruction_style = ParagraphStyle(name='Instruction', fontName='RobotoMedium', fontSize=18, leading=27)
options_style = ParagraphStyle(name='Normal', fontName='Roboto', fontSize=18, leading=24)

# Function to draw a card on a PDF page
def draw_card(c, card, page_width, page_height):
    def draw_paragraph(text, x, y, width, style):
        p = Paragraph(text, style)
        w, h = p.wrap(width, y)
        p.drawOn(c, x, y - h)
        return y - h

    title = f"{card.get('Číslo', '')}. {card.get('Název kartičky', '')}"
    y = page_height - 50
    y = draw_paragraph(title, 50, y, page_width - 100, title_style)
    y -= 20

    y = draw_paragraph(card.get('Text', ''), 50, y, page_width - 100, text_style)
    y -= 20
    y = draw_paragraph(card.get('Instrukce', ''), 50, y, page_width - 100, instruction_style)
    y -= 20

    for i in ['A', 'B', 'C', 'D', 'E', 'F']:
        if card.get(f'Možnost {i}'):
            y = draw_paragraph(f"{i}) {card.get(f'Možnost {i}', '')} -> {card.get(f'Číslo {i}', '')}", 50, y, page_width - 100, options_style)
            y -= 10

# Create PDF
c = canvas.Canvas(output_file, pagesize=A5)
page_width, page_height = A5

for card in data:
    draw_card(c, card, page_width, page_height)
    c.showPage()

c.save()

print(f"PDF file '{output_file}' has been created.")
