import fraplib
import pytest

from pathlib import Path
import czifile



@pytest.fixture()
def testfile():
    # put the data file to load in the test folder
    return czifile.CziFile(Path(__file__).parent / "testfile.czi")

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
    
    assert [650] == fraplib.get_gain(testfile)
    
    assert "Plan-Apochromat 40x/1.3 Oil DIC M27" == fraplib.get_objective(testfile)
     
    assert [0.1] == fraplib.get_power(testfile)
    
    expected = [(128.01983145986762, 128.00010304153278, 37.49985947114415)]
    assert expected == fraplib.get_regions(testfile)
    
    expected = [(5.488461102633269e-09, 2.8517287604581007e-11, 1.0378283869946033e-05)]
    assert expected == fraplib.get_regions(testfile, units="physical")
    
    expected = [(0.005488461102633269, 2.8517287604581008e-05, 10.378283869946033)]
    assert expected == fraplib.get_regions(testfile, units="microns")
    
    expected = {"X-scale": 0.276755273654613, "Y-scale": 0.276755273654613, "Z-scale": 0.0}
    assert expected == fraplib.get_scales(testfile)
    
    expected = {"BLEACH_START": 2827.2208624560003, "BLEACH_STOP": 2833.1649571760004}
    assert expected == fraplib.get_events(testfile)
    