import logging
import coloredlogs
import json
import re

from sys import argv
from os import walk
from os.path import join
from PIL import Image
from pprint import pprint


class PackNode(object):
    """
    Creates an area which can recursively pack other areas of smaller sizes into itself.
    """
    def __init__(self, area):
        #if tuple contains two elements, assume they are width and height, and origin is (0,0)
        if len(area) == 2:
            area = (0,0,area[0],area[1])
        self.area = area

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self.area))

    def get_width(self):
        return self.area[2] - self.area[0]
    width = property(fget=get_width)

    def get_height(self):
        return self.area[3] - self.area[1]
    height = property(fget=get_height)

    def insert(self, area):
        if hasattr(self, 'child'):
            a = self.child[0].insert(area)
            if a is None: return self.child[1].insert(area)
            return a

        area = PackNode(area)
        if area.width <= self.width and area.height <= self.height:
            self.child = [None,None]
            self.child[0] = PackNode((self.area[0]+area.width, self.area[1], self.area[2], self.area[1] + area.height))
            self.child[1] = PackNode((self.area[0], self.area[1]+area.height, self.area[2], self.area[3]))
            return PackNode((self.area[0], self.area[1], self.area[0]+area.width, self.area[1]+area.height))

images = []
includes = '(png)|(jpg)'

def load_images(root, files):
    # global images
    for file in files:
        name = file.split('.')
        if re.findall(includes, name[-1]):
            logging.debug(f"Loading from {root} file: {file}")
            image = Image.open(join(root, file)).convert("RGBA")
            images.append((name[0], image))


if __name__ == "__main__":
    coloredlogs.install()
    
    assert len(argv) >= 4, "Usage: python3 combine_images_into_single.py dir size(two numbers seperated by space) "
    
    for root, dirs, files in walk(argv[1]):
        if 'manifest.json' in files:
            files.remove('manifest.json')
        if '_compiled.png' in files:
            files.remove('_compiled.png')
        
        load_images(root, files)  
    
    images = sorted([(data[1].size[0] * data[1].size[1], data[0], data[1]) for data in images])
    
    size = int(argv[2]), int(argv[3])
    tree = PackNode(size)
    out_image = Image.new("RGBA", size)
    """
    {
        name: image_name
        offset_x: int
        offset_y: int
        size_x: int
        size_y: int
    }
    """
    manifest = []
    
    for area, name, img in images:
        uv = tree.insert(img.size)
        if uv is None: 
            raise ValueError('Pack size too small.')
        logging.info(f"Pasting {name} into {uv.area}")
        out_image.paste(img, uv.area)
        manifest.append({
                "name": name[0],
                "offset_x": uv.area[0],
                "offset_y": uv.area[1],
                "size_x": uv.area[2] - uv.area[0],  # get correct size_x
                "size_y": uv.area[3] - uv.area[1]   # get correct size_y
                })
        
    out_image.save(join(argv[1], "_compiled.png"))
    manifest_file = open(join(argv[1], "manifest.json"), 'w', encoding='utf-8')
    json.dump(manifest, manifest_file, ensure_ascii=False, indent=4)
    manifest_file.close()
