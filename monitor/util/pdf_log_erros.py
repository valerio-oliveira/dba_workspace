from fpdf import FPDF


class PDF(FPDF):
    title = "Resumo dos Logs de Erros"

    def header(self):
        #     # Rendering logo:
        #     # self.image("../docs/fpdf2-logo.png", 10, 8, 33)
        #     # Setting font: helvetica bold 15
        #     self.set_font("helvetica", "B", 15)
        #     # Moving cursor to the right:
        #     self.cell(80)
        #     # Printing title:
        #     self.cell(30, 10, title, border=0, align="C")
        #     # Performing a line break:
        #     self.ln(20)
        # Arial bold 15
        self.set_font('helvetica', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(PDF.title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, PDF.title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    # def chapter_body(self, name):
    #     # Read text file
    #     with open(name, 'rb') as fh:
    #         txt = fh.read().decode('utf-8')
    #     # Times 12
    #     self.set_font('Times', '', 12)
    #     # Output justified text
    #     self.multi_cell(0, 5, txt)
    #     # Line break
    #     self.ln()
    #     # Mention in italics
    #     self.set_font('', 'I')
    #     self.cell(0, 5, '(end of excerpt)')

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")


class reports:
    def GetSummaryPdf(hosts_summary: tuple, txt: str):
        host_count = 0
        col_width = 100

        pdf = PDF()
        for host_line in hosts_summary:
            pdf.add_page()
            pdf.set_font("Times", "B", size=12)

            host_name = host_line[0]
            host_ip = host_line[1]
            log_size = host_line[3]
            log_file = host_line[2]
            log_dir = host_line[4]

            header1 = f"Servidor\t\t\t\t\t: {host_name} ({host_ip})"
            header2 = f"Esaço ocupado\t: {log_size}"
            header3 = f"Arquivo lido\t: {log_dir}{log_file}"

            pdf.cell(0, 5, header1, new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 5, header2, new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 5, header3, new_x="LMARGIN", new_y="NEXT")

            col_header = ["seq", "line", "count",
                          "day/time", "pid", "db", "user", "app"]
            hor = 0
            ver = 5
            for item in col_header:
                pdf.cell(0, ver, item, new_x=hor, new_y="NEXT")
                hor = hor + col_width
                ver = 0

            lin_list = []
            for log_line in host_line[5]:
                seq_num = f'{log_line[0]:3}'
                seq = f"{seq_num}"
                msg = f'{log_line[1]}'
                count = f'{log_line[2]}'
                line = f'{log_line[3]}'
                date = f'{log_line[4]}'.replace(
                    '-', '') if log_line[4] else f"{'':20}"
                pid = f'{log_line[5]}'
                db = f'{log_line[6]}' if log_line[6] else f"{'':10}"
                user = f'{log_line[7]}' if log_line[7] else f"{'':20}"
                app = f'{log_line[8]}' if log_line[8] else f"{'':39}"
                ip = f'{log_line[9]}' if log_line[9] else f"{'':15}"

                lin_list.append([seq, line, count, date[6:8],
                                date[9:18], pid, db, user, app])
                # pdf.set_font("Times", size=12)
                # pdf.cell(0, 5, detail1, new_x="LMARGIN", new_y="NEXT")

                # detail2 = f"    {msg}"
                # pdf.set_font("Times", size=10)
                # pdf.cell(0, 5, detail2, new_x="LMARGIN", new_y="NEXT")

            for lin in lin_list:
                hor = 0
                ver = 5
                for item in lin:
                    pdf.cell(0, ver, item, new_x=hor, new_y="NEXT")
                    hor = hor + col_width
                    ver = 0

            host_count += 1
        # txt = txt+".pdf"
        return pdf.output()
