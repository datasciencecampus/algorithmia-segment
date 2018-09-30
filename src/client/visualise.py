################################################################################
# Visualise segmentation algo results                                          #
# ============================================================================ #
# E.g., python3 visualise.py test_images result visualise                      #
#                                                                              #
# Phil Stubbings, ONS Data Science Campus.                                     #
################################################################################

import sys
import numpy as np
from PIL import Image
from re import sub
from glob import glob


def get_labels(alpha=255):
    """Cityscape classes.
    
    Colour codes for each class.

    Parameters
    ----------
    alpha: int
        Class alpha level - Useful for composite images.
       
    Returns
    -------
    list
        A list of {label, (r, g, b, a)}
    """
    return [
        {"road":          (128, 64,  128, alpha)},
        {"sidewalk":      (244, 35,  232, alpha)},
        {"building":      (255, 127, 0,   alpha)},
        {"wall":          (102, 102, 156, alpha)},
        {"fence":         (190, 153, 153, alpha)},
        {"pole":          (153, 153, 153, alpha)},
        {"traffic light": (250, 170, 30,  alpha)},
        {"traffic sign":  (255, 0,   0,   alpha)},
        {"vegetation":    (107, 142, 35,  alpha)},
        {"terrain":       (152, 251, 152, alpha)},
        {"sky":           (70,  130, 180, alpha)},
        {"person":        (0,   0,   255, alpha)},
        {"rider":         (255, 0,   0,   alpha)},
        {"car":           (255, 0,   0,   alpha)},
        {"truck":         (0,   0,   70,  alpha)},
        {"bus":           (0,   60,  100, alpha)},
        {"train":         (0,   80,  100, alpha)},
        {"motorcycle":    (0,   0,   230, alpha)},
        {"bicycle":       (119, 11,  32,  alpha)}
    ]


def colourise(bmp_file, labels):
    """Colourise an input bitmap.

    Converts an input bmp image into a colour coded jpg.

    Parameters
    ----------
    bmp_file: str
        Location of the bitmap image
    labels: list
        see get_labels()

    Returns
    -------
    Image
        pillow Image.
    """
    #np_bmp = cv2.imread(bmp_img, cv2.IMREAD_GRAYSCALE)
    bmp_img = Image.open(bmp_file)
    width, height = bmp_img.size
    bmp_np = np.array(bmp_img)
    np_all = np.uint8([list(labels[x].values())[0] for x in bmp_np.flatten()])
    np_all = np_all.reshape((height, width, 4))
    return Image.fromarray(np_all)
    

def composite(img_input, img_segments):
    """Combine two images into a composite.

    Parameters
    ----------
    img_input: Image
        Base image
    img_segments: Image
        see colourise()

    Returns
    -------
    Image
        pillow Image.
    """
    combo = img_input.copy()
    combo.paste(img_segments, (0, 0), img_segments)
    return combo


def process(input_image_dir, result_image_dir, visualise_dir):
    """Process segmentation algo results.

    Parameters
    ----------
    input_image_dir: str
        Location of original street-level (.jpg) images.
    result_image_dir: str
        Location of segementation algo (.bmp) results.
    visualise_dir: str
        Target output directory.

    Returns
    -------
    None
    """
    labels = get_labels(alpha=128)
    for result_file in glob(result_image_dir+"/*.bmp"):
        img_segments = colourise(result_file, labels)
        input_file = sub("^.*/", "", sub(".bmp", ".jpg", result_file))
        img_input = Image.open(input_image_dir+"/"+input_file)
        combo = composite(img_input, img_segments)
        combo.save(visualise_dir+"/"+input_file)
       

if __name__ == '__main__':
    process(*sys.argv[1:])
    print("take a look in visualise dir...")
