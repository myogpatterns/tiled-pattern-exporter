#--------------------------------------------------------------
#   pattern_tile.py
#
#   Created for LearnMYOG.com
#   Automates creation of PDF pattern sheets from Inkscape PNG export
#   From large format PNG create A0, tabloid/A3 and letter/A4 merged patterns
# 
#   Tiles, adds cut registration, alignment guides, and converts to PDF
#   Wand requires imagemagick to be installed locally
#   https://imagemagick.org/script/download.php
#   
#   import.png must be 300dpi and sized a multiple of 7.5 in wide by 10 in tall
#
#
#--------------------------------------------------------------


import os, glob
from wand.image import Image, Color
from wand.drawing import Drawing
import wand.display 



def pattern_tile(import_png, format, dir_path):

    # formats accepted
    format = format.lower() #make case-insensitive

    if (format == 'letter'):
        tile_width = 7.5
        tile_height = 10
        guides_png = 'guides/cut_guides_letter.png'
    elif (format == 'tabloid'):
        tile_width = 15
        tile_height = 10
        guides_png = 'guides/cut_guides_tabloid.png'
    elif (format == 'a0'):
        tile_width = 45
        tile_height = 30
        guides_png = None
    else:
        print("Format must be letter, tabloid, or a0. Case sensitive.")
        exit()

    
    # constants
    ppi = 300
    ppi_width = round(tile_width * ppi)
    ppi_height = round(tile_height * ppi)
    
    
    #### Full size Exported PNG operations ####

    # open the import_png
    with Image(filename=import_png) as img:
        img.units='pixelsperinch'
        img.resolution=300
        print(import_png +' is ' + str(img.width/ppi) + ' by '+ str(img.height/ppi) + ' at ' + str(img.resolution[0]) + ' ' + img.units)


        #### Alignment Guides ####
        if guides_png:
            with Image(filename=guides_png) as guides:
                img.composite(guides, left=0, top=0)


        #### Tile Img ####
        currentx = 0
        currenty = 0
        
        i=1
        
        while currenty < img.height:
            while currentx < img.width:
                with img.clone() as cloned:
                    cloned.crop(left=currentx, top=currenty, width= ppi_width, height= ppi_height)
                    tile_id = dir_path + os.path.splitext(import_png)[0] + "-" + str(i).zfill(2) +".png"
                    cloned.save(filename=tile_id)
                currentx += ppi_width
                i+=1
            currenty += ppi_height
            currentx = 0
        print("Tiled",i-1,format,"pattern sheets")
        

    #### Single Tile Operations ####
    
    # add tiled pngs into a list
    if glob.glob(dir_path+'*-*.png'): 
        png_list = sorted(glob.glob(dir_path+'*-*.png'))

    
    pg_num = 1

    for i in png_list:

        with Image(filename=i) as img:
            img.units = 'pixelsperinch'
            img.resolution = 300

            # remove alpha channel and fill white
            if img.alpha_channel:
                print("Removing alpha channel from ",i)
                img.alpha_channel = 'remove' #close alpha channel   
                img.background_color = Color('white')
                #img.save(filename=new_image_path)

            # Add border 0.5 in = 150/300
            img.border('white', 150, 150)

                
            # Add lines and texts
            with Drawing() as draw:
                # cut registration lines 
                draw.push()
                draw.stroke_color = Color('grey50')
                draw.stroke_width = 3
                draw.fill_opacity = 0
                draw.path_start()
                draw.path_move(to=(img.width,150)) #top
                draw.path_horizontal_line(1)
                draw.path_move(to=(150,img.height)) #left
                draw.path_vertical_line(1)
                draw.path_move(to=(img.width,img.height-150)) #bottom
                draw.path_horizontal_line(1)
                draw.path_move(to=(img.width-150,img.height)) #right
                draw.path_vertical_line(1)
                draw.path_close()
                draw.path_finish()
                draw.pop()

                

                # texts
                draw.push()
                draw.font_size = 32
                draw.text_alignment='center'
                draw.fill_color = Color('grey50') 
                draw.font_family = "Arial"
                draw.text(int(img.width/2), int(img.height-100),"2021 © LearnMYOG.com")
                draw.text(int(img.width-100), int(img.height-100),str(pg_num))
                draw(img)
                draw.pop()

            # Convert to PDF
            with img.convert('pdf') as converted:
                fileout = os.path.splitext(i)[0]+'.pdf'
                converted.save(filename=fileout)
                print("Converted",i,"from",img.format,"to",fileout,converted.format)

        pg_num += 1

        #wand.display.display(img)  #debug display
    
        



if __name__ == '__main__':
    pattern_tile(
        import_png='pattern.png',
        format='letter',
        dir_path='pdfs/')