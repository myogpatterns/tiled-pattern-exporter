# Tile Pattern Exporter
Created for LearnMYOG.com<br>
This set of scripts automate the tiling of large format PNG files into letter(A4), tabloid(A3), and A0 sized PDF pages with print margins, alignment and cut guides, page numbers, and a copyright stamp to each page.   

For best results, input an exported PNG with size in multiples of 7.5 inches wide and 10 inches tall @ 300dpi.

## Dependencies
1. Imagemagick https://imagemagick.org/index.php
1. Wand https://docs.wand-py.org/en/0.6.7/
1. PyPDF2 https://pypi.org/project/PyPDF2/

##   Use
1.   Place exported PNG in script directory
1.   Execute with the following command:

`python3 pattern_exporter.py 'input_file.png' [format = 'letter','tabloid','a0', 'all' (default)]`

## Desired improvements
1. Implement basic UI


Good readme
1 Title
# Title
## Subtitle 

2 Paragraph Explanation and problem it solves (SEO keywords)

3 Visual helper
Youtube demo if applicable

4 User installation instructions

5 Contributor instructions (build and install) and how to work on it

6 Expectations for contributors
Invite to submit issue or submit a PR for features

7 Known issues, coming soon

8 Donation link, buy me a coffee