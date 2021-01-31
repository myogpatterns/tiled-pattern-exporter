# image_tiler.py
# Breaks large format images (PNG) into individual tile PNGs
# Double check PNG export PPI is 300

from PIL import Image
import sys, os

Image.MAX_IMAGE_PIXELS = None

def image_tiler(image, tile_width, tile_height, dir_path):
    # constants
    ppi=300
    tile_width = tile_width*ppi
    tile_height = tile_height*ppi

    # open image as a PIL object
    image = Image.open(image)   

    # check Pattern.PNG meets requirements
    if hasattr(image, 'filename'):
        if image.info['dpi'] == (300,300):
            print(image.filename,"is",image.size[0]/ppi,"inches by", image.size[1]/ppi,"inches")
        else:
            print(image.filename,"is not 300 dpi")
            exit()
    else: 
        print("In image_tiler, pattern.png not found")
        exit()
 
    # tile image into seperate PNGs and save in dir_path
    if image.size[0] % tile_width == 0 and image.size[1] % tile_height ==0 :
        currentx = 0
        currenty = 0
        i=1
        while currenty < image.size[1]:
            while currentx < image.size[0]:
                tile = image.crop((currentx,currenty,currentx + tile_width,currenty + tile_height))
                tile.save(dir_path + os.path.splitext(image.filename)[0] + "-" + str(i).zfill(2) + ".png","PNG")
                currentx += tile_width
                i+=1
            currenty += tile_height
            currentx = 0
        print("Tiled",i-1,"single page pattern sheets")
    else:
        print ("Your image does not fit neatly into",tile_width,"*",tile_height,"tiles")

if __name__ == '__main__':
    image_tiler(
        image = "pattern.png",
        tile_width = 7.5,
        tile_height = 10,
        dir_path='pdfs/')
