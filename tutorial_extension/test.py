import csv
from csvw import CSVW
import json

data = CSVW("C:\\Users\\qiji1\\data\\tree-ops.csv")
print(json.dumps(data.to_json(minimal=True), indent=4))