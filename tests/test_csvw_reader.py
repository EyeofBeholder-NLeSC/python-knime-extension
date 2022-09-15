import os
import sys
import pytest


extension_path = os.path.abspath("../extension")
sys.path.insert(0, extension_path)

from my_extension import CSVWReader as cr
