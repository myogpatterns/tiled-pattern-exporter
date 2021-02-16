# Tile Pattern Exporter
Created for LearnMYOG.com<br>

## Automates creation of PDF pattern sheets from Inkscape PNG export  

1. Export PNG with size in multiple of 7.5 inches wide and 10 inches tall @ 300dpi.
1. Tile huge PNG into pattern-#.pngs with image_tiler.py
1. Convert pattern-#.pngs to PDFs with image_conv_pdf.py, saves into /pdfs/
1. Merge individual pdfs using pdf_merge.py
1. Watermark cut lines with pdf_watermarker.py