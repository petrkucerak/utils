from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import random

not_allowed_numbers = [1000, 6666, 9999]


def draw_number(c, numbers, i, x, y):
    x += 50
    y -= 50
    c.setFont("Helvetica-Bold", 80)
    c.drawString(x, y, f"{numbers[i]}")
    x += 400
    c.drawString(x, y, f"{numbers[i+1]}")
    x -= 400
    y -= 40
    x -= 50


def generate_numbers(min_num, max_num, count, not_allowed_numbers):
    numbers = []
    for i in range(count):
        rnd_num = random.randint(min_num, max_num)
        while rnd_num in numbers or rnd_num in not_allowed_numbers:
            rnd_num = random.randint(min_num, max_num)
        numbers.append(rnd_num)
    return numbers


def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    x = 1 * inch
    y = height - 1 * inch

    numbers = generate_numbers(1000, 9999, 240, not_allowed_numbers)

    size = int(len(numbers)/2)

    for i in range(size):
        draw_number(c, numbers, i*2, x, y)
        y -= 200  # Move down for the next ticket
        if y < 1 * inch:  # Check if we need to create a new page
            c.showPage()
            y = height - 1 * inch

    c.save()


create_pdf("number-cards.pdf")
