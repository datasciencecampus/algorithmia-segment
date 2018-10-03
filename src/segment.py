################################################################################
# Algorithmia image segmentation algorithm                                     #
# ============================================================================ #
# Phil Stubbings, ONS Data Science Campus.                                     #
################################################################################

import Algorithmia
from Algorithmia.errors import AlgorithmException

import numpy as np
import chainer
from chainercv.utils import read_image

# see caveats section in:
# https://algorithmia.com/developers/algorithm-development/languages/python/
from .dsc_chainer_pspnet.pspnet import PSPNet

from PIL import Image
from glob import glob
from re import sub
import io
import time


def load(src, conf, use_gpu=False):
    """Load a PSPNet.

    This will initialise an instance of PSPNet pre-trained on the Cityscapes
    dataset.

    Parameters
    ----------
    src: str
        The pre-trained model weights.        
    conf: dict
        The model conf. (Must match pre-trained weights)
    use_gpu: bool, optional)
        If True, will try to use GPU. (Requires CUDA)

    Returns
    -------
    pspnet.PSPNet
        An instance of PSPNet
    """
    algo_client = Algorithmia.client()
    model = algo_client.file(src).getFile().name
 
    t = time.time()
    psp_net = PSPNet(pretrained_model=model, **conf)
    print("model loaded in {:d}ms".format(int(1000*(time.time()-t))))

    if use_gpu:
        #chainer.cuda.get_device_from_id(0).use()
        psp_net.to_gpu()

    return psp_net


pspnet_conf = {
    'src': 'data://nocturne/models/pspnet101_cityscapes_713_reference.npz',
    'conf': {
        'n_class': 19,
        'input_size': (713, 713),
        'n_blocks': [3, 4, 23, 3],
        'mid_stride': True,
        'pyramids': [6, 3, 2, 1],
        'mean': np.array([123.68, 116.779, 103.939])
    },
    'use_gpu': True 
}
# will persist whilst in slot. 
# avoids cold-starts. see:
# https://blog.algorithmia.com/advanced-algorithm-design/
psp_net = load(**pspnet_conf)


def segment(src):
    """Segment an individual image.
    
    Parameters
    ----------
    src: str
        Local location of input image.

    Returns
    -------
    pillow Image
        A bitmap image with up to 255 possible classes per pixel.
    """
    src_img = read_image(src) # (bgr, w, h)
    psp_out = psp_net.predict([src_img])[0]
    psp_out = psp_out.astype('uint8')
    psp_out = Image.fromarray(psp_out)
    return psp_out


def segment_images(src, dst):
    """Segment a collection of images.

    This will iterate over all images in the src directory, segment each one and
    then stash the results in dst directory.

    Parameters
    ----------
    src: str
        The directory containing input (.jpg) images.
    dst: str
        The destination/target directory to put segmentation results (.bmp) in.

    Returns
    -------
    int
        Average time, in milliseconds, to process each image.
    """
    algo_client = Algorithmia.client()

    src_dir = algo_client.dir(src)
    if not src_dir.exists():
        raise AlgorithmException("src ({}) does not exist".format(src))

    dst_dir = algo_client.dir(dst)
    if not dst_dir.exists():
        dst_dir.create()

    # src = DataFile. see:
    # https://github.com/algorithmiaio/algorithmia-python/blob/master/Algorithmia/datafile.py
    t = time.time()
    src_files = src_dir.files()
    i = 0
    for src in src_files:

        # target file
        dst_file = sub(".jpg$", ".bmp", sub("^.*/", "", src.getName()))
        algo_dst_file = algo_client.file(dst+"/"+dst_file)

        # skip if already done.
        if algo_dst_file.exists():
            continue

        # fetch local copy of input .jpg image
        t = time.time()
        src_file = src.getFile().name
        print("got {} in {:d}ms".format(src.getName(), int(1000*(time.time()-t))))

        # segment the image using PSPNet
        t = time.time()
        psp_pred = segment(src_file)
        print("segmentation took {:d}ms".format(int(1000*(time.time()-t))))

        # stash the result in buffer
        t = time.time()
        buf = io.BytesIO()
        psp_pred.save(buf, format='BMP')
        buf = buf.getvalue()
            
        # push psp_pred bytes to destination .bmp
        algo_dst_file.put(buf)
        print("uploaded {} in {:d}ms".format(dst+"/"+dst_file, int(1000*(time.time()-t))))

        i += 1

    return int((1000*(time.time()-t))/max(1, i))


def sanity(input):
    """Boilerplate input sanity check.
    
    see:

    https://algorithmia.com/developers/algorithm-development/algorithm-basics/algorithm-errors/
    https://github.com/algorithmiaio/algorithmia-python/blob/master/Algorithmia/errors.py
    """
    if type(input) is not dict:
        raise AlgorithmException("Only JSON accepted", 'UnsupportedError')
    if 'src' not in input:
        raise AlgorithmException("Must specify source image dir", 'InputError')
    if 'dst' not in input:
        raise AlgorithmException("Must specify destination dir", 'InputError')


def apply(input):
    """Algorithmia entry point."""

    sanity(input)
    src, dst = input['src'], input['dst']
    t = time.time()
    image_time = segment_images(src, dst)
    
    return {
        'status': 'ok',
        'verbose': {
            '__name__': __name__,
            'total_time': int(1000*(time.time()-t)),
            'image_time': image_time
        }
    }
