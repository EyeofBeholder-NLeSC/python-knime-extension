# python-knime-extension

This is the repo for keeping the source code of all the KNIME nodes developed for the Eye of the Beholder project.

## Installation

To use this extension, you should have the KNIME Analytics Platform (KAP) version 4.6 or higher installed on your machine. You can download it from their [official website](https://www.knime.com/downloads).

After you have the correct version of KAP installed, follow the steps below to install the extension:
- Clone this repo to your machine.
- In KAP, add the `bundled_extension` folder in this repo to KAP as a software site in *FileFile → Preferences → Install/Update → Available Software Sites*
- Install it by clicking *File → Install KNIME Extensions*, search for "eye of beholder" and install all items that show up.

## Node list

### CSVW Validator

This is the node(s) for reading a csv file and the corresponding metadata file as input and validating the csc file based on the [CSVW (CSV on the Web)](https://www.w3.org/TR/tabular-data-primer/) standard.

#### Input

The input files should be stored either locally or in a publicly accessible remote origin (e.g. a public GitHub repo). Note that the files should be put together, and the metadata file should be named as `<csv-file-name.csv>-metadata.json`.
