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


@knext.node(
    name="CSV Validator",
    node_type=knext.NodeType.MANIPULATOR,
    icon_path="icon.png",
    category=my_category,
)
@knext.output_table(
    name="CSV Urls",
    description="A list of Urls to the CSV files referred by the metadata file.",
)
class CSVWValidator:

    metadata_url = knext.StringParameter(
        label="Metadata File URL",
        description="Url to the metadata file",
        default_value="https://raw.githubusercontent.com/EyeofBeholder-NLeSC/assessments-ontology/fix-metadata/metadata.json",
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