from . import segment
from Algorithmia.errors import AlgorithmException
from pytest import raises


def test_boilerplate():
    with raises(AlgorithmException) as ae:
        segment.apply(0)
    assert ae.value.error_type == 'UnsupportedError' and ae.value.message == "Only JSON accepted"
    
    with raises(AlgorithmException) as ae:
        segment.apply({})
    assert ae.value.error_type == 'InputError' and ae.value.message == "Must specify image(s)"

    with raises(AlgorithmException) as ae:
        segment.apply({'images': 0})
    assert ae.value.error_type == 'InputError' and ae.value.message == "Must specify image(s)"

    with raises(AlgorithmException) as ae:
        segment.apply({'images': []})
    assert ae.value.error_type == 'InputError' and ae.value.message == "Must specify image(s)"

    with raises(AlgorithmException) as ae:
        segment.apply({'images': ""})
    assert ae.value.error_type == 'InputError' and ae.value.message == "Must specify image(s)"


def test_segment():
    assert segment.apply({'images': "x"}) == {}
    assert segment.apply({'images': ["x"]}) == {}
