import pytest

def test_smoke():
    try:
        import songbook
    except Exception as err:
        pytest.fail("SongBook module fails to load: %s" % str(err))