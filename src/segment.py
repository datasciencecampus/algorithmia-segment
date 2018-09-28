import Algorithmia
from Algorithmia.errors import AlgorithmException

import sys
sys.path.append('PSPNet')

import os
import chainer
from chainercv.utils import read_image
from chainercv.visualizations import vis_image
from chainercv.visualizations import vis_label
from datasets import ade20k_label_colors
from datasets import ade20k_label_names
from datasets import cityscapes_label_colors
from datasets import cityscapes_label_names
from pspnet import PSPNet
from glob import glob
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def load(src='data://.models/pspnet101_cityscapes_713_reference.npz'):
    client = Algorithmia.client()
    model = client.file(src).getFile().name
    psp_net = PSPNet(pretrained_model=model)
    chainer.cuda.get_device_from_id(0).use()
    psp_net.to_gpu(0)
    return psp_net

# avoid cold start
psp_net = load()

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

    return {}
