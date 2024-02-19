import pandas as pd
from pathlib import Path


root_path = Path(r"../data/")

all_df = list()
for file in root_path.iterdir():
    if file.is_file() and file.suffix.lower() == ".csv":
        df = pd.read_csv(file)
        all_df.append(df)

DF = pd.concat(all_df, axis=0)
print(DF.shape)

DF.to_csv("../data/all_data.csv", encoding="utf-8", index=False)
