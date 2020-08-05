from PIL import Image

'''
This function will compress an image located at <path>/<image_name>/ by lowering its [quality] factor.
The new compressed image is saved under <path>/COMPRESSED<image_name>
'''


def compress_image(path, image_name, quality):
    abs_path = path + image_name

    # Opening image, read mode.
    image = Image.open(abs_path, 'r')

    # Setting the path of the new lower quality file
    image_path = path + 'COMPRESSED' + image_name

    # Saving new image file with lower quality to compress size
    if image.mode in ('RGBA', 'p'):
        image.save(fp=image_path, quality=quality, optimize=True, format='PNG')

    elif image.mode in 'RGB':
        image.save(fp=image_path, quality=quality, optimize=True, format='JPEG')

    return image_path
