import fraplib
import pytest

from pathlib import Path
import czifile



@pytest.fixture()
def testfile():
    # put the data file to load in the test folder
    return czifile.CziFile(Path(__file__).parent / "B2_40xOil_003_bleach.czi")

def test_metadata(testfile):
    expected = {
        "SizeB": 1,
        "SizeV": 1,
        "SizeC": 1,
        "SizeT": 45,
        "SizeZ": 1,
        "SizeY": 256,
        "SizeX": 256,
        "Size0": 1,
    }

    assert expected == fraplib.get_dims(testfile)


    expected = [(638.0000000000002, 759.0000000000001)]
    assert expected == fraplib.get_em(testfile)
    assert [633.0] == fraplib.get_ex(testfile)
