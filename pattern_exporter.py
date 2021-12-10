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
from pattern_tile import pattern_tile
from pdf_merge import merge_pdfs

start_time = time.time()


def pattern_exporter(input_png):

    # Set variables
    if len(sys.argv) > 1:
        input_png = sys.argv[1]
        #format = sys.argv[2]
    
    dir_path = 'pdfs/'
    
    
    # 1 check if pattern.PNG exists, create or cleanup dir_paths folder

    if os.path.exists(input_png):
        prepare_temp_dir(dir_path)
        
    else:
        print(input_png,"does not exist in ",os.path.abspath('.'))
        exit()


    # 2 convert individual PNGs to PDFs
    formats = ['letter','tabloid','a0']
    for f in formats:
        print("Working on",f,"pattern sheets.")
        pattern_tile(input_png, f, dir_path)

   
        # 4 merge the individual PDFs with pdf_merge.py
        merged_temp = f + 'merged.pdf'
        merge_pdfs(
            dir_path, 
            merged_temp)

        # 5 final output file named and copied to base directory
        timestr = time.strftime("%Y%m%d")
        output_pdf = 'LearnMYOG_Pattern_'+ f + '_' + timestr + '.pdf'
        shutil.copy(dir_path + merged_temp, output_pdf)
        print()
        print(">>>>>>>>> Created: " + output_pdf +" <<<<<<<<<")

        prepare_temp_dir(dir_path)  # clean up after yourself

        print()
        print("--- %s seconds elapsed---" % (time.time() - start_time))



#### HELPER FUNCTIONS ####

def prepare_temp_dir(dir_path):
    if os.path.exists(dir_path):
        try:
            for i in os.listdir(dir_path):
                os.remove(dir_path+i)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
    else: 
        os.mkdir(dir_path)



if __name__ == '__main__':
    pattern_exporter(
        input_png='pattern.png')