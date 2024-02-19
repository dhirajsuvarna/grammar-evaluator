import pandas as pd


file_path = r"F:\projects\freelancing\grammar-stuff\grammar_checker\data\all_data.csv"

df = pd.read_csv(file_path)
print(df.shape)

# df["USER_ANSWER"].to_csv("user_answer.csv", index=False, encoding="utf-8")
df = df[df["USER_ANSWER"].notna()]
print(df.shape)
