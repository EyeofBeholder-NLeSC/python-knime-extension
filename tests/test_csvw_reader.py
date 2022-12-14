import os
from re import I
import sys
import pytest
from knime_extension.knime_schema import Schema, string
from knime_extension.knime_node_table import _Backend
import knime_extension
import pandas as pd

extension_path = os.path.abspath("../extension")
sys.path.insert(0, extension_path)

from my_extension import CSVWReader as cr


class ConcreteBackend(_Backend):
    def create_table_from_pandas(self, data, sentinel):
        return data


knime_extension.knime_node_table._backend = ConcreteBackend()


class KTable:
    def __init__(self, df):
        self.df = df

    def to_pandas(self, sentinel=None):
        return self.df


@pytest.fixture
def reader():
    r = cr()
    r.metadata_url = (
        "https://w3c.github.io/csvw/tests/test011/tree-ops.csv-metadata.json"
    )
    return r


def test_reader_configure_positive(reader):
    input_schema = Schema(ktypes=[string()], names=["csv_urls"])
    reader.configure(None, input_schema)


def test_reader_configure_negative(reader):
    input_schema = Schema(ktypes=[string()], names=["arbitrary_name"])
    with pytest.raises(
        AssertionError, match='Input doesn\'t contains column "csv_urls"!'
    ):
        reader.configure(None, input_schema)


def test_reader_execute_positive(reader):
    input_df = pd.DataFrame(
        {"csv_urls": ["https://w3c.github.io/csvw/tests/test011/tree-ops.csv"]}
    )
    input_table = KTable(input_df)
    output_df = reader.execute(None, input_table)
    assert (
        "on_street" in output_df.columns
    )  # column name "On Street" is changed to "on_street"
    assert (
        output_df.dtypes["GID"] == "O"
    )  # GID is int originally but read as string (object)


def test_reader_execute_negative_no_input(reader):
    input_df = pd.DataFrame({"csv_urls": []})
    input_table = KTable(input_df)
    with pytest.raises(AssertionError, match="None or more than 2 CSVs in the input!"):
        reader.execute(None, input_table)


def test_reader_execute_negative_multiple_input(reader):
    input_df = pd.DataFrame(
        {
            "csv_urls": [
                "https://w3c.github.io/csvw/tests/test011/tree-ops.csv",
                "https://w3c.github.io/csvw/tests/countries.csv",
            ]
        }
    )
    input_table = KTable(input_df)
    with pytest.raises(AssertionError, match="None or more than 2 CSVs in the input!"):
        reader.execute(None, input_table)


def test_reader_execute_negative_input_not_found(reader):
    input_df = pd.DataFrame(
        {"csv_urls": ["https://w3c.github.io/csvw/tests/countries.csv"]}
    )
    input_table = KTable(input_df)
    with pytest.raises(Exception, match="Input invalid or not found in Metadata!"):
        reader.execute(None, input_table)
