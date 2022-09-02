import logging
from this import d
import knime_extension as knext
from csvw import CSVW
import pandas as pd

LOGGER = logging.getLogger(__name__)

my_category = knext.category(
    path="/",
    level_id="eye_of_beholder",
    name="Eye of Beholder",
    description="This is the KNIME extension that includes nodes for the Eye of Beholder project.",
    icon="icon.png",
)


class CSVURLNotInMetadata(Exception):
    """
    Exception raised for errors in the csv normalizer node, when the input CSV URL is not found in the metadata file provided.
    """

    def __init__(self, message="The input CSV URL is not found in the metadata file."):
        self.message = message
        super().__init__(self.message)


@knext.node(
    name="CSV Validator",
    node_type=knext.NodeType.MANIPULATOR,
    icon_path="icon.png",
    category=my_category,
)
@knext.output_table(
    name="CSV URLs",
    description="A list of Urls to the CSV files referred by the metadata file.",
)
class CSVWValidator:
    """
    This node uses the Python CSVW library (https://github.com/cldf/csvw) for csv files validation. This node assumes that the CSV files are embedded with the metadata file in a remote place. To validate, fill in the URL to the metadata file in the configuration dialog. By executing the node, if the validation passes, it will output a table that contains the list of the validated CSV files. Otherwise, this node will encounter an error.
    """

    metadata_url = knext.StringParameter(
        label="Metadata File URL",
        description="URL to the metadata file",
    )

    def configure(self, configure_context):
        pass

    def execute(self, execute_context):
        result = CSVW(url=self.metadata_url, validate=True)  # csvw validation
        csv_list = []
        for i in range(len(result.tables)):
            base = result.tables[i].base
            csv_list.append(result.tables[i].url.resolve(base))
        return knext.Table.from_pandas(pd.DataFrame(csv_list, columns=["csv_urls"]))


@knext.node(
    name="CSV Normalizer",
    node_type=knext.NodeType.MANIPULATOR,
    icon_path="icon.png",
    category=my_category,
)
@knext.input_table(
    name="CSV URL", description="The URL to the CSV file that will be normalized."
)
@knext.output_table(name="Normalized Table", description="The normalized table.")
class CSVNormalizer:
    """
    This node normalizes a CSV file based on a corresponding metadata file.
    """

    metadata_url = knext.StringParameter(
        label="Metadata File URL",
        description="URL to the metadata file",
    )

    def configure(self, configure_context, input_schema):
        pass

    def execute(self, execute_context, input_table):
        result = CSVW(url=self.metadata_url, validate=True)
        csv_url = input_table.to_pandas()["csv_urls"].iloc[0]
        if len(result.tables) == 1:
            return knext.Table.from_pandas(pd.DataFrame(result.tables[0]))
        else:  # in case of multiple csv files referred by the metadata file
            for i in range(len(result.tables)):
                base = result.tables[i].base
                target_url = result.tables[i].url.resolve(base)
                if target_url == csv_url:
                    return knext.Table.from_pandas(pd.DataFrame(result.tables[i]))

        # if the input CSV URL is not found in the metadata, raise an exception
        raise CSVURLNotInMetadata()
