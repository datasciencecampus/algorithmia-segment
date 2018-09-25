from . import segment

def test_segment():
    assert segment.apply("Jane") == "hello Jane"
