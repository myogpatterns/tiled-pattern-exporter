# image_tiler.py
# Breaks large format images (PNG) into individual tile PNGs
# Double check PNG export PPI is greater than 150 for pdf quality

from PIL import Image
import sys, os

Image.MAX_IMAGE_PIXELS = None

def image_tiler(image, format, dir_path):
    

    # open image as a PIL object
    image = Image.open(image)   

    # constants
    ppi=round(image.info['dpi'][0])
    format = format.lower()

    if (format == 'letter'):
        width = 7.5
        height = 10
        tile_width = round(width*ppi)
        tile_height = round(height*ppi)
    elif (format == 'tabloid'):
        width = 15
        height = 10
        tile_width = round(width*ppi)
        tile_height = round(height*ppi)
    elif (format == 'a0'):
        width = 30
        height = 45
        tile_width = round(width*ppi)
        tile_height = round(height*ppi)
    else:
        print("Format must be letter, tabloid, or a0. Case sensitive.")
        exit()

    # check Pattern.PNG meets requirements
    if hasattr(image, 'filename'):
        if ppi >= 299:
            print(image.filename,"is",image.size[0]/ppi,"inches by", image.size[1]/ppi,"inches")
        else:
            print(image.filename,"is less than 300 dpi")
            exit()
    else: 
        print("In image_tiler, pattern.png not found")
        exit()
 
    # tile image into seperate PNGs and save in dir_path
    #if image.size[0] % tile_width == 0 and image.size[1] % tile_height ==0 :
    currentx = 0
    currenty = 0
    i=1
    while currenty < image.size[1]:
        while currentx < image.size[0]:
            tile = image.crop((currentx,currenty,currentx + tile_width,currenty + tile_height))
            tile.save(dir_path + os.path.splitext(image.filename)[0] + "-" + str(i).zfill(2) + ".png","PNG", dpi=(ppi,ppi))
            currentx += tile_width
            i+=1
        currenty += tile_height
        currentx = 0
    print("Tiled",i-1,"single page pattern sheets")
    #else:
     #   print ("Your image does not fit neatly into",tile_width,"*",tile_height,"tiles")

if __name__ == '__main__':
    image_tiler(
        image = "pattern.png",
        format = "letter",
        dir_path='pdfs/')
