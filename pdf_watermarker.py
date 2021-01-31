# pdf_watermarker.py
# Save a PDF from Inkscape using individual page sizes of 7.5 x 10 "postered.pdf"
# Print to PDF from Acrobat Reader so centered on 8.5 x 11 "posteredLet.pdf"
# Watermark using watermark pdf "watermarked_postered.pdf"

from PyPDF2 import PdfFileWriter, PdfFileReader

def create_watermark(input_pdf, output, watermark):

    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(input_pdf, strict=False)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for pg in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(pg)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output, 'wb') as out:
        pdf_writer.write(out)
        print("Pattern exported",output)

if __name__ == '__main__':
    create_watermark(
        input_pdf='pdfs/merged.pdf', 
        output='patternSheets.pdf',
        watermark='watermark.pdf')