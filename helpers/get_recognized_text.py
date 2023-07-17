import easyocr
from PIL import Image, ImageDraw
import numpy

def get_recognized_text(source_filepath, dest_filepath, color_processing=True):
    '''
    If any instances of the text "Beacon" are found on image, saves annotated
    image to dest_filepath.

    If color_processing is True, attempts to isolate black text.
    '''

    img = Image.open(source_filepath)

    #white out all non-black pixels (try to add buffer around black pixels next to account for feathering?)
    if color_processing:
        width = img.size[0] 
        height = img.size[1] 
        for i in range(0,width):
            for j in range(0,height):
                data = img.getpixel((i,j))
                if not (data[0]<125 and data[1]<125 and data[2]<125):
                    img.putpixel((i,j),(255, 255, 255))

    #find locations of text
    img_array = numpy.array(img) #convert to array
    reader = easyocr.Reader(['en']) # load the model into memory - MOVE OUTSIDE FUNCTION
    all_text = reader.readtext(img_array)

    #filter for "beacon"
    beacon_instances = []
    for entry in all_text:
        text = entry[1].lower()
        if len(text) > 2:
            if "beacon".find(text) != -1:
                beacon_instances.append(entry)
    
    #draw rectangle around "beacon" instances
    if beacon_instances:
        for instance in beacon_instances:
            rec = ImageDraw.Draw(img)
            bounding_box = [tuple(instance[0][0]), tuple(instance[0][2])]
            rec.rectangle(bounding_box, outline="red", width=6)
        img.save(dest_filepath) #save annotated image

    