from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

LINE_HEIGHT = 12
BOTTOM_MARGIN = 50
TOP_MARGIN = 80
SIDE_MARGIN = 50
BULLET_INDENT = 20


def _draw_paragraph(c, content, x, y, text_width, width, height):
    words = content.split()
    line = ""
    for word in words:
        test_line = line + word + " " if line else word + " "
        if c.stringWidth(test_line, "Helvetica", 10) <= text_width:
            line = test_line
        else:
            if y < BOTTOM_MARGIN + LINE_HEIGHT:
                c.showPage()
                y = height - LINE_HEIGHT
            c.drawString(x, y, line.rstrip())
            y -= LINE_HEIGHT
            line = word + " "
    if line:
        if y < BOTTOM_MARGIN + LINE_HEIGHT:
            c.showPage()
            y = height - LINE_HEIGHT
        c.drawString(x, y, line.rstrip())
        y -= LINE_HEIGHT
    return y


def generate_pdf(content, as_bullets=False):
    pdf_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
        prefix="lecture_"
    )
    pdf_path = pdf_file.name
    pdf_file.close()

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    text_width = width - 2 * SIDE_MARGIN - (BULLET_INDENT if as_bullets else 0)

    c.setFont("Helvetica", 16)
    c.drawString(SIDE_MARGIN, height - 50, "Lecture Transcript")

    c.setFont("Helvetica", 10)
    y = height - TOP_MARGIN

    if as_bullets:
        bullet_x = SIDE_MARGIN
        text_x = SIDE_MARGIN + BULLET_INDENT
        bullet_text_width = width - 2 * SIDE_MARGIN - BULLET_INDENT
        for line in content.split("\n"):
            line = line.strip()
            if not line:
                continue
            if y < BOTTOM_MARGIN + LINE_HEIGHT:
                c.showPage()
                y = height - LINE_HEIGHT
            c.drawString(bullet_x, y, "-")
            y = _draw_paragraph(c, line, text_x, y, bullet_text_width, width, height)
            y -= 4
    else:
        full_width = width - 2 * SIDE_MARGIN
        _draw_paragraph(c, content, SIDE_MARGIN, y, full_width, width, height)

    c.save()
    return pdf_path
