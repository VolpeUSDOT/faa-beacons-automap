import easyocr
from PIL import Image, ImageDraw
import numpy
import os

def get_recognized_text(source_filepath, dest_filepath, ocr_reader, color_processing=False):
    '''
    If any instances of the text "Beacon" are found on image at source_filepath, saves annotated
    image to dest_filepath.

    Must pass in ocr_reader (text recognition model) as argument to avoid it being loaded into memory multiple times.
    
    If color_processing is True, attempts to isolate black text.
    '''

    img = Image.open(source_filepath)
    metadata = img.getexif() #save metadata (including projection info) before processing

    #white out all non-black pixels (try to add buffer around black pixels next to account for feathering?)
    if color_processing:
        print("     +--> color processing")
        img.convert('HSV')
        _, _, V = img.split()
        img = V.point(lambda p: p < 50 and 255)

    #find locations of text
    print("     +--> ocr")
    img_array = numpy.array(img) #convert to array
    all_text = ocr_reader.readtext(img_array)

    #filter for "beacon"
    print("     +--> filtering")
    beacon_instances = []

    def in_beacon(str):
        return "beacon".find(str) != -1
    
    def add_instance(text, entry):
        print(f'              text found: {text}')
        beacon_instances.append(entry)

    for entry in all_text:
        text = entry[1].lower().replace(" ", "")
        if len(text) == 2 and in_beacon(text):
            add_instance(text, entry)
        elif len(text) > 2 and len(text) < 15:
            #find all substrings of length 3 or greater and check if in the word beacon
            substrings = [text[i:j] for i in range(len(text)) for j in range(i+3, len(text)+1)]
            for substring in substrings:
                if in_beacon(substring):
                    add_instance(text, entry)
                    break
            
            #handling strings that are about the right length but may be badly misspelled
            #TODO: ERROR HERE SOMEWHERE
            # if len(text) in range(5, 10):
            #     filtered = ''
            #     for letter in text:
            #         if in_beacon(letter):
            #             filtered += letter
            #     if len(filtered) > 4:
            #         add_instance(text, entry)


    #draw polygon around "beacon" instances
    if beacon_instances:
        print("     +--> drawing and saving")

        for instance in beacon_instances:
            poly = ImageDraw.Draw(img)

            #reformat bounding box coordinates
            bb = instance[0]
            bb = [tuple(bb[0]), tuple(bb[1]), tuple(bb[2]), tuple(bb[3])]

            poly.polygon(bb, outline="red", width=8)

        #save annotated image and delete original
        img.save(dest_filepath, exif=metadata)
        os.remove(source_filepath)
    