import pandas as pd
import json

# opening the data file
file = open("data.json")

# reading the file as a list line by line
content = file.readlines()
file.close()
# parse x:
y = json.loads(json.dumps(content))

# the result is a Python dictionary:
# print(y)

df = pd.read_json(path_or_buf='data.json',lines=True)

print(df.columns) 
