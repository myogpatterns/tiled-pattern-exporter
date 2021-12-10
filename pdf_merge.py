#--------------------------------------------------------------
#   pdf_merge.py
#
#   Created for LearnMYOG.com
#   Merges all pdf files in dir_path into one pdf file
#   
#--------------------------------------------------------------

import os, time
from PyPDF2 import PdfFileReader, PdfFileWriter

def merge_pdfs(dir_path, output):
    timestr = str('D:' + time.strftime("%Y%m%d%H%M%S"))

    pdf_writer = PdfFileWriter()

    #checks if existing merged.pdf exists, if so deletes it
    if os.path.isfile(dir_path+output):
        os.remove(dir_path+output)
        print('Deleted a previous',output)

    paths = sorted(os.listdir(dir_path))
    #print("Looking in",paths,"for PDFs")
    
    for i in paths: 
        if i.endswith('.pdf'):
            pdf_reader = PdfFileReader(dir_path+i)
            for page in range(pdf_reader.getNumPages()):
                # Add each page to the writer object
                pdf_writer.addPage(pdf_reader.getPage(page))
                pdf_writer.addMetadata({
                    '/Author': 'Tim @ LearnMYOG.com',
                    '/CreationDate': timestr,
                    '/Producer': 'https://github.com/myogpatterns/tiled-pattern-exporter'
                })

    # Write out the merged PDF
    with open(dir_path+output, 'wb') as out:
        pdf_writer.write(out)
        #print("Merged PDFs into",dir_path+output)

if __name__ == '__main__':
    merge_pdfs(dir_path='pdfs/', output='merged.pdf')