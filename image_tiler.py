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


    format = format.lower() #make case-insensitive

    if (format == 'letter'):
        width = 7.5
        height = 10
    elif (format == 'tabloid'):
        width = 15
        height = 10
    elif (format == 'a0'):
        width = 30
        height = 45
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
    tile_width = round(width*ppi)
    tile_height = round(height*ppi)
    
    currentx = 0
    currenty = 0
    i=1
    all_tiles = []
    
    while currenty < image.size[1]:
        row_tile = []
        while currentx < image.size[0]:
            tile = image.crop((currentx,currenty,currentx + tile_width,currenty + tile_height))
            tile_id = dir_path + os.path.splitext(image.filename)[0] + "-" + str(i).zfill(2) +".png"
            tile.save(tile_id, "PNG", dpi=(ppi,ppi))
            currentx += tile_width
            row_tile.append(tile_id)
            i+=1
        currenty += tile_height
        all_tiles.append(row_tile)
        currentx = 0
    print("Tiled",i-1,"single page pattern sheets")

    return(all_tiles)


if __name__ == '__main__':
    image_tiler(
        image = "pattern.png",
        format = "letter",
        dir_path='pdfs/')
