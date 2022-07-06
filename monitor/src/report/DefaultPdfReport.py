from fpdf import FPDF


class DefaultPdfReport(FPDF):
    title = ""

    def __init__(self, title=None):
        super(DefaultPdfReport, self).__init__()
        self.title = title

    def header(self):
        # Setting font: helvetica bold 15
        self.set_font('helvetica', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(self.title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        # self.set_draw_color(0, 80, 180)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(50, 50, 160)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w=w, h=9, txt=self.title, border=0, ln=1, align="C", fill=1)
        # Line break
        self.ln(5)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")
