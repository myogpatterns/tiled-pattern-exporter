# image_conv_pdf.py
# 
# Converts Pattern-#.png's in directory (created by image_tiler.py) to PDFs
# Wand is imagemagick
# PDFs at 300dpi

import os, glob, shutil, math
from wand.image import Image, Color
from wand.drawing import Drawing

def image_conv_pdf(dir_path):
    #check if pattern-#.pngs exist
    
    if glob.glob(dir_path+'*-*.png'): 
        png_list = sorted(glob.glob(dir_path+'*-*.png'))
    else:
        print("No Pattern-#.pngs found. Run image_tiler first")

    #list pngs and remove alpha channels for pdf conversion, place file in /pdfs
    
    for i in png_list: 
        
        if hasAlpha(i):     
            removeAlpha(i,i)
            print("Processing",i)
        else:
            #shutil.move(i,dir_path)
            pass
        
        #convert to pngs to pdfs
    for index, j in enumerate(png_list):
        convert2pdf(index, j)

def convert2pdf(index, image_path):
    pg_num = index
    filein = image_path
    fileout = os.path.splitext(filein)[0]+'.pdf'
    
    # wand save individual jpgs or pdfs not working    
    with Image(filename=filein, resolution=300, units='pixelsperinch') as img:
        #img.border('white',150,150)
        img.border('white', 150, 150)
        #border 0.5 inch = 150/300
        
        with Drawing() as draw:
            # cut registration lines
            draw.line((0,150),(img.width,150))
            draw.line((0,img.height-150),(img.width,img.height-150))
            draw.line((150,0),(150,img.height))
            draw.line((img.width-150,0),(img.width-150,img.height))
            # alignment guides
            
            
            draw.push()
            draw.stroke_width=1
            draw.stroke_color='red'
            draw.fill_opacity=0
            sq_size = math.sqrt(300**2+300**2)/2
            draw.translate(x=img.width-150, y=img.height/2-150)
            
            draw.rotate(45)
            draw.rectangle(left=0, top=0, width=sq_size, height=sq_size)
            
            draw.pop()
            # texts
            draw.font_size = 10
            draw.text_alignment='center'
            draw.fill_color = 'grey50'
            draw.text(int(img.width/2), int(img.height-100),"2021 © LearnMYOG.com")
            draw.text(int(img.width-100), int(img.height-100),str(pg_num+1))
            draw(img)


        #img.save(filename=filein)
        with img.convert('pdf') as converted:
            converted.save(filename=fileout)
            print("Converted",filein,"from",img.format,"to",fileout,converted.format)
            

def hasAlpha(image_path):
    with Image(filename=image_path) as img:
        alpha = img.alpha_channel
        return alpha

def removeAlpha(image_path, new_image_path):
    with Image(filename=image_path) as img:
        img.alpha_channel = 'remove' #close alpha channel   
        img.background_color = Color('white')
        img.save(filename=new_image_path)

# def create_folder(self, path):
#     try:
#         if os.path.isdir(path):
#             print("Error: The directory you're attempting to create already exists") # or just pass
#         else:
#             os.makedirs(path)
#             print(path,"created")
#     except IOError as exception:
#         raise IOError('%s: %s' % (path, exception.strerror))
#     return None

if __name__ == '__main__':
    image_conv_pdf(
        dir_path='pdfs/')
