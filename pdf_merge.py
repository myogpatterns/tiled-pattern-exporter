# pdf_merging.py

import os
from PyPDF2 import PdfFileReader, PdfFileWriter

def merge_pdfs(dir_path, output):

    pdf_writer = PdfFileWriter()

    paths = os.listdir(dir_path) 
    #print("Looking in",paths,"for PDFs")
    
    #checks if existing merged.pdf exists, if so deletes it
    if os.path.isfile(dir_path+output):
        os.remove(dir_path+output)
        print('Deleted a previous',output)

    for i in paths: 
        if i.endswith('.pdf'):
            pdf_reader = PdfFileReader(dir_path+i)
            for page in range(pdf_reader.getNumPages()):
                # Add each page to the writer object
                pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)
        print("Merged PDFs into",output)

if __name__ == '__main__':
    merge_pdfs(dir_path='pdfs/', output='pdfs/merged.pdf')