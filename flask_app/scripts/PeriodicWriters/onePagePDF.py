import PyPDF2
import csv
import sys

def addright(page, right_page, tx=0):
    page.mergeTranslatedPage(right_page, page.mediaBox[2] + tx, 0, expand=True)
    return page


def main(one, two, three):
    tx = 0
    ty = 0
    with open(one, 'rb') as input:
        pdf = PyPDF2.PdfFileReader(input)
        print("Number of Pages: %1.2i" % pdf.getNumPages())

        first_page = True
        with open(two, 'r') as f:
            reader = csv.reader(f)
            rows = []
            for row in reader:
                for page in row:
                    print("Reading page %1.2i" % int(page))
                    if first_page is True:
                        output = pdf.getPage(int(page) - 1)
                        first_page = False
                    else:
                        output = addright(output, pdf.getPage(int(page) - 1), tx)
                rows.append(output)
                first_page = True

            print("Stitching lines of pages ...")
            first_line = True
            for row in reversed(rows):
                if first_line is True:
                    output = rows[-1]
                    first_line = False
                else:
                    output.mergeTranslatedPage(row, 0, output.mediaBox[3] + ty - 14, expand=True)

        print("Saving new file...")
        with open(three, 'wb') as out_file:
            pdf_out = PyPDF2.PdfFileWriter()
            pdf_out.addPage(output)
            pdf_out.write(out_file)
    print("Finished.")
    return

if __name__ == "__main__":
    main("test.pdf", "form.csv", "output.pdf")