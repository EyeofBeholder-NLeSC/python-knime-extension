import logging
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


@knext.node(
    name="CSVW Validator",
    node_type=knext.NodeType.MANIPULATOR,
    icon_path="icon.png",
    category=my_category,
)
@knext.input_table(
    name="Input Data",
    description="The input data table that should come from a CSV Reader node.",
)
@knext.output_table(
    name="Output Data",
    description="The output data table that should be exactly the same as the input.",
)
class CSVWValidator:
    """
    This node uses the CoW (Csv on the Web) library for validation. It accepts one data table that is read from a csv file. If the input passes the validation, the output port will return exactly the same table as the input. Otherwise, the node will fail to execute. For validation, the URL to the metadata file must be provided in the configuration dialog before execution.
    """

    metadata_url = knext.StringParameter(
        "Metadata File URL", "The classic placeholder", ""
    )

    def configure(self, configure_context, input_schema_1):
        # Should return the same schema as the input if valid
        return input_schema_1

    def execute(self, exec_context, input_1):
        # Throw the exception if validation is failed
        metadata_url = exec_context.flow_variables["input_path_location"]
        data = CSVW(url=metadata_url, validate=True)

        # If validation passed, output the table
        LOGGER.warning("Validation successed!")
        return knext.Table.from_pandas(pd.DataFrame(data.tables[0]))
