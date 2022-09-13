import os
import sys
import pytest


extension_path = os.path.abspath("../extension")
sys.path.insert(0, extension_path)

from my_extension import CSVWValidator as cv
from my_extension import validate_metadata_url


def test_validate_metadata_url():
    # url to a valid metadata file
    assert validate_metadata_url(
        "https://w3c.github.io/csvw/tests/test011/tree-ops.csv-metadata.json"
    )

    # empty string
    with pytest.raises(AssertionError) as e:
        validate_metadata_url("")

    # json but not json-ld
    with pytest.raises(AssertionError) as e:
        validate_metadata_url(
            "https://raw.githubusercontent.com/johan/world.geo.json/master/countries/AFG.geo.json"
        )

    # url not linking to a json file
    with pytest.raises(Exception) as e:
        validate_metadata_url("https://www.google.com/maps")
