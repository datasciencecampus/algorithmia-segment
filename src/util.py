################################################################################
# Utils                                                                        # 
# ============================================================================ #
# Phil Stubbings, ONS Data Science Campus.                                     #
################################################################################

from Algorithmia.errors import AlgorithmException


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
