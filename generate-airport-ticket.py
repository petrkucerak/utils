import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import io
import random
from unidecode import unidecode


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return ImageReader(img_byte_arr)


def draw_ticket(c, ticket_data, x, y):
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Airport Ticket")

    c.setFont("Helvetica", 11)
    y -= 15
    c.drawString(x, y, f"Passenger Name: ")
    c.setFont("Helvetica-Bold", 13)
    x += 93
    c.drawString(x, y, f"{ticket_data['passenger_name']}")
    c.setFont("Helvetica", 11)
    x -= 93

    y -= 15
    c.drawString(x, y, f"Flight Number: {ticket_data['flight_number']}")

    y -= 15
    c.drawString(x, y, f"Departure: {ticket_data['departure']}")

    y -= 15
    c.drawString(x, y, f"Destination: {ticket_data['destination']}")

    y -= 15
    c.drawString(x, y, f"Date: {ticket_data['date']}")

    y -= 15
    c.drawString(x, y, f"Boarding Time: {ticket_data['boarding_time']}")

    y -= 15
    c.drawString(x, y, f"Gate: {ticket_data['gate']}")

    qr_code = generate_qr_code(ticket_data['qr_data'])
    c.drawImage(qr_code, x + 330, y + 10, width=1.5*inch, height=1.5*inch)

    y -= 30  # Add some space before the next ticket


def get_qr_data():
    qr_data = ["Raději bych nenastupoval", "Ulambátar", "Už se těším na dovolenou", "Co kdybychom to letadlo unesli?",
               "Mám hlad", "Ridlas si nechá narůst vlasy", "Co když to letadlo vzplane?", "Vysočany - můj ideál",
               "Dej si lentilku, kámo", "Kajak, ten bych chtěl řídit", "Co když se naše letadlo srazí s ptákem?",
               "Co když má někdo na palubě bombu?", "Ta slečne předemnou je fakt sexy",
               "Když se spojí golf a hojek bude z toho golfhokej"]
    return random.choice(qr_data)


def get_gate_num():
    gates = ["A12", "B13"]
    return random.choice(gates)


def generate_tickets_data(path):
    tickets = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for name in lines:
            gate = get_gate_num()
            random = get_qr_data()
            tickets.append({
                "passenger_name": unidecode(name.replace("\n", "")).upper(),
                "flight_number": "KF927",
                "departure": "Jedlová (JFR)",
                "destination": "Ulambatar (UBN)",
                "date": "2024-06-29",
                "boarding_time": "19:30 PM",
                "gate": gate,
                "qr_data": f"{random} | {name}, AB123, Jedlová (JFR) -> Ulambátar (UBN), 2024-06-29, 19:30 AM, Gate {gate}"
            })
    return tickets


def create_pdf(filename, input_path):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    x = 1 * inch
    y = height - 1 * inch

    tickets = generate_tickets_data(input_path)
    # print(tickets)

    for ticket_data in tickets:
        draw_ticket(c, ticket_data, x, y)
        y -= 150  # Move down for the next ticket
        if y < 1 * inch:  # Check if we need to create a new page
            c.showPage()
            y = height - 1 * inch

    c.save()


create_pdf("airport_tickets.pdf", "names.txt")
