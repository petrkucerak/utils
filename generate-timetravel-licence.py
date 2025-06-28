import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import io
import random
from unidecode import unidecode
import base64


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
    c.setFont("Helvetica-Bold", 17)
    c.drawString(x, y, "Time Travel ID")

    c.setFont("Helvetica", 15)
    y -= 25
    c.drawString(x, y, f"Identita: ")
    c.setFont("Helvetica-Bold", 20)
    x += 60
    c.drawString(x, y, f"{ticket_data['passenger_name']}")
    c.setFont("Helvetica", 15)
    x -= 60

    y -= 25
    # {ticket_data['flight_number']}")
    c.drawString(x, y, f"Jméno: __________________________ ")

    y -= 15
    # c.drawString(x, y, f"Domovský časoprostor: {ticket_data['departure']}")

    y -= 15
    # c.drawString(x, y, f"Destination: {ticket_data['destination']}")

    y -= 15
    # c.drawString(x, y, f"Date: {ticket_data['date']}")

    y -= 15
    # c.drawString(x, y, f"Boarding Time: {ticket_data['boarding_time']}")

    y -= 15
    # c.drawString(x, y, f"Gate: {ticket_data['gate']}")

    qr_code = generate_qr_code(ticket_data['qr_data'])
    c.drawImage(qr_code, x + 330, y + 40, width=1.5*inch, height=1.5*inch)

    y -= 30  # Add some space before the next ticket


def get_qr_data():
    qr_data = [
        "16. 1. 1964 - Dvacet let po tomto dnu se narodí legenda jménem Ridlas", "1. 5. 1. 1905 – V Rusku vypuká revoluce, protože někdo přelil čaj samovarem.", "12. 2. 1809 – Narodil se Abraham Lincoln. Později se ukázalo, že byl i mistrem memů.", "7. 3. 1876 – Alexander Graham Bell si patentuje telefon. Nikdo mu ale nezavolal pogratulovat.", "4. 4. 1968 – Martin Luther King Jr. byl zavražděn. Svět ztratil hlas snu.", "22. 6. 1633 – Galileo Galilei byl donucen odvolat, že se Země točí. Uvnitř ale věděl své.", "18. 7. 1925 – Hitler vydává Mein Kampf. Lidstvo má důvod k hlubokému zamyšlení.", "1. 9. 1939 – Začíná druhá světová válka. Důkaz, že lidstvo neumí vyřešit věci domluvou.", "20. 7. 1969 – První člověk přistál na Měsíci. A pak tam zapíchl vlajku.", "6. 8. 1945 – Hiroshima. Den, kdy jaderná zbraň ukázala svou tvář.", " 9. 11. 1989 – Padá Berlínská zeď. Němci si začali půjčovat cukr napříč hranicí.", " 2. 12. 1942 – Fermi spouští první řízenou jadernou reakci. A nevybouchl!", " 3. 3. 1931 – USA dostávají hymnu. A trubky konečně vědí, co mají hrát.", " 14. 4. 1912 – Titanic se potápí. Ledovec měl přednost v jízdě.", " 1. 4. 1976 – Apple byl založen. Ne, to nebyl apríl.", " 19. 4. 1995 – Bombový útok v Oklahoma City. Hrůza, kterou si USA pamatovaly dlouho.", " 16. 1. 1964 – Dvacet let po tomto dnu se narodí legenda jménem Ridlas.", " 30. 6. 1908 – Tunguská exploze. Sibiř si dala nečekané ohňostroje.", " 28. 7. 1914 – Začíná první světová válka. A nikdo nevěděl, co tím začal.", " 12. 4. 1961 – Jurij Gagarin letí do vesmíru. A z vesmíru zpět!", " 1. 12. 1989 – Václav Havel začíná mířit k Hradu. A nešel tam na výlet.", " 8. 12. 1980 – John Lennon byl zavražděn. Hudba na chvíli zmlkla.", " 10. 5. 1994 – Nelson Mandela prezidentem. Jižní Afrika slaví.", " 1. 7. 1967 – První barevné vysílání v ČSSR. A všichni chtěli nový televizor.", " 13. 3. 1781 – William Herschel objevil Uran. A děti se začaly smát jménu planety.", " 27. 3. 1998 – Microsoft koupil Hotmail. A začal spamový věk.", " 11. 9. 2001 – Útoky na WTC. Den, který změnil svět.", " 24. 8. 2006 – Pluto bylo přeřazeno na trpasličí planetu. Astronomové plakali.", " 22. 11. 1963 – JFK byl zastřelen v Dallasu. Amerika zadržela dech.", " 29. 6. 2007 – První iPhone. A lidé začali koukat dolů místo před sebe.", " 14. 7. 1789 – Dobytí Bastily. Francouzi umí slavit revoluci se stylem."]
    return random.choice(qr_data)


def get_gate_num():
    gates = ["A12", "B13"]
    return random.choice(gates)


def generate_tickets_data(path):
    tickets = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            name, id = line.split(";")
            if int(id) > 170000:
                inicials = name.split()
                name = f"{inicials[0][0]}.{inicials[1][0]}."
                code = f"{name} {id}"
            else:
                code = f"{id}"
            gate = get_gate_num()
            random = get_qr_data()
            baseString = f"{name} {id}"
            baseIn = base64.b64encode(
                baseString.encode('utf-8')).decode('ascii')
            tickets.append({
                "passenger_name": unidecode(code.replace("\n", "")).upper(),
                "flight_number": "KF927",
                "departure": "Jedlová (JFR)",
                "destination": "Ulambatar (UBN)",
                "date": "2024-06-29",
                "boarding_time": "19:30 PM",
                "gate": gate,
                "qr_data": f"{random} | {baseIn}"
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


create_pdf("timetravel-licence.pdf", "names_2025.txt")
