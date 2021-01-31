# image_conv_pdf.py
# 
# Converts Pattern-#.png's in directory (created by image_tiler.py) to PDFs
# Wand is imagemagick
# PDFs at 300dpi

import os, glob, shutil
import img2pdf, wand.image

def image_conv_pdf(dir_path):
    #check if pattern-#.pngs exist
    png_list = sorted(glob.glob(dir_path+'pattern-*.png'))
    
    if glob.glob(dir_path+'pattern-*.png'): 
        #create_folder('.','pdfs')
        pass
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
    for j in png_list:
        convert2pdf(j)

def convert2pdf(image_path):
    filein = image_path
    fileout = os.path.splitext(filein)[0]+'.pdf'
    
    # wand save individual jpgs or pdfs not working    
    with wand.image.Image(filename=filein, resolution=300, units='pixelsperinch') as img:
        img.border('white',150,150)
        #img.density=300
        img.compression_quality=99
        #print("Converting",os.path.splitext(filein)[0],img.format,"and",img.size)
        img.save(filename=filein)
        with img.convert('pdf') as converted:
            converted.save(filename=fileout)
            print("Converted",filein,"from",img.format,"to",fileout,converted.format)
            

def hasAlpha(image_path):
    with wand.image.Image(filename=image_path) as img:
        alpha = img.alpha_channel
        return alpha

def removeAlpha(image_path, new_image_path):
    with wand.image.Image(filename=image_path) as img:
        img.alpha_channel = 'remove' #close alpha channel   
        img.background_color = wand.image.Color('white')
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
