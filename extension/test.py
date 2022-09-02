import csv
from csvw import CSVW, Table
import pandas as pd
import requests


csv_url = "https://raw.githubusercontent.com/EyeofBeholder-NLeSC/assessments-ontology/fix-metadata/IPM_worker_profile.csv"
metadata_url = "https://raw.githubusercontent.com/EyeofBeholder-NLeSC/assessments-ontology/fix-metadata/metadata.json"
csv_path = "C:/Workspace/knime_repos/eyeofbeholder/data/IPM_assessment.csv"

data = CSVW(url=metadata_url)
print(data.tables[0].url.resolve(data.tables[0].base))