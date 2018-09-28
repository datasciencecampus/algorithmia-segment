import Algorithmia
from Algorithmia.errors import AlgorithmException

import chainer
from chainercv.utils import read_image

# see caveats section in:
# https://algorithmia.com/developers/algorithm-development/languages/python/
from .pspnet.pspnet import PSPNet

from PIL import Image
from glob import glob
from re import sub


def load(src):
    client = Algorithmia.client()
    model = client.file(src).getFile().name
    
    import os
    s = os.path.getsize(model)
    raise Exception(model + " " + s)
    psp_net = PSPNet(pretrained_model=model)
    #chainer.cuda.get_device_from_id(0).use()
    #psp_net.to_gpu(0)
    return psp_net

# avoid cold start
psp_net = load('data://.my/models/pspnet101_cityscapes_713_reference.npz')


def segment(src, dst):
    src_img = read_image(src) # (bgr, w, h)
    psp_out = psp_net.predict([img])[0]
    psp_out = psp_out.astype('uint8')
    psp_out = Image.fromarray(psp_out)
    return psp_out


def segment_images(src, dst):
    algo_client = Algorithmia.client()
    src_dir = algo_client.dir(src)
    if not src_dir.exits():
        raise AlgorithmException("src ({}) does not exist".format(src))
    dst_dir = algo_client.dir(dst)
    if not dst_dir.exists():
        dst_dir.create()
    for src in src_dir.files():
        # just copy for now...
        algo_client.file(dst+"/"+sub("^.*/", "", src.name)).putFile(src.name)


def sanity(input):
    """boilerplate input sanity check.
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
    sanity(input)
    src, dst = input['src'], input['dst']
    segment_images(src, dst)
    return {
        'status': 'ok',
        'verbose': {
            '__name__': __name__
        }
    }
