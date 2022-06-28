import pandas as pd
from fpdf import FPDF

#Ideas for future features:
# — Clients can choose to highlight publications
# — Pull the list of authors and parse them from the global list of publications

class PDF(FPDF):
    def header(self):
        self.image('logo.png', x=10, y=10, w=26, h=8)
        self.set_font('Times', 'B', 16)
        self.cell(80)
        self.cell(30, 10, 'Weekly Media Analysis', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Print centered page number
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

class pdfReport:
    def __init__(self, df=None, filename=None, list=None, unsub_link=None):
        if(df is None and filename is None):
            raise Exception("Must provide either a dataframe or a filename")
        elif(df is None):
            try:
                self.df = pd.read_csv(filename)
            except:
                raise Exception("Could not read file")
        elif(df is not None):
            self.df = df

        self.list = list
        self.unsub_url = unsub_link
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.image('logo.png', x=10, y=10, w=26, h=8)
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(w=0, h=10, txt='Muckrack Weekly Analysis', ln=1, align='C')


    def show_df(self):
        return self.df

    def create_PDF(self, filename=None):
        df = self.df

        pdf = PDF()
        pdf.add_page()
        #group df by name
        grouped = df.groupby("Name", sort=True)
        for name, name_df in grouped:
            #add name as header
            pdf.set_font('Times', 'B', 14)
            pdf.cell(w=0, h=10, txt=name, ln=1, align='C')

            for index, row in name_df.iterrows():
                #pass
            # for i in range(len(df)):
            #     if(df["Name"][i] == name):
                    #READ IT:
                    #ADD LATER WHEN IMPLEMENTING PERSONALIZATION:
                    #To if statement above: "and name in list_of_authors"


                media = "Media:"
                pdf.set_font('Times', 'B', 12)
                pdf.cell(w=0, h=5, txt=media, ln=1, align='L')
                media = row["Media"]
                pdf.set_font('Times', '', 12)
                pdf.cell(w=0, h=5, txt=media, ln=1, align='L')
                media = "Publication:"
                pdf.set_font('Times', 'B', 12)
                pdf.cell(w=0, h=5, txt=media, ln=1, align='L')
                media = row["Date"]+"\n"
                pdf.set_font('Times', '', 12)
                pdf.cell(w=0, h=5, txt=media, ln=1, align='L')
                media = "Headline:"
                pdf.set_font('Times', 'B', 12)
                pdf.cell(w=0, h=5, txt=media, ln=1, align='L')
                text = row["Headline"] + "\n\n"
                link = row["Link"]
                text_final = text.encode('latin-1', 'replace').decode('latin-1')
                pdf.set_font('Times', '', 12)
                pdf.cell(w=0, h=5, txt=text_final, ln=1, align='L', link=link)
                pdf.cell(w=0, h=5, txt="\n", ln=1, align='L')

        pdf.set_font('Times', '', 14)
        pdf.set_text_color(240,76,35)
        pdf.ln(20)
        pdf.cell(w=0, h=5, txt='Click here to unsubscribe.', align='C', link=self.unsub_url)
        pdf.output(filename, 'F')



if __name__ == "__main__":
    test = pdfReport(filename='muckrack_analysis.csv')
    test.create_PDF(filename='muckrack_analysis.pdf')





