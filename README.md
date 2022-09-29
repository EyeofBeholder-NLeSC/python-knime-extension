# python-knime-extension

This is the repo for keeping the source code of all the KNIME nodes developed for the Eye of the Beholder project.

<!--
## Installation

To use this extension, you should have the KNIME Analytics Platform (KAP) version 4.6 or higher installed on your machine. You can download it from their [official website](https://www.knime.com/downloads).

After you have the correct version of KAP installed, follow the steps below to install the extension:
- Clone this repo to your machine.
If you don't have Git LFS (Large File Storage) installed, you should do that beforehand.
- In KAP, add the `bundled_extension` folder in this repo to KAP as a software site in *File → Preferences → Install/Update → Available Software Sites*
- Install it by clicking *File → Install KNIME Extensions*, search for "eye of beholder" and install all items that show up.
-->

## Node list

### CSV Validator

This is the node for validating csv files based on a given metadata file describing a predefined data schema. The validation is done by following the [CSVW (CSV on the Web)](https://www.w3.org/TR/tabular-data-primer/) standard.

- Output: a data table that stores a list of URLs to the CSV files referred by the metadata file provided
- Configuration:
    - Metadata File URL: the URL to the given metadata file

### CSV Normalizer

This is the node for converting the input data table into the desired format based on a specified data schema.

- Input: a data table that stored the URL to the CSV file to be normalized, there should be only one row of column "csv_urls" in the table.
- Output: the normalized table
- Configuration:
    - Metadata File URL: the URL to the given metadata file
