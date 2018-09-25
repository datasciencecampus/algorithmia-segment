import Algorithmia
from Algorithmia.errors import AlgorithmException


def sanity(input):
    """boilerplate input sanity check.
    see:
    https://algorithmia.com/developers/algorithm-development/algorithm-basics/algorithm-errors/
    https://github.com/algorithmiaio/algorithmia-python/blob/master/Algorithmia/errors.py
    """
    if type(input) is not dict:
        raise AlgorithmException("Only JSON accepted", 'UnsupportedError')
    if 'images' not in input:
        raise AlgorithmException("Must specify image(s)", 'InputError')
    images = input['images']
    if not (type(images) is list or type(images) is str):
        print(type(images))
        raise AlgorithmException("Must specify image(s)", 'InputError')
    if len(images) == 0:
        raise AlgorithmException("Must specify image(s)", 'InputError')


def apply(input):
    sanity(input)
    return {}
