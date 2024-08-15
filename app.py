import io
import os.path

from pypdf import PdfReader, PdfWriter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont

font_dir_name = "fonts/"
text_font = "Consolas"
pdf_template_name = "template.pdf"
pdf_output_name = "output.pdf"
displayed_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor".upper()


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(ROOT_DIR, pdf_template_name)
FONT_PATH = os.path.join(ROOT_DIR, font_dir_name)

# Register custom font (Consolas) to ReportLib
pdfmetrics.registerFont(TTFont(text_font, FONT_PATH + f"{text_font}.ttf"))

# Create temporary PDF
packet = io.BytesIO()

doc = SimpleDocTemplate(filename=packet, pagesize=A4)

# Instantiate styling class
style = ParagraphStyle(
    name="Default",
    fontName=text_font,
    fontSize=13,
    borderColor="#000000",
    borderWidth=1,
    leading=15,
    borderPadding=20
)

# Paragraph parameters
para_pager = Paragraph(displayed_string, style=style)

# Create a vertical spacer
top_spacer = Spacer(0, 50)

# Build the document with specified flowables
doc.build([top_spacer, para_pager])

# Build the new PDF we'll be using
packet.seek(0)
new_pdf = PdfReader(packet)

# Read existing template PDF
existing_pdf = PdfReader(open(PDF_PATH, "rb"))
output = PdfWriter()

# Overlay new PDF onto template PDF
page = existing_pdf.get_page(0)
page.merge_page(new_pdf.get_page(0))
output.add_page(page)

# Save output to a file
outputStream = open(pdf_output_name, "wb")
output.write(outputStream)
outputStream.close()
