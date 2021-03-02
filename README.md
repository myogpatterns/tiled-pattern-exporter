# Tile Pattern Exporter
Created for LearnMYOG.com<br>
This set of scripts automate the tiling of large format PNG files into letter sized PDF pages with print margins and can add cut registration marks with a watermark.pdf common to every page.   

1. Input an exported PNG with size in multiples of 7.5 inches wide and 10 inches tall @ 300dpi.
1. Tile huge PNG into pattern-#.pngs with image_tiler.py
1. Convert pattern-#.pngs to PDFs with image_conv_pdf.py, saves into /pdfs/
1. Merge individual pdfs using pdf_merge.py
1. Watermark cut lines with pdf_watermarker.py

## Dependencies
1. Imagemagick https://imagemagick.org/index.php
1. Wand https://docs.wand-py.org/en/0.6.6/
1. Pillow https://pypi.org/project/Pillow/
1. Py2PDF2 https://pypi.org/project/PyPDF2/

##   Use
1.   Place exported PNG in script directory
1.   Execute with the following command:

`python3 pattern_exporter.py 'input_file.png' 'output_file.pdf'`

## Desired improvements
1. Remove Imagemagick and Wand dependency without losing pdf conversion quality
1. Accept PNG files with different resolutions
1. Find workaround for Image.MAX_IMAGE_PIXELS = None
1. Implement basic UI