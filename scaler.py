from PIL import Image
import configparser
import os
from pathlib import PurePath

def scaler(path, scale, output_format, save_path, image, prefix, suffix):
        image_path = os.path.join(path, image)
        parent_folder = PurePath(image_path).parent.name
        im = Image.open(image_path)
        width, height = im.size
        file, ext = os.path.splitext(image)
        ext, output_format = get_output_format(ext, output_format)
        new_path = os.path.join(save_path, parent_folder)
        os.makedirs(new_path, exist_ok=True) 
        new_file = os.path.join(new_path, prefix + file + suffix + ext)
        if type(scale) == float:
            imResize = im.resize((int(scale * width), int(scale * height)))
            imResize.save(new_file, output_format, quality=100)
        elif type(scale) == tuple:
            imResize = im.resize((scale[0], scale[1]))
            imResize.save(new_file, output_format, quality=100)

def get_output_format(ext, output_format):
    if output_format.lower() == "original":
        return ext, ext[1::]
    if output_format.lower() == "jpeg":
        ext = ".jpg"
    else:
        ext = ".png"
    return ext, output_format

def scale_images(path, scale, output_format, save_path, prefix, suffix):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            image = item
            scaler(path, scale, output_format, save_path, image, prefix, suffix)

def main():
    config = configparser.ConfigParser()
    config.read("paths.ini")

    save_path = os.path.abspath(config["DEFAULT"]["savepath"])
    for section in config.sections():
        path = config[section]["path"]
        scale = eval(config[section]["scale"])
        output_format = config[section]["outputformat"]
        prefix = config[section]["prefix"]
        if prefix.lower() == "none":
            prefix = ""
        suffix = config[section]["suffix"]
        if suffix.lower() == "none":
            suffix = ""
        scale_images(path, scale, output_format, save_path, prefix, suffix)


if __name__ == '__main__':
    main()