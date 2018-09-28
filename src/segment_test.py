from . import segment
from Algorithmia.errors import AlgorithmException
from pytest import raises


def test_boilerplate():
    with raises(AlgorithmException) as ae:
        segment.apply(0)
    assert ae.value.error_type == 'UnsupportedError' and ae.value.message == "Only JSON accepted"
    
    with raises(AlgorithmException) as ae:
        segment.apply({})
    assert ae.value.error_type == 'InputError' and ae.value.message == "Must specify source image dir"

    with raises(AlgorithmException) as ae:
        segment.apply({'src': 'lala'})
    assert ae.value.error_type == 'InputError' and ae.value.message == "Must specify destination dir"


def test_segment():
    assert segment.apply({'src': 'data://.my/images', 'dst': 'data://.my/segments'}) == {}
