#!/usr/bin/python3

import json
from os import environ
import pandas as pd
import requests

# get the journal abbreviations list from the ubc library
url = "https://journal-abbreviations.library.ubc.ca/fulllist.php"
html = requests.get(url).content

# parse the html and extra the table as a pandas dataframe
df_list = pd.read_html(html)
df = df_list[-1]

# drop NaN rows
df = df.dropna()

# some empty dictionaries to store the entries
journal_names = {}
journal_names["long2short"] = {}
journal_names["short2long"] = {}

# add the names to the dictionary
for long_name, short_name in zip(df["Title"], df["Abbreviation"]):
    journal_names["long2short"][long_name] = short_name
    journal_names["short2long"][short_name] = long_name

    # some common ones that the ubc list missed...
    journal_names["short2long"][
        "Phys. Rev. A"
    ] = "Physical Review A: Atomic, Molecular, and Optical Physics"
    journal_names["short2long"]["Phys. Rev. B"] = "Physical Review B: Condensed Matter"
    journal_names["short2long"]["Phys. Rev. C"] = "Physical Review C: Nuclear Physics"
    journal_names["short2long"][
        "Phys. Rev. D"
    ] = "Physical Review D: Particles and Fields"
    journal_names["short2long"][
        "Phys. Rev. E"
    ] = "Physical Review E: Statistical, Nonlinear, and Soft Matter Physics"

# write the dictiony to a file
with open(environ["HOME"] + "/.journal_names.json", "w") as fh:
    json.dump(journal_names, fh, indent=3, separators=(",", ": "))
