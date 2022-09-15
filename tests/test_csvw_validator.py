import os
import sys
from unittest.mock import patch
import pytest
from knime_extension.knime_node_table import _Backend
import knime_extension


extension_path = os.path.abspath("../extension")
sys.path.insert(0, extension_path)

from my_extension import CSVWValidator as cv
from my_extension import validate_metadata_url


class ConcreteBackend(_Backend):
    def create_table_from_pandas(self, data, sentinel):
        return data


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


def test_validator_execute():
    validator = cv()

    # negative test
    with pytest.raises(AssertionError) as e:
        validator.metadata_url = (
            "https://w3c.github.io/csvw/tests/test111-metadata.json"
        )
        validator.execute(None)

    # check output
    knime_extension.knime_node_table._backend = ConcreteBackend()
    validator.metadata_url = "https://w3c.github.io/csvw/tests/countries.json"
    r = validator.execute(None)
    assert r.shape[0] == 2
    assert (
        r["csv_urls"].iloc[0] == "https://w3c.github.io/csvw/tests/countries.csv"
        and r["csv_urls"].iloc[1]
        == "https://w3c.github.io/csvw/tests/country_slice.csv"
    )
