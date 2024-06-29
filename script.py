import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import io


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
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "Airport Ticket")

    c.setFont("Helvetica", 12)
    y -= 20
    c.drawString(x, y, f"Passenger Name: {ticket_data['passenger_name']}")

    y -= 20
    c.drawString(x, y, f"Flight Number: {ticket_data['flight_number']}")

    y -= 20
    c.drawString(x, y, f"Departure: {ticket_data['departure']}")

    y -= 20
    c.drawString(x, y, f"Destination: {ticket_data['destination']}")

    y -= 20
    c.drawString(x, y, f"Date: {ticket_data['date']}")

    y -= 20
    c.drawString(x, y, f"Boarding Time: {ticket_data['boarding_time']}")

    y -= 20
    c.drawString(x, y, f"Gate: {ticket_data['gate']}")

    qr_code = generate_qr_code(ticket_data['qr_data'])
    c.drawImage(qr_code, x + 300, y + 60, width=1.5*inch, height=1.5*inch)

    y -= 40  # Add some space before the next ticket


def create_pdf(filename, tickets):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    x = 1 * inch
    y = height - 1 * inch

    for ticket_data in tickets:
        draw_ticket(c, ticket_data, x, y)
        y -= 180  # Move down for the next ticket
        if y < 1 * inch:  # Check if we need to create a new page
            c.showPage()
            y = height - 1 * inch

    c.save()


tickets = [
    {
        "passenger_name": "Láďa Hruška",
        "flight_number": "AB123",
        "departure": "New York (JFK)",
        "destination": "London (LHR)",
        "date": "2024-07-01",
        "boarding_time": "10:00 AM",
        "gate": "A12",
        "qr_data": "John Doe, AB123, New York (JFK) -> London (LHR), 2024-07-01, 10:00 AM, Gate A12"
    },
    {
        "passenger_name": "Jane Smith",
        "flight_number": "CD456",
        "departure": "San Francisco (SFO)",
        "destination": "Tokyo (NRT)",
        "date": "2024-07-02",
        "boarding_time": "2:00 PM",
        "gate": "B34",
        "qr_data": "Jane Smith, CD456, San Francisco (SFO) -> Tokyo (NRT), 2024-07-02, 2:00 PM, Gate B34"
    },
    # Add more tickets as needed
]

create_pdf("airport_tickets.pdf", tickets)
