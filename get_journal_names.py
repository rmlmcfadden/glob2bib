#!/usr/bin/python3

# import json
import pandas as pd
import requests
import yaml

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

# write the dictiony to a file
with open("journal_names.yaml", "w") as fh:
    # json.dump(journal_names, fh, indent=True)
    yaml.dump(journal_names, fh, default_flow_style=False)

# print(journal_names["short2long"]["Nat. Prod. Res., Part A"])
