# image_conv_pdf.py
# 
# Tiles, adds cut registration, alignment guides, and converts to PDF
# Wand is imagemagick
# PDFs at 300dpi
#
# add format parameter
# define formats and constants
# get exported png
# overlay alignment guides based on format
    # for A0, no cut lines
# tile, add borders, add cutlines, add texts per page
# convert tile to pdf and save
#
#


import os, glob, shutil, math
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
        #wand.display.display(img)  #debug display
        print(import_png +' is ' + str(img.width/ppi) + ' by '+ str(img.height/ppi) + ' at ' + str(img.resolution[0]) + ' ' + img.units)


        #### Alignment Guides ####
        if guides_png:
            with Image(filename=guides_png) as guides:
                img.composite(guides, left=0, top=0)

        # Expand to A0 tile size
        #if format == 'a0':
        if img.width < ppi_width:
            #with img[]
            print(img.size)

        #### Tile Img ####
        currentx = 0
        currenty = 0
        
        i=1
        
        while currenty < img.height:
            while currentx < img.width:
                with img[currentx:currentx+ppi_width, currenty:currenty+ppi_height] as tile:
                        tile_id = dir_path + os.path.splitext(import_png)[0] + "-" + str(i).zfill(2) +".png"
                        tile.save(filename=tile_id)
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

                
            # Add cut registrations
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

                    #wand.display.display(img)


            with img.convert('pdf') as converted:
                fileout = os.path.splitext(i)[0]+'.pdf'
                converted.save(filename=fileout)
                print("Converted",i,"from",img.format,"to",fileout,converted.format)

        pg_num += 1
    
        

#### Functions ####

#remove alpha channels for pdf conversion
    #for i in png_list: 
    #    if hasAlpha(i):     
    #        removeAlpha(i,i)
    #        print("Processing",i)
    #    else:
    #       pass

def hasAlpha(image_path):
    with Image(filename=image_path) as img:
        alpha = img.alpha_channel
        return alpha

def removeAlpha(image_path, new_image_path):
    with Image(filename=image_path) as img:
        img.alpha_channel = 'remove' #close alpha channel   
        img.background_color = Color('white')
        img.save(filename=new_image_path)


if __name__ == '__main__':
    pattern_tile(
        import_png='pattern.png',
        format='letter',
        dir_path='pdfs/')