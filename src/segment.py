import Algorithmia
from Algorithmia.errors import AlgorithmException

import numpy as np
import chainer
from chainercv.utils import read_image

# see caveats section in:
# https://algorithmia.com/developers/algorithm-development/languages/python/
from .pspnet.pspnet import PSPNet

from PIL import Image
from glob import glob
from re import sub
#import os
import io
import time


def load(src):
    client = Algorithmia.client()
    model = client.file(src).getFile().name
    #s = os.path.getsize(model)
    #assert os.path.getsize(model) == 262925472
    #pspnet_cache = "/home/algo/chainer/dataset/pfnet/chainercv/models"
    #os.makedirs(pspnet_cache, exist_ok=True)
    #os.rename(model, pspnet_cache+"/pspnet101_cityscapes_713_reference.npz")
    #psp_net = PSPNet(pretrained_model='cityscapes')
    #/home/algo/.chainer/dataset/pfnet/chainercv/models
    #psp_net = PSPNet(pretrained_model=model)
    #chainer.cuda.get_device_from_id(0).use()
    #psp_net.to_gpu(0)
  
    # see pspnet/pspnet.py
    # if model (not name) provided, must also specify these.
    # if just model name 'cityscapes', no need.
    cityscapes_conf = {
        'n_class': 19,
        'input_size': (713, 713),
        'n_blocks': [3, 4, 23, 3],
        'mid_stride': True,
        'pyramids': [6, 3, 2, 1],
        'mean': np.array([123.68, 116.779, 103.939])
    }

    print("loading " + model)
    return PSPNet(pretrained_model=model, **cityscapes_conf)


# avoid cold start
# (if running on algorithmia) - so local unit tests work
# 
# note: this not working - probably getting kicked off slot since we need lots
# of heap
if __name__ == 'src.segment':
    t = time.time()    
    psp_net = load('data://.my/models/pspnet101_cityscapes_713_reference.npz')
    print("model loaded in {:d}ms".format(int(1000*(time.time()-t))))


def segment(src):
    src_img = read_image(src) # (bgr, w, h)
    psp_out = psp_net.predict([src_img])[0]
    psp_out = psp_out.astype('uint8')
    psp_out = Image.fromarray(psp_out)
    return psp_out


def segment_images(src, dst):
    algo_client = Algorithmia.client()
    src_dir = algo_client.dir(src)
    if not src_dir.exists():
        raise AlgorithmException("src ({}) does not exist".format(src))
    dst_dir = algo_client.dir(dst)
    if not dst_dir.exists():
        dst_dir.create()
    for src in src_dir.files():
        # for each DataFile
        # https://github.com/algorithmiaio/algorithmia-python/blob/master/Algorithmia/datafile.py
        # just copy for now...
        #algo_client.file(dst+"/"+sub("^.*/", "", src.getName())).putFile(src.getFile().name)

        t = time.time()
        src_file = src.getFile().name
        print("got {} in {:d}ms".format(src.getName(), int(1000*(time.time()-t))))

        t = time.time()
        psp_pred = segment(src_file)
        print("segmentation took {:d}ms".format(int(1000*(time.time()-t))))

        t = time.time()
        buf = io.BytesIO()
        psp_pred.save(buf, format='BMP')
        buf = buf.getvalue()
            
        # push psp_pred bytes to dst bmp. 
        dst_file = sub(".jpg$", ".bmp", sub("^.*/", "", src.getName()))
        algo_client.file(dst+"/"+dst_file).put(buf)
        print("uploaded {} in {:d}ms".format(dst+"/"+dst_file, int(1000*(time.time()-t))))
        return # <- debug


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
    t = time.time()
    segment_images(src, dst)
    return {
        'status': 'ok',
        'verbose': {
            '__name__': __name__,
            'time': int(1000*(time.time()-t))
        }
    }
