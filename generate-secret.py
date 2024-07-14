import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit

tymy = ["cerni", "cerveni", "zluti", "modri", "tyrkysovi", "zeleni", "ruzovi"]

# Funkce pro odstranění diakritiky a převedení na malá písmena


def normalize_text(text):
    replacements = (
        ("á", "a"), ("č", "c"), ("ď", "d"), ("é", "e"), ("ě", "e"),
        ("í", "i"), ("ň", "n"), ("ó", "o"), ("ř", "r"), ("š", "s"),
        ("ť", "t"), ("ú", "u"), ("ů", "u"), ("ý", "y"), ("ž", "z"),
        ("Á", "a"), ("Č", "c"), ("Ď", "d"), ("É", "e"), ("Ě", "e"),
        ("Í", "i"), ("Ň", "n"), ("Ó", "o"), ("Ř", "r"), ("Š", "s"),
        ("Ť", "t"), ("Ú", "u"), ("Ů", "u"), ("Ý", "y"), ("Ž", "z")
    )
    for a, b in replacements:
        text = text.replace(a, b).replace(a.upper(), b)
    return text.lower()

# Funkce pro vytvoření náhodného šifrovacího klíče


def generate_cipher_key():
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    shuffled = alphabet[:]
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))


def draw_ticket(c, key, x, y):
    y -=30
    c.setFont("Helvetica-Bold", 40)
    c.drawString(x, y, key)
    y -= 30  # Add some space before the next ticket

# Funkce pro zašifrování textu pomocí šifrovacího klíče


def encrypt_text(text, cipher_key):
    return ''.join(cipher_key.get(char, char) for char in text)

# Funkce pro rozdělení textu na řádky, které se vejdou na šířku stránky


def split_text_to_lines(text, max_width, canvas, font_name="Helvetica", font_size=14):
    canvas.setFont(font_name, font_size)
    return simpleSplit(text, font_name, font_size, max_width)

# Funkce pro vytvoření PDF s textem a šifrovacím klíčem


def create_pdf(sentences, filename="encrypted_texts.pdf"):
    # Generování šifrovacího klíče
    cipher_key = generate_cipher_key()

    # Vytvoření PDF
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    left_margin = 100
    top_margin = 100
    line_height = 26  # Zvýšení výšky řádku pro větší text
    max_width = width - 2 * left_margin
    font_name = "Helvetica"
    font_size = 20

    # Přidání zašifrovaných textů
    for i, text in enumerate(sentences):
        # Normalizujeme text
        normalized_text = normalize_text(text)

        # Zašifrujeme text
        encrypted_text = encrypt_text(normalized_text, cipher_key)

        # Rozdělíme zašifrovaný text na řádky
        lines = split_text_to_lines(
            encrypted_text, max_width, c, font_name, font_size)

        # Přidání zašifrovaného textu na stránku
        c.setFont(font_name, font_size)
        c.drawString(left_margin, height - top_margin, f"Tým {tymy[i]}:")
        for j, line in enumerate(lines):
            c.drawString(left_margin, height - top_margin -
                         line_height * (j + 2), line)

      #   # Přidáme dešifrovací klíč na poslední stránku
      #   if i == len(sentences) - 1:
      #       c.showPage()
      #       c.setFont(font_name, font_size)
      #       c.drawString(left_margin, height - top_margin, "Cipher Key:")
      #       for k, (plain, cipher) in enumerate(cipher_key.items()):
      #           c.drawString(left_margin, height - top_margin - line_height * (k + 2), f"{plain} -> {cipher}")

        # Přechod na další stránku, pokud to není poslední věta
        if i != len(sentences) - 1:
            c.showPage()

    # Uložíme PDF
    c.save()

    c = canvas.Canvas("cipher.pdf", pagesize=A4)
    width, height = A4

    x = 1 * inch
    y = height - 1 * inch

    for k, (plain, cipher) in enumerate(cipher_key.items()):
        draw_ticket(c, f"{plain.upper()} -> {cipher.upper()}", x, y)
        y -= 150  # Move down for the next ticket
        if y < 1 * inch:  # Check if we need to create a new page
            c.showPage()
            y = height - 1 * inch

    c.save()


# Vstupní věty
sentences = [
    "Vyfoťte se s dětským banjem, je k dostání na srubu číslo dvacet. Fotku udělejte u kapličky a pošlete ji Ridlasovi.",
    "Vyfoťte se s ozvučnými dřívky, jsou k dostání na srubu číslo dvacet. Fotku udělejte u kapličky a pošlete ji Ridlasovi.",
    "Vyfoťte se s tamburínou, je k dostání na srubu číslo dvacet. Fotku udělejte u kapličky a pošlete ji Ridlasovi.",
    "Vyfoťte se s xylofonem, je k dostání na srubu číslo dvacet. Fotku udělejte u kapličky a pošlete ji Ridlasovi.",
    "Vyfoťte se s rumba koulemi, je k dostání na srubu číslo dvacet. Fotku udělejte u koupaliště a pošlete ji Ridlasovi.",
    "Vyfoťte se se zelenými chůdami, je k dostání na srubu číslo dvacet. Fotku udělejte u koupaliště a pošlete ji Ridlasovi.",
    "Vyfoťte se s červenými chůdami, je k dostání na srubu číslo dvacet. Fotku udělejte u koupaliště a pošlete ji Ridlasovi."
]

# Vytvoření PDF
create_pdf(sentences)
