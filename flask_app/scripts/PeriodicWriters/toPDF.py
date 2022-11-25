from fileinput import filename
from venv import create
import pandas as pd
from fpdf import FPDF
import datetime
from math import sqrt
import re

#To-do:
# 1. Remove HTMLs from the contents of the article
# 2. Figure out multi_cell thing

#Ideas for future features:
# — Clients can choose to highlight publications
# — Pull the list of authors and parse them from the global list of publications

class PDF(FPDF):

    def rounded_rect(self, x, y, w, h, r, style = '', corners = '1234'):

        k = self.k
        hp = self.h
        if(style=='F'):
            op='f'
        elif(style=='FD' or style=='DF'):
            op='B'
        else:
            op='S'
        myArc = 4/3 * (sqrt(2) - 1)
        self._out('%.2F %.2F m' % ((x+r)*k,(hp-y)*k))

        xc = x+w-r
        yc = y+r
        self._out('%.2F %.2F l' % (xc*k,(hp-y)*k))
        if '2' not in corners:
            self._out('%.2F %.2F l' % ((x+w)*k,(hp-y)*k))
        else:
            self._arc(xc + r*myArc, yc - r, xc + r, yc - r*myArc, xc + r, yc)

        xc = x+w-r
        yc = y+h-r
        self._out('%.2F %.2F l' % ((x+w)*k,(hp-yc)*k))
        if '3' not in corners:
            self._out('%.2F %.2F l' % ((x+w)*k,(hp-(y+h))*k))
        else:
            self._arc(xc + r, yc + r*myArc, xc + r*myArc, yc + r, xc, yc + r)

        xc = x+r
        yc = y+h-r
        self._out('%.2F %.2F l' % (xc*k,(hp-(y+h))*k))
        if '4' not in corners:
            self._out('%.2F %.2F l' % (x*k,(hp-(y+h))*k))
        else:
            self._arc(xc - r*myArc, yc + r, xc - r, yc + r*myArc, xc - r, yc)

        xc = x+r
        yc = y+r
        self._out('%.2F %.2F l' % (x*k,(hp-yc)*k))
        if '1' not in corners:
            self._out('%.2F %.2F l' % (x*k,(hp-y)*k))
            self._out('%.2F %.2F l' % ((x+r)*k,(hp-y)*k))
        else:
            self._arc(xc - r, yc - r*myArc, xc - r*myArc, yc - r, xc, yc - r)
        self._out(op)


    def _arc(self, x1, y1, x2, y2, x3, y3):

        h = self.h
        self._out('%.2F %.2F %.2F %.2F %.2F %.2F c ' % (x1*self.k, (h-y1)*self.k,
                                                        x2*self.k, (h-y2)*self.k, x3*self.k, (h-y3)*self.k))

class pdfReport:
    def __init__(self, df=None, filename=None, list=None, unsub_link=None):
        if (df is None and filename is None):
            raise Exception("Must provide either a dataframe or a filename")
        elif (df is None):
            try:
                self.df = pd.read_csv(filename)
            except:
                raise Exception("Could not read file")
        elif (df is not None):
            self.df = df

        self.list = list
        self.unsub_url = unsub_link

    def show_df(self):
        return self.df

    def remove_urls(self, text):
        return re.sub(r"http\S+", "", text)
        # return text

    def remove_linebreaks(self, text):
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        return text



    def make_PDF(self, filename=None, fileDimentions=(210, 297)):
        df = self.df
        pdf = PDF(format=fileDimentions)
        pdf.add_page()
        pdf.set_fill_color(246, 246, 246)
        pdf.set_margins(left=25, top=0)
        pdf.add_font('Trebuchet', '', 'assets/Trebuchet MS.ttf', uni=True)
        pdf.add_font('Trebuchet', 'B', 'assets/Trebuchet MS Italic.ttf', uni=True)
        pdf.set_auto_page_break(auto=True, margin=0)

        #group df by name
        grouped = df.groupby("Name", sort=True)
        pdf.image('assets/logo.png', x=12, y=10, w=23, h=22)
        pdf.set_font('Trebuchet', 'B', 15)
        pdf.cell(w=0, h=40, txt='', new_x="LMARGIN", new_y="NEXT", align='L')
        for name, name_df in grouped:
            # add name as header
            pdf.set_font('Trebuchet', 'B', 15)
            pdf.cell(w=0, h=5, txt=name, new_x="LMARGIN", new_y="NEXT", align='L')
            name_df = name_df.drop_duplicates(subset="Headline", keep="first")
            pdf.ln(5)

            for index, row in name_df.iterrows():
                pdf.set_text_color(0, 0, 0)
                padding = ' ' * 4
                #add a filled empty line
                pdf.cell(w=0, h=4, txt='', new_x="LMARGIN", new_y="NEXT", align='L', fill=True)

                text = row["Headline"]
                if(len(text) > 70):
                    text = text[:70] + "..."
                text = padding + text
                link = row["Link"]
                link = link.encode('latin-1', 'ignore').decode('latin-1')
                try:
                    text_final = text.encode('latin-1', 'ignore').decode('latin-1')
                except:
                    text_final = ''

                pdf.set_font('Trebuchet', '', 12)
                pdf.multi_cell(w=0, h=5, txt=text_final, align='L', fill=True, new_x="LMARGIN", new_y="NEXT",
                               link=link)
                pdf.cell(w=0, h=1, txt='', new_x="LMARGIN", new_y="NEXT", align='L', fill=True)



                date = row["Date"]
                date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%B %d, %Y")
                media = row["Media"]
                combined = padding + ' ' + date + " | " + media
                combined = combined.encode('latin-1', 'ignore').decode('latin-1')
                pdf.set_font('Trebuchet', '', 10)
                pdf.set_text_color(146, 146, 146)
                pdf.cell(w=0, h=5, txt=combined, new_x="LMARGIN", new_y="NEXT", align='L', fill=True)


                pdf.set_text_color(65, 65, 65)
                #full_text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies, purus lectus malesuada libero, sit amet commodo magna eros quis urna. Nunc viverra imperdiet enim. Fusce est. Vivamus a tellus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Proin pharetra nonummy pede. Mauris et orci. Aenean nec lorem. In porttitor. Donec laoreet nonummy augue."
                full_text = row["Coverage"]
                full_text = full_text.encode('latin-1', 'ignore').decode('latin-1')
                try:
                    full_text = self.remove_urls(full_text)
                    full_text = self.remove_linebreaks(full_text)
                except:
                    pass
                split_text = []
                while len(full_text) > 0:
                    if len(full_text) > 90:
                        last_space = full_text[:90].rfind(' ')
                        if(last_space == -1 or last_space < 50):
                            last_space = 90
                        split_text.append(full_text[:last_space])
                        full_text = full_text[last_space:]
                    else:
                        split_text.append(full_text)
                        full_text = ''

                for i in range(len(split_text)):
                    pdf.set_font('Trebuchet', '', 10)
                    text = padding + split_text[i]
                    if(i == 0):
                        text = ' ' + text #Padding for the beginning, it's dumb, but it works, sorry
                    pdf.multi_cell(w=0, h=3.5, txt=text, align='L', fill=True, new_x="LMARGIN", new_y="NEXT")

                pdf.cell(w=0, h=4, txt='', new_x="LMARGIN", new_y="NEXT", align='L', fill=True)
                pdf.ln(5)
            pdf.ln(10)

        return pdf, pdf.page_no()


    def createOnePagePdf(self, num_pages=1, filename=None):
        pdf, _ = self.make_PDF(fileDimentions=(210, 297 * num_pages))
        pdf.output(filename)

    def create_PDF(self, filename):
        _, num_pages = self.make_PDF()
        self.createOnePagePdf(num_pages=num_pages, filename=filename)


if __name__ == "__main__":
    test = pdfReport(filename='test.csv')
    test.create_PDF('test.pdf')
