import pytest

def test_smoke():
    try:
        import marktex
    except Exception as err:
        pytest.fail("MarkTex module fails to load: %s" % str(err))