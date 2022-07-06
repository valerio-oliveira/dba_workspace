from src.report.DefaultPdfReport import DefaultPdfReport


class LogSummaryPdfReport:
    def get_pdf(hosts_summary: tuple, txt: str) -> bytearray:
        pdf = DefaultPdfReport(title="Resumo do Log de Erros")
        pdf.set_font("Times", "B", size=12)  # it is necessary to set font here

        host_count = 0
        col_strcnt = [6, 0, 8, 0, 14, 9, 18, 26]
        col_header = ["seq", "line", "count",
                      "day/time", "pid", "db", "user", "app"]
        # col_align = ["C", "C", "R",
        #              "L", "C", "L", "L", "L"]
        col = 0
        col_spaces = []
        for item in col_header:
            itemf = item + " "*(col_strcnt[col])
            if len(col_spaces) == 0:
                spc = pdf.get_string_width(itemf)
            else:
                spc = col_spaces[-1] + pdf.get_string_width(itemf)
            col_spaces.append(spc)
            col += 1

        for host_line in hosts_summary:
            pdf.add_page()

            host_name = host_line[0]
            host_ip = host_line[1]
            log_size = host_line[3]
            log_file = host_line[2]
            log_dir = host_line[4]

            LblServer1 = "Servidor: "
            LblServer2 = f"{host_name} ({host_ip})"
            LblSpace1 = "Espaço ocupado: "
            LblSpace2 = f"{log_size}"
            LblLogFile1 = "Arquivo lido: "
            LblLogFile2 = f"{log_dir}{log_file}"

            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Times", "B", size=12)
            w = 10 + pdf.get_string_width(LblSpace1)

            pdf.ln(5)

            pdf.cell(w=w, h=0, txt=LblServer1, border=0,
                     ln=0, align="L", fill=0)
            pdf.set_font("Times", size=12)
            pdf.set_x(w)
            pdf.cell(w=w, h=0, txt=LblServer2, border=0,
                     ln=0, align="L", fill=0)

            pdf.set_font("Times", "B", size=12)
            pdf.ln(5)

            pdf.cell(w=w, h=0, txt=LblSpace1, border=0,
                     ln=0, align="L", fill=0)
            pdf.set_font("Times", size=12)
            pdf.set_x(w)
            pdf.cell(w=w, h=0, txt=LblSpace2, border=0,
                     ln=0, align="L", fill=0)

            pdf.set_font("Times", "B", size=12)
            pdf.ln(5)

            pdf.cell(w=w, h=0, txt=LblLogFile1, border=0,
                     ln=0, align="L", fill=0)
            pdf.set_font("Times", size=12)
            pdf.set_x(w)
            pdf.cell(w=w, h=0, txt=LblLogFile2, border=0,
                     ln=0, align="L", fill=0)
            pdf.ln(3)

            pdf.set_font("Times", "B", size=12)
            col = 0

            for item in col_header:
                w = col_spaces[col]
                pdf.set_x(w)
                if col == 0:
                    pdf.cell(w=0, h=5, txt="", new_x="LMARGIN", new_y="NEXT")
                pdf.cell(w=w, h=0, txt=item, border=0,
                         ln=0, align="L", fill=0)
                col += 1

            pdf.set_font("Times", size=10)
            lin_list = []
            for log_line in host_line[5]:
                seq_num = f'{log_line[0]:3}'
                seq = f"{seq_num}"
                msg = f'{log_line[1]}'
                count = f'{log_line[2]}'
                line = f'{log_line[3]}'
                date = f'{log_line[4]}'.replace(
                    '-', '') if log_line[4] else f"{'':20}"
                date = date[6:8] + " " + date[9:18]

                pid = f'{log_line[5]}'
                db = f'{log_line[6]}' if log_line[6] else f"{'':10}"
                user = f'{log_line[7]}' if log_line[7] else f"{'':20}"
                app = f'{log_line[8]}' if log_line[8] else f"{'':39}"
                ip = f'{log_line[9]}' if log_line[9] else f"{'':15}"

                lin_list.append(
                    [seq, line, count, date, pid, db, user, app, msg])

            pdf.cell(w=0, h=2, txt="", new_x="LMARGIN", new_y="NEXT")
            for lin in lin_list:
                pdf.set_text_color(0, 0, 0)
                col = 0
                for item in lin:
                    if col < 8:
                        w = col_spaces[col]
                        pdf.set_x(w)
                        if col == 0:
                            pdf.cell(w=0, h=4, txt="",
                                     new_x="LMARGIN", new_y="NEXT")

                        pdf.cell(w=w, h=0, txt=item, border=0,
                                 ln=0, align='L', fill=0)
                    col += 1
                pdf.multi_cell(w=0, h=3, txt="", new_x="LMARGIN", new_y="NEXT")

                msg = lin[8]
                pdf.set_x(15)
                pdf.set_text_color(50, 50, 160)
                pdf.multi_cell(w=0, h=3, txt=msg,
                               new_x="LMARGIN", new_y="NEXT")

            host_count += 1

        return pdf.output()
