#--------------------------------------------------------------
#   pattern_exporter.py
#
#   Created for LearnMYOG.com
#   Automates creation of PDF pattern sheets from Inkscape PNG export
#   From large format PNG create A0, tabloid/A3 and letter/A4 merged patternsl
#   
#   use python3 pattern_exporter.py input.png output.pdf format=(letter, tabloid, a0)
#
#   1. Export PNG with size in multiple of 7.5 inches wide and 10 inches tall @ 300dpi.
#   2. Tile huge PNG into pattern-#.pngs with image_tiler.py
#   3. Convert pattern-#.pngs to PDFs with image_conv_pdf.py, saves into /pdfs/
#   Add page numbers, copyright, cut registration, and alignment aids
#   4. Merge individual pdfs using pdf_merge.py
#   
#   Add argparse for automated help
#
#--------------------------------------------------------------

import sys, os, shutil, string, time
from image_tiler import image_tiler
from image_conv_pdf import image_conv_pdf
from pdf_merge import merge_pdfs

start_time = time.time()


def pattern_exporter(input_png, output_pdf, format):

    # Set variables
    if len(sys.argv) > 1:
        input_png = sys.argv[1]
        output_pdf = sys.argv[2]
        format = sys.argv[3]
    
    dir_path = 'pdfs/'
    
    
    # 1 check if pattern.PNG exists, create or cleanup dir_paths folder

    if os.path.exists(input_png):
        if os.path.exists(dir_path):
            try:
                for i in os.listdir(dir_path):
                    os.remove(dir_path+i)
            except OSError as e:
                print("Error: %s : %s" % (dir_path, e.strerror))
        else: 
            os.mkdir(dir_path)
        print("Preparing", dir_path)
    else:
        print(input_png,"does not exist in",os.path.abspath('.'))
        exit()

    # 2 tile PNG with image_tiler.py --- Letter / A4

    image_tiler(
        input_png, 
        format, 
        dir_path)

    # 3 convert individual PNGs to PDFs

    image_conv_pdf(dir_path)
   
    # 4 merge the individual PDFs with pdf_merge.py

    merge_pdfs(
        dir_path, 
        'merged.pdf')

    # 5 final output file named and copied to base directory
    timestr = time.strftime("%Y%m%d")
    output_pdf = 'PatternSheets_'+format+'_'+timestr+'.pdf'
    shutil.copy(dir_path+'merged.pdf',output_pdf)
    print()
    print(">>>>>>>>> Created:" + output_pdf)

    print()
    print("--- %s seconds elapsed---" % (time.time() - start_time))

if __name__ == '__main__':
    pattern_exporter(
        input_png='pattern.png', 
        output_pdf='patternSheets.pdf',
        format='tabloid')